#It is few corrected
import difflib
import re

def checkSyntax(query, schema):
    """
    Check and correct common SQL syntax errors in the given query using the 
    provided database schema.

    :param query: The SQL query string to check.
    :param schema: Dict mapping table names to list of column names (strings) 
                   or to column definitions (with data types).
    :return: (corrected_query, errors) where errors is a list of strings 
             describing fixes applied.
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
        for col in (cols.keys() if isinstance(cols, dict) else cols):
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
            context_columns = {c.lower() for c in schema[tables[tbl]].keys()} if isinstance(schema[tables[tbl]], dict) else {c.lower() for c in schema[tables[tbl]]}
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

    # 5. Fix quoting of values in WHERE and similar clauses based on column data type
    low = corrected.lower()
    pattern = re.compile(r"(\b(?:\w+\.)?\w+\b)\s*(=|<>|!=|<=|>=|<|>)\s*('[^']*'|\"[^\"]*\"|[^'\s][^,;\)\s]*)", re.IGNORECASE)
    def replace_value(match):
        col = match.group(1)
        op = match.group(2)
        val = match.group(3)
        # Skip subqueries or functions (value starting with parenthesis)
        if val.startswith("(") or "(" in val:
            return match.group(0)
        # Determine table and column name
        if "." in col:
            prefix, col_name = col.split(".", 1)
            col_name_lower = col_name.lower()
            prefix_lower = prefix.lower()
            table_name = None
            for t in tables_in_query:
                if t.lower() == prefix_lower:
                    table_name = t
                    break
            if table_name is None:
                return match.group(0)
        else:
            col_name_lower = col.lower()
            if len(tables_in_query) == 1:
                table_name = tables_in_query[0]
            else:
                table_name = None
                for t in tables_in_query:
                    col_names = schema[t].keys() if isinstance(schema.get(t), dict) else schema.get(t, [])
                    if any(c.lower() == col_name_lower for c in col_names):
                        if table_name is None:
                            table_name = t
                        else:
                            table_name = None
                            break
                if table_name is None:
                    return match.group(0)
        # Determine column type if available
        field_type = None
        if isinstance(schema.get(table_name), dict):
            for c_key, c_val in schema[table_name].items():
                if c_key.lower() == col_name_lower:
                    field_type = c_val[0] if isinstance(c_val, (list, tuple)) else c_val
                    break
        # Classify type
        numeric_types = {'int','bigint','smallint','tinyint','decimal','numeric','float','double','real','bit','serial'}
        string_types = {'char','varchar','text','tinytext','mediumtext','longtext','date','datetime','timestamp','time','year','enum','set'}
        numeric_type = False
        string_type = False
        max_len = None
        if field_type:
            ft = field_type.lower()
            base = ft.split('(')[0]
            if base in numeric_types:
                numeric_type = True
            if base in string_types:
                string_type = True
                if "(" in ft and ")" in ft:
                    num = ft[ft.find('(')+1:ft.rfind(')')]
                    try:
                        max_len = int(num.split(',')[0])
                    except:
                        max_len = None
        # Get raw value without quotes
        raw_val = val
        if (raw_val.startswith("'") and raw_val.endswith("'")) or (raw_val.startswith('"') and raw_val.endswith('"')):
            raw_val = raw_val[1:-1]
        new_val = val
        if string_type:
            if max_len is not None and len(raw_val) > max_len:
                errors.append(f"Truncated '{raw_val}' to '{raw_val[:max_len]}' for field '{col}' (max length {max_len})")
                raw_val = raw_val[:max_len]
            new_val = f"'{raw_val}'"
        elif numeric_type:
            # If numeric and quoted, remove quotes
            if re.fullmatch(r"\d+(\.\d+)?", raw_val):
                if val.startswith("'") or val.startswith('"'):
                    new_val = raw_val
                    errors.append(f"Removed quotes from numeric value '{raw_val}' for field '{col}'")
                else:
                    new_val = val
            else:
                new_val = val
        else:
            # Unknown type: do basic numeric check
            if re.fullmatch(r"\d+(\.\d+)?", raw_val):
                if val.startswith("'") or val.startswith('"'):
                    new_val = raw_val
                    errors.append(f"Removed quotes from numeric-like value '{raw_val}' for field '{col}'")
                else:
                    new_val = val
            else:
                # Treat as string if not numeric
                if not (val.startswith("'") or val.startswith('"')):
                    new_val = f"'{raw_val}'"
                else:
                    new_val = f"'{raw_val}'"
        return f"{col} {op} {new_val}"
    corrected, _ = re.subn(pattern, replace_value, corrected)

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

    # 7. Balance single quotes (add closing quote if unmatched)
    if corrected.count("'") % 2 != 0:
        sem_index = corrected.rfind(';')
        if sem_index != -1:
            corrected = corrected[:sem_index] + "'" + corrected[sem_index:]
        else:
            corrected = corrected + "'"
        errors.append("Balanced unmatched single quote")

    # 8. Balance parentheses (add missing closing parenthesis at end)
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
dobj = serverConnect()  # It should be first
schema = dobj.fetch_database_structure()  # It should be second


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
    "select * from student where s_name like 'Bibh% and s_id like '%_5"
    ]

for query in test_queries:
    corrected_query, fixes = checkSyntax(query, schema)
    print("Original:", query)
    print("Corrected:", corrected_query)
    print("Fixes:", fixes)
    print("-" * 50)