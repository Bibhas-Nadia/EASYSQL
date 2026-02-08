import difflib
import re

def checkSyntax(query, schema):
    """
    Check and correct common SQL syntax errors in the given query using the 
    provided database schema.
    :param query: The SQL query string to check.
    :param schema: Dict mapping table names to dict of column details (list of strings).
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

    # 1. Fix mistyped keywords (using difflib fuzzy match, skip capitalized proper nouns)
    tokens = re.findall(r"[A-Za-z_]+", corrected)
    for token in tokens:
        tl = token.lower()
        # Skip if already a keyword or known identifier
        if tl in KEYWORDS or tl in tables or tl in fields:
            continue
        # Skip proper names (capitalized words)
        if token[0].isupper() and (len(token) == 1 or token[1:].islower()):
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

    # 2. Fix table names after FROM and JOIN clauses
    table_list = []
    pos_from = low.find(" from ")
    if pos_from != -1:
        end_pos = len(corrected)
        for clause in [" where ", " group by ", " order by ", " having ", " limit ", ";"]:
            idx = low.find(clause, pos_from + 6)
            if idx != -1:
                end_pos = min(end_pos, idx)
        tables_clause = corrected[pos_from+6:end_pos]
        parts = [t.strip() for t in tables_clause.split(',') if t.strip()]
        for part in parts:
            name = part.split()[0].split('.')[-1]
            table_list.append(name)
        # Also check JOIN clauses
        for match in re.finditer(r'\bjoin\s+([A-Za-z_][\w]*)', corrected, flags=re.IGNORECASE):
            table_list.append(match.group(1))
        for tbl in table_list:
            tl = tbl.lower()
            if tl and tl not in tables:
                possible = difflib.get_close_matches(tl, list(tables.keys()), n=1, cutoff=0.7)
                if possible:
                    correct_name = tables[possible[0]]
                    corrected = re_replace_word(corrected, tbl, correct_name)
                    errors.append(f"Corrected table '{tbl}' to '{correct_name}'")
                    table_list = [correct_name if x == tbl else x for x in table_list]

    # 3. Build set of valid columns based on context tables
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

    # 4. Fix column names in SELECT clause (fuzzy match against context columns)
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

    # 4b. Fix column names in WHERE and other clauses (fuzzy match)
    pos_where = corrected.lower().find(" where ")
    if pos_where != -1:
        where_clause = corrected[pos_where+7:]
        col_patterns = [r"(\b\w+\b)\s*=", r"(\b\w+\b)\s+like", r"(\b\w+\b)\s+in", r"(\b\w+\b)\s*[<>]"]
        for pat in col_patterns:
            for match in re.finditer(pat, where_clause, flags=re.IGNORECASE):
                col_expr = match.group(1)
                if '.' in col_expr:
                    _, col = col_expr.split('.', 1)
                else:
                    col = col_expr
                col_lower = col.lower()
                if col_lower and col_lower not in context_columns:
                    match_col = difflib.get_close_matches(col_lower, list(context_columns), n=1, cutoff=0.8)
                    if match_col:
                        correct_col = match_col[0]
                        corrected = re_replace_word(corrected, col, correct_col)
                        errors.append(f"Corrected column '{col}' to '{correct_col}'")

        # 5. Quote unquoted WHERE string values; unquote numeric values
        def quote_match(match):
            col = match.group(1)
            val = match.group(2)
            if re.fullmatch(r"\d+(\.\d+)?", val):
                return f"{col} = {val}"
            if val.startswith("'") or val.startswith('"'):
                return match.group(0)
            return f"{col} = '{val}'"
        new_where, count = re.subn(r"(\b\w+\b)\s*=\s*([^'\"\s][\w%]*)", quote_match, where_clause, flags=re.IGNORECASE)
        if new_where != where_clause:
            if "'" in new_where and "'" not in where_clause:
                errors.append("Added missing quotes around value in WHERE")
            corrected = corrected[:pos_where+7] + new_where

        new_where2, count2 = re.subn(r"(\b\w+\b)\s*=\s*'(\d+(\.\d+)?)'", 
                                     lambda m: f"{m.group(1)} = {m.group(2)}", 
                                     corrected[pos_where+7:], flags=re.IGNORECASE)
        if count2 > 0:
            corrected = corrected[:pos_where+7] + new_where2
            errors.append("Unquoted numeric value in WHERE")

        where_clause = corrected[pos_where+7:]
        # 5b. Truncate string values exceeding column length
        tbl = tables_in_query[0].lower() if len(tables_in_query) == 1 else None
        for match in re.finditer(r"(\b\w+\b)\s*=\s*'([^']*)'", where_clause):
            col = match.group(1)
            val = match.group(2)
            col_lower = col.split('.')[-1].lower()
            col_info = None
            if tbl and tbl in tables:
                col_info = schema[tables[tbl]].get(col_lower)
            if col_info and col_info[0].lower().startswith("varchar"):
                m_len = re.search(r'varchar\((\d+)\)', col_info[0].lower())
                if m_len:
                    maxlen = int(m_len.group(1))
                    if len(val) > maxlen:
                        new_val = val[:maxlen]
                        corrected = corrected.replace(f"'{val}'", f"'{new_val}'")
                        errors.append(f"Truncated value for column '{col}' to {maxlen} characters")
        # 5c. Fix LIKE clause quote mismatches (e.g., missing closing quote before AND/OR)
        new_where3 = re.sub(r"(?i)(like\s*')([^']*)(\s+(and|or)\b)",
                            lambda m: m.group(1) + m.group(2) + "'" + m.group(3),
                            corrected[pos_where+7:])
        if new_where3 != corrected[pos_where+7:]:
            corrected = corrected[:pos_where+7] + new_where3
            errors.append("Fixed LIKE clause quote mismatch")
        # 5d. Fix malformed IN clauses (insert missing commas between values)
        def fix_in(match):
            inner = match.group(1)
            fixed_inner = re.sub(r"'([^']*) '([^']*)'", r"'\1', '\2'", inner)
            if fixed_inner != inner:
                return "IN(" + fixed_inner + ")"
            return match.group(0)
        corrected_before = corrected
        corrected = re.sub(r"(?i)IN\s*\(\s*([^)]*)\)", fix_in, corrected)
        if corrected != corrected_before:
            errors.append("Fixed malformed IN clause")

    # 6. Insert missing commas in SELECT list (simple check)
    if pos_from != -1:
        select_clause = corrected[:pos_from]
        select_content = re.sub(r'(?i)^select\s+', '', select_clause, count=1)
        parts = [p.strip() for p in select_content.split(',')]
        for part in parts:
            tokens_part = part.split()
            if len(tokens_part) >= 2:
                a, b = tokens_part[0], tokens_part[1]
                if a.lower() in context_columns and b.lower() in context_columns:
                    corrected = re.sub(rf"({a})\s+({b})", r"\1, \2", corrected, flags=re.IGNORECASE)
                    errors.append(f"Inserted missing comma between '{a}' and '{b}' in SELECT")

    # 7. Balance single quotes (add closing quote if unmatched)
    if corrected.count("'") % 2 != 0:
        sem_index = corrected.rfind(';')
        if sem_index != -1:
            corrected = corrected[:sem_index] + "'" + corrected[sem_index:]
        else:
            corrected = corrected + "'"
        errors.append("Balanced unmatched single quote")

    # 8. Balance parentheses (add missing closing parenthesis)
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

# --- Test block with sample queries and mock schema ---
if __name__ == "__main__":
    schema = {
      "college": {"c_id": ["int(11)", "NO", "PRI", ""], 
                  "c_name": ["varchar(100)", "NO", "UNI", ""], 
                  "c_city": ["varchar(100)", "NO", "", ""], 
                  "c_state": ["varchar(100)", "NO", "", ""]},
      "department": {"d_id": ["int(11)", "NO", "PRI", ""], 
                     "d_name": ["varchar(100)", "NO", "", ""], 
                     "d_college_name": ["varchar(100)", "NO", "", ""]},
      "student": {"s_id": ["int(11)", "NO", "PRI", ""], 
                  "s_name": ["varchar(100)", "NO", "", ""], 
                  "s_email": ["varchar(100)", "NO", "", ""], 
                  "s_age": ["int(11)", "YES", "", ""], 
                  "s_city": ["varchar(100)", "YES", "", ""], 
                  "s_college_name": ["varchar(100)", "NO", "", ""]},
      "teacher": {"t_id": ["int(11)", "NO", "PRI", ""], 
                  "t_name": ["varchar(100)", "NO", "", ""], 
                  "t_email": ["varchar(100)", "NO", "", ""], 
                  "t_age": ["int(11)", "YES", "", ""], 
                  "t_city": ["varchar(100)", "YES", "", ""], 
                  "t_college_name": ["varchar(100)", "NO", "", ""]}
    }

    from serverConnect import serverConnect
    dobj = serverConnect()  # It should be first
    schema = dobj.fetch_database_structure()  # It should be second

    test_queries = [
        "SELEC * FRM college WHERE c_name = Das",
        "SELECT s_nam FROM studen WHERE s_age = '21'",
        "SELECT t_name, t_cityt FROM techer",
        "SELECT * FROM depatment",
        "SELECT * FROM college WHERE c_city IN('Bibhas 'Gragi')",
        "SELECT s_email FROM student WHERE s_name LIKE 'Bibh% and s_age>20",
        "SELECT * FROM student WHERE (s_age = 30",
        "SELECT c_name c_city FROM college"
    ]

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
        corrected_query, fixes = checkSyntax(query, schema)
        print("Original:", query)
        print("Corrected:", corrected_query)
        print("Fixes:", fixes)
        print("-" * 50)
