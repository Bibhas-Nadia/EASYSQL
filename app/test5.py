import difflib
import re

def checkSyntax(query, schema):
    """
    Check and correct common SQL syntax errors in the given query using the provided database schema.
    :param query: The SQL query string to check.
    :param schema: Dict mapping table names to list of column names (strings).
    :return: (corrected_query, errors) where errors is a list of strings describing fixes applied.
    """
    errors = []
    corrected = query.strip()
    if not corrected:
        return "", ["Empty query"]

    # SQL keywords for fuzzy matching
    KEYWORDS = {
        'select', 'from', 'where', 'insert', 'update', 'delete',
        'join', 'inner', 'left', 'right', 'full', 'outer',
        'group', 'by', 'order', 'values', 'set', 'into',
        'on', 'and', 'or', 'not', 'exists', 'in', 'between',
        'like', 'limit', 'offset', 'having', 'as', 'union',
        'all', 'distinct', 'case', 'when', 'then', 'end', 'else',
        'asc', 'desc', 'is', 'null', 'if', 'for', 'primary', 'key',
        'foreign', 'constraint', 'default', 'unique', 'create',
        'table', 'drop', 'alter', 'add'
    }
    # Prepare lower-case mappings of tables and fields
    tables = {table.lower(): table for table in schema.keys()}
    fields = {}
    for table, cols in schema.items():
        for col in cols:
            fields.setdefault(col.lower(), []).append(table.lower())

    # Helper to replace a whole word (case-insensitive) in the query
    def re_replace_word(text, word, replacement):
        pattern = re.compile(r'\b{}\b'.format(re.escape(word)), flags=re.IGNORECASE)
        return pattern.sub(replacement, text)

    # 1. Fix mistyped keywords (using difflib fuzzy match)
    tokens = re.findall(r"[A-Za-z_]+", corrected)
    for token in tokens:
        tl = token.lower()
        # Skip if already a keyword or known identifier
        if tl in KEYWORDS or tl in tables or tl in fields:
            continue
        # Skip if token has uppercase (treat as name or alias, e.g. 'Das')
        if token != token.lower():
            continue
        match = difflib.get_close_matches(tl, KEYWORDS, n=1, cutoff=0.8)
        if match:
            correction = match[0].upper()
            if tl != match[0]:
                corrected = re_replace_word(corrected, token, correction)
                errors.append(f"Corrected keyword '{token}' to '{correction}'")

    # Normalize comma spacing
    corrected = re.sub(r',\s*', ', ', corrected)
    low = corrected.lower()

    # 2. Fix table names after FROM clause (fuzzy match using context)
    pos_from = low.find(" from ")
    if pos_from != -1:
        end_pos = len(corrected)
        for clause in [" where ", " group by ", " order by ", " having ", " limit ", ";"]:
            idx = low.find(clause, pos_from+6)
            if idx != -1:
                end_pos = min(end_pos, idx)
        tables_clause = corrected[pos_from+6:end_pos]
        tables_clause = re.split(r'\bjoin\b', tables_clause, flags=re.IGNORECASE)[0]
        raw_tables = [t.strip() for t in tables_clause.split(',') if t.strip()]
        for tbl in raw_tables:
            name = tbl.split()[0].split('.')[-1]
            tl = name.lower()
            if tl and tl not in tables:
                possible = difflib.get_close_matches(tl, list(tables.keys()), n=1, cutoff=0.7)
                if possible:
                    correct_name = tables[possible[0]]
                    corrected = re_replace_word(corrected, name, correct_name)
                    errors.append(f"Corrected table '{name}' to '{correct_name}'")

    # 2.5 Fix missing commas in IN(...) clause values
    def repl_in(match):
        inner = match.group(1)
        # Split on single quotes to capture values, trim whitespace
        parts = [x.strip() for x in inner.split("'") if x.strip()]
        if len(parts) > 1 and ',' not in inner:
            return "IN(" + ",".join(f"'{p}'" for p in parts) + ")"
        return match.group(0)
    new_corrected = re.sub(r"(?i)IN\s*\(([^)]+)\)", repl_in, corrected)
    if new_corrected != corrected:
        corrected = new_corrected
        errors.append("Inserted missing comma in IN clause")

    # 3. Build set of valid columns (context from tables if one table is used)
    tables_in_query = []
    low = corrected.lower()
    pos_from = low.find(" from ")
    if pos_from != -1:
        end_pos = len(corrected)
        for clause in [" where ", " group by ", " order by ", " having ", " limit ", ";"]:
            idx = low.find(clause, pos_from+6)
            if idx != -1:
                end_pos = min(end_pos, idx)
        tables_clause = corrected[pos_from+6:end_pos]
        raw_tables = [t.strip().split()[0].split('.')[-1] for t in tables_clause.split(',') if t.strip()]
        tables_in_query = [t for t in raw_tables if t]
    context_columns = set()
    if len(tables_in_query) == 1:
        tbl = tables_in_query[0].lower()
        if tbl in tables:
            context_columns = {c.lower() for c in schema[tables[tbl]]}
    if not context_columns:
        context_columns = set(fields.keys())

    # 4. Fix column names in SELECT clause (fuzzy match against context)
    if pos_from != -1:
        select_clause = corrected[:pos_from]
        select_content = re.sub(r'(?i)^select\s+', '', select_clause, count=1)
        select_items = [s.strip() for s in select_content.split(',')]
        for item in select_items:
            if not item:
                continue
            tokens_item = re.split(r'\s+as\s+|\s+', item, flags=re.IGNORECASE)
            col_expr = tokens_item[0]
            if col_expr.lower() == '*':
                continue
            col = col_expr.split('.',1)[-1]  # handle table.column
            col_lower = col.lower()
            if col_lower and col_lower not in context_columns:
                match = difflib.get_close_matches(col_lower, list(context_columns), n=1, cutoff=0.8)
                if match:
                    correct_col = match[0]
                    corrected = re_replace_word(corrected, col, correct_col)
                    errors.append(f"Corrected column '{col}' to '{correct_col}'")

    # 5. Quote unquoted WHERE values and unquote numeric literals
    pos_where = low.find(" where ")
    if pos_where != -1:
        where_clause = corrected[pos_where+7:]
        # Add quotes around unquoted strings
        def quote_match(match):
            col = match.group(1)
            val = match.group(2)
            # If value is numeric, leave unquoted
            if re.fullmatch(r"\d+(\.\d+)?", val):
                return f"{col} = {val}"
            # If already quoted, leave as is
            if val.startswith("'") or val.startswith('"'):
                return match.group(0)
            # Otherwise quote the value
            return f"{col} = '{val}'"
        new_where, count = re.subn(r"(\b\w+\b)\s*=\s*([^'\"\s][\w]*)", quote_match, where_clause)
        # Remove quotes around pure numeric strings (e.g. '123' -> 123)
        def unquote_numeric(match):
            col = match.group(1)
            val = match.group(2)
            return f"{col} = {val}"
        new_where2, count_num = re.subn(r"(\b\w+\b)\s*=\s*'(\d+(\.\d+)?)'", unquote_numeric, new_where)
        # Apply fixes to the corrected query
        if "'" in new_where and "'" not in where_clause:
            corrected = corrected[:pos_where+7] + new_where
            errors.append("Added missing quotes around value in WHERE")
        else:
            if new_where2 != new_where:
                corrected = corrected[:pos_where+7] + new_where2
                errors.append("Removed quotes around numeric value")
            elif new_where != where_clause:
                corrected = corrected[:pos_where+7] + new_where

    # 6. Insert missing commas in SELECT list (simple heuristic)
    if pos_from != -1:
        select_clause = corrected[:pos_from]
        select_content = re.sub(r'(?i)^select\s+', '', select_clause, count=1)
        parts = [p.strip() for p in select_content.split(',')]
        for part in parts:
            tokens_part = part.split()
            if len(tokens_part) >= 2:
                # If first two tokens are both column names, insert comma
                if all(tok.lower() in context_columns for tok in tokens_part[:2]):
                    a, b = tokens_part[0], tokens_part[1]
                    corrected = re.sub(rf"({a})\s+({b})", rf"\1, \2", corrected, flags=re.IGNORECASE)
                    errors.append(f"Inserted missing comma between '{a}' and '{b}' in SELECT")

    # 6.5 Fix unmatched quotes in LIKE clause (add a closing quote before AND/OR)
    like_pattern = re.compile(r"(?i)(LIKE\s*')([^']*?)(\s+(?:and|or)\b)")
    if like_pattern.search(corrected):
        corrected = like_pattern.sub(r"\1\2'\3", corrected)
        errors.append("Added missing quote in LIKE clause")

    # 7. Balance single quotes (if still odd number of quotes)
    if corrected.count("'") % 2 != 0:
        sem_index = corrected.rfind(';')
        if sem_index != -1:
            corrected = corrected[:sem_index] + "'" + corrected[sem_index:]
        else:
            corrected = corrected + "'"
        errors.append("Balanced unmatched single quote")

    # 8. Balance parentheses (if more '(' than ')')
    open_parens = corrected.count("(")
    close_parens = corrected.count(")")
    if open_parens > close_parens:
        needed = open_parens - close_parens
        sem_index = corrected.rfind(';')
        addition = ")" * needed
        if sem_index != -1:
            corrected = corrected[:sem_index] + addition + corrected[sem_index:]
        else:
            corrected = corrected + addition
        errors.append("Balanced unmatched parenthesis")

    # 9. Ensure exactly one semicolon at end
    if ';' in corrected:
        if corrected.count(';') > 1:
            corrected = corrected.replace(';', '')
            errors.append("Removed extra semicolons")
        if not corrected.strip().endswith(';'):
            corrected = corrected.rstrip(';').strip() + ';'
            errors.append("Moved semicolon to end")
    else:
        corrected = corrected.rstrip() + ';'
        errors.append("Added missing semicolon")

    return corrected, errors

# ------------------------
# Demonstration of Fixes
# ------------------------

# Example schema for demonstration (table -> columns)
database_schema = {
    'employees': ['id', 'name', 'age']
}

# User-provided test queries to check
test_queries = [
    "select s_name s_email from studennt where s_name = 'Bibhas'",
    "select s_name from student where s_name = Bibhas and s_id = '123'",
    "select s_name from student where s_name = 'Bibhas''",
    "select s_name s_email from studennt where s_name = (sellect s_name fromm student where s_city = Kolkatta",
    "select s_name from student where s_name = 'A_VERY_LONG_NAME_EXCEEDING_100_CHARACTERS_ABCDEFGHIJKLMNOPQRSTUVWXYZ_ABCDEFGHIJKLMNOPQRSTUVWXYZ_1234567890'",
    "select s_id, s_name from student where s_id = 102",
    "selct s_name s_city from student wheer s_city = kolkata;",
    "select s_name s_email s_id from student",
    "select s_name from student;;;",
    "select s_name from student where s_name in('Bibhas 'Gragi')",
    "select s_name from student where s_name in('Bibhas Das 'Gragi')",
    "select * from student where s_name like 'Bibh% and s_id like '%_5"
]

for query in test_queries:
    print(f"Enter query: {query}")
    corrected, fixes = checkSyntax(query, database_schema)
    print(f"Corrected: {corrected}")
    print(f"Fixes: {fixes}")
    print()
