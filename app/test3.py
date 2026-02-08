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

    # Define SQL keywords for typo-checking
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
    # Prepare lowercase mappings of tables and fields
    tables = {table.lower(): table for table in schema.keys()}
    fields = {}
    for table, cols in schema.items():
        for col in cols:
            fields.setdefault(col.lower(), []).append(table.lower())

    # Helper to replace a whole word (case-insensitive) in the query
    def re_replace_word(text, word, replacement):
        pattern = re.compile(r'\b{}\b'.format(re.escape(word)), flags=re.IGNORECASE)
        return pattern.sub(replacement, text)

    # 1. Fix mistyped keywords (using difflib fuzzy match):contentReference[oaicite:3]{index=3}
    tokens = re.findall(r"[A-Za-z_]+", corrected)
    for token in tokens:
        tl = token.lower()
        # Skip if already a keyword or known identifier
        if tl in KEYWORDS or tl in tables or tl in fields:
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

    # 2. Fix table names after FROM clause
    table_list = []
    pos_from = low.find(" from ")
    if pos_from != -1:
        end_pos = len(corrected)
        for clause in [" where ", " group by ", " order by ", " having ", " limit ", ";"]:
            idx = low.find(clause, pos_from + 6)
            if idx != -1:
                end_pos = min(end_pos, idx)
        tables_clause = corrected[pos_from+6:end_pos]
        tables_clause = re.split(r'\bjoin\b', tables_clause, flags=re.IGNORECASE)[0]
        raw_tables = [t.strip() for t in tables_clause.split(',') if t.strip()]
        for tbl in raw_tables:
            name = tbl.split()[0].split('.')[-1]
            table_list.append(name)
        for tbl in table_list:
            tl = tbl.lower()
            if tl and tl not in tables:
                possible = difflib.get_close_matches(tl, list(tables.keys()), n=1, cutoff=0.7)
                if possible:
                    correct_name = tables[possible[0]]
                    corrected = re_replace_word(corrected, tbl, correct_name)
                    errors.append(f"Corrected table '{tbl}' to '{correct_name}'")
                    table_list = [correct_name if x == tbl else x for x in table_list]

    # 3. Build set of valid columns (context from tables)
    tables_in_query = []
    low = corrected.lower()
    pos_from = low.find(" from ")
    if pos_from != -1:
        end_pos = len(corrected)
        for clause in [" where ", " group by ", " order by ", " having ", " limit ", ";"]:
            idx = low.find(clause, pos_from + 6)
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

    # 4. Fix column names in SELECT clause (fuzzy match against context):contentReference[oaicite:4]{index=4}
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
            if '.' in col_expr:
                _, col = col_expr.split('.', 1)
            else:
                col = col_expr
            col_lower = col.lower()
            if col_lower and col_lower not in context_columns:
                match = difflib.get_close_matches(col_lower, list(context_columns), n=1, cutoff=0.8)
                if match:
                    correct_col = match[0]
                    corrected = re_replace_word(corrected, col, correct_col)
                    errors.append(f"Corrected column '{col}' to '{correct_col}'")

    # 5. Quote unquoted WHERE values (basic check: non-numeric strings):contentReference[oaicite:5]{index=5}
    pos_where = low.find(" where ")
    if pos_where != -1:
        where_clause = corrected[pos_where+7:]
        def quote_match(match):
            col = match.group(1)
            val = match.group(2)
            # Numeric check
            if re.fullmatch(r"\d+(\.\d+)?", val):
                return f"{col} = {val}"
            # Already quoted?
            if val.startswith("'") or val.startswith('"'):
                return match.group(0)
            return f"{col} = '{val}'"
        new_where, count = re.subn(r"(\b\w+\b)\s*=\s*([^'\"\s][\w]*)", quote_match, where_clause)
        # Insert only if quotes were added
        if "'" in new_where and "'" not in where_clause:
            corrected = corrected[:pos_where+7] + new_where
            errors.append("Added missing quotes around value in WHERE")
        else:
            # Update spacing if only formatting changed
            if new_where != where_clause:
                corrected = corrected[:pos_where+7] + new_where

    # 6. Insert missing commas in SELECT list (simple check)
    if pos_from != -1:
        select_clause = corrected[:pos_from]
        select_content = re.sub(r'(?i)^select\s+', '', select_clause, count=1)
        parts = [p.strip() for p in select_content.split(',')]
        for part in parts:
            tokens_part = part.split()
            if len(tokens_part) >= 2:
                if all(tok.lower() in context_columns for tok in tokens_part[:2]):
                    a, b = tokens_part[0], tokens_part[1]
                    corrected = re.sub(rf"({a})\s+({b})", rf"\1, \2", corrected, flags=re.IGNORECASE)
                    errors.append(f"Inserted missing comma between '{a}' and '{b}' in SELECT")

    # 7. Balance single quotes (add closing quote if unmatched):contentReference[oaicite:6]{index=6}
    if corrected.count("'") % 2 != 0:
        sem_index = corrected.rfind(';')
        if sem_index != -1:
            corrected = corrected[:sem_index] + "'" + corrected[sem_index:]
        else:
            corrected = corrected + "'"
        errors.append("Balanced unmatched single quote")

    # 8. Balance parentheses (add missing closing parenthesis at end):contentReference[oaicite:7]{index=7}
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




from serverConnect import serverConnect
dobj=serverConnect() #It should be first
database_schema = dobj.fetch_database_structure() #It should be second
print(database_schema)
corrected,fixes = checkSyntax(input("ENter queryL : "),database_schema)    


print(corrected,"  ",fixes)