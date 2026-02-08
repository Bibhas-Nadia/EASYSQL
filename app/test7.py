# import difflib
# import re

# SQL_KEYWORDS = {
#     "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
#     "UPDATE", "SET", "DELETE", "JOIN", "GROUP", "BY", "ORDER",
#     "HAVING", "CREATE", "TABLE", "DROP", "ALTER", "AS", "AND",
#     "OR", "IN", "NOT", "NULL", "DISTINCT", "LIMIT"
# }

# def detectSyntaxErrors(query: str, table_names: list, field_names: list):
#     """
#     Detects and returns ALL syntax error tags in 'query'.
#     Does NOT modify the query.
#     """
#     errors = []
#     q = query.strip()

#     # Build set of valid tokens = keywords + schema identifiers
#     valid = set(SQL_KEYWORDS)
#     valid |= {t.upper() for t in table_names}
#     valid |= {f.upper() for f in field_names}

#     # 1) Keyword / identifier checks
#     for tok in q.split():
#         up = tok.upper()
#         if up not in valid:
#             # typo of keyword?
#             if difflib.get_close_matches(up, SQL_KEYWORDS, n=1, cutoff=0.8):
#                 errors.append("wrong_keyword")
#             else:
#                 errors.append("unknown_identifier")

#     # 2) Semicolon at end
#     if not q.endswith(";"):
#         errors.append("semicolon_missing")

#     # 3) Parenthesis balance
#     o, c = q.count("("), q.count(")")
#     if o > c:
#         errors.append("missing_closing_bracket")
#     elif c > o:
#         errors.append("extra_closing_bracket")

#     # 4) Unmatched quotes
#     if q.count("'") % 2 != 0 or q.count('"') % 2 != 0:
#         errors.append("quote_unbalanced")

#     # 5) Comma issues in SELECT list
#     select_match = re.search(r"SELECT\s+(.*?)\s+FROM", q, re.IGNORECASE)
#     if select_match:
#         cols = select_match.group(1)
#         if re.search(r"\b\w+\s+\w+\b", cols) and "," not in cols:
#             errors.append("comma_missing")
#         if re.search(r",\s*$", cols):
#             errors.append("extra_comma")

#     # 6) Operator missing in WHERE clause
#     where_match = re.search(r"WHERE\s+(.*?)(?:;|$)", q, re.IGNORECASE)
#     if where_match:
#         cond = where_match.group(1)
#         # field followed by literal without operator
#         if re.search(rf"\b({'|'.join(f.upper() for f in field_names)})\s+(?:'[^']*'|\d)", cond, re.IGNORECASE):
#             errors.append("operator_missing")

#     return list(set(errors)) or ["no_error"]


# def correctSyntax(query: str, table_names: list, field_names: list):
#     """
#     Applies corrections for detected errors and returns:
#       (corrected_query, [error tags])
#     """
#     errors = []
#     valid = set(SQL_KEYWORDS)
#     valid |= {t.upper() for t in table_names}
#     valid |= {f.upper() for f in field_names}

#     parts = []
#     # 1) Fix keyword typos & leave identifiers intact
#     for tok in query.strip().split():
#         up = tok.upper()
#         if up in SQL_KEYWORDS:
#             parts.append(up)
#         elif up not in valid:
#             match = difflib.get_close_matches(up, SQL_KEYWORDS, n=1, cutoff=0.8)
#             if match:
#                 parts.append(match[0])
#                 errors.append("wrong_keyword")
#             else:
#                 parts.append(tok)
#                 errors.append("unknown_identifier")
#         else:
#             parts.append(tok)

#     fixed = " ".join(parts)

#     # 2) Balance parentheses
#     o, c = fixed.count("("), fixed.count(")")
#     if o > c:
#         fixed += ")" * (o - c)
#         errors.append("missing_closing_bracket")
#     elif c > o:
#         fixed = fixed.rstrip(")").rstrip()
#         errors.append("extra_closing_bracket")

#     # 3) Close quotes if unbalanced
#     if fixed.count("'") % 2 != 0:
#         fixed += "'"
#         errors.append("quote_unbalanced")
#     if fixed.count('"') % 2 != 0:
#         fixed += '"'
#         errors.append("quote_unbalanced")

#     # 4) Fix commas in SELECT list (add missing comma between fields)
#     def fix_commas(match):
#         cols = match.group(1)
#         # insert commas between words if none
#         cols_fixed = re.sub(r"\b(\w+)\s+(\w+)\b", r"\1, \2", cols)
#         return f"SELECT {cols_fixed} FROM"

#     fixed = re.sub(r"SELECT\s+(.*?)\s+FROM", fix_commas, fixed, flags=re.IGNORECASE)

#     # 5) Add missing semicolon
#     if not fixed.strip().endswith(";"):
#        fixed = fixed.strip() + ";"
#        errors.append("semicolon_missing")

#     return fixed, list(set(errors)) or ["no_error"]


# def checkSyntax(raw_query:str,database_schema:dict[str, dict[str, list[str]]])->str:
#     tables=[]
#     fields=[]
#     for table,desc in database_schema.items():
#        #print(f"\n{table}: {desc.keys()}")
#         tables.append(table)
#         fields.extend(desc.keys())
    
#     print(tables)
#     print(fields)

#     detected = detectSyntaxErrors(raw_query, tables, fields)
#     print("Detected Errors:", detected)
#     corrected_query, applied = correctSyntax(raw_query, tables, fields)
#     print("Corrected Query:", corrected_query,"Corrections Applied:", applied)
#     return corrected_query

import difflib
import re

SQL_KEYWORDS = {
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
    "UPDATE", "SET", "DELETE", "JOIN", "GROUP", "BY", "ORDER",
    "HAVING", "CREATE", "TABLE", "DROP", "ALTER", "AS", "AND",
    "OR", "IN", "NOT", "NULL", "DISTINCT", "LIMIT"
}

def detectSyntaxErrors(query: str, table_names: list, field_names: list):
    errors = []
    q = query.strip().upper()
    valid = set(SQL_KEYWORDS) | {t.upper() for t in table_names} | {f.upper() for f in field_names}

    # 1) Keyword/identifier checks
    for tok in re.findall(r"\b\w+\b", q):
        if tok not in valid:
            if difflib.get_close_matches(tok, SQL_KEYWORDS, n=1, cutoff=0.8):
                errors.append("wrong_keyword")
            else:
                errors.append("unknown_identifier")

    # 2) Semicolon check
    if not q.endswith(";"):
        errors.append("semicolon_missing")

    # 3) Parenthesis balance
    o, c = q.count("("), q.count(")")
    if o > c:
        errors.append("missing_closing_bracket")
    elif c > o:
        errors.append("extra_closing_bracket")

    # 4) Quote balance
    if q.count("'") % 2 != 0 or q.count('"') % 2 != 0:
        errors.append("quote_unbalanced")

    # 5) Comma issues in SELECT
    select_match = re.search(r"SELECT\s+(.*?)\s+FROM", q, re.IGNORECASE)
    if select_match:
        cols = select_match.group(1)
        if re.search(r"\b\w+\s+\w+\b", cols) and "," not in cols:
            errors.append("comma_missing")
        if re.search(r",\s*$", cols):
            errors.append("extra_comma")

    return list(set(errors)) or ["no_error"]

def correctSyntax(query, table_names, field_names):
    errors = []
    valid = set(SQL_KEYWORDS) | {t.upper() for t in table_names} | {f.upper() for f in field_names}

    # Phase 1: Token normalization
    tokens = []
    for tok in query.strip().split():
        up = tok.upper()
        if up in SQL_KEYWORDS:
            tokens.append(up)
        elif up not in valid:
            closest = difflib.get_close_matches(up, SQL_KEYWORDS, n=1, cutoff=0.8)
            if closest:
                tokens.append(closest[0])
                errors.append("wrong_keyword")
            else:
                tokens.append(tok)
                errors.append("unknown_identifier")
        else:
            tokens.append(tok)
    fixed = " ".join(tokens)

    # Phase 2: SELECT comma correction
    def fix_select(match):
        cols = match.group(1)
        if "," not in cols and len(cols.split()) > 1:
            errors.append("comma_missing")
            return "SELECT " + ", ".join(cols.split()) + " FROM"
        return match.group(0)
    
    fixed = re.sub(r"SELECT\s+(.+?)\s+FROM", fix_select, fixed, flags=re.IGNORECASE)

    # Phase 3: Smart quote handling
    def fix_where_quotes(match):
        col, op, value = match.groups()
        quote = "'" if "'" in value else '"'
        
        # Count existing quotes
        quote_count = value.count(quote)
        
        if quote_count % 2 != 0:
            # Add missing closing quote
            corrected = value + quote
            errors.append("quote_unbalanced")
        elif not any(c in value for c in "'\""):
            # Add quotes if missing completely
            corrected = f"'{value}'"
            errors.append("quote_missing")
        else:
            corrected = value
            
        return f"{col} {op} {corrected}"

    # Handle WHERE clauses with string comparisons
    fixed = re.sub(
        r"WHERE\s+(\w+)\s*(=|<|>|LIKE)\s*((?:'[^']*'?|\"[^\"]*\"?|[\w%]+)+)",
        fix_where_quotes,
        fixed,
        flags=re.IGNORECASE
    )

    # Phase 4: Semicolon placement (AFTER quote fixes)
    if not fixed.endswith(";"):
        # Check if last character is a quote
        if fixed and fixed[-1] in ("'", '"'):
            # Add closing quote before semicolon
            fixed = fixed[:-1] + fixed[-1] + ";"
        else:
            fixed += ";"
        errors.append("semicolon_missing")

    # Final quote validation
    quote_stack = []
    for char in fixed:
        if char in ("'", '"'):
            if quote_stack and quote_stack[-1] == char:
                quote_stack.pop()
            else:
                quote_stack.append(char)
    if quote_stack:
        fixed += quote_stack[-1]
        errors.append("quote_unbalanced")

    return fixed, list(set(errors))

def checkSyntax(raw_query: str, database_schema: dict[str, dict[str, list[str]]]) -> str:
    tables = list(database_schema.keys())
    fields = [field for table in database_schema.values() for field in table.keys()]

    detected_errors = detectSyntaxErrors(raw_query, tables, fields)
    corrected_query, applied_corrections = correctSyntax(raw_query, tables, fields)

    print(f"Original query: {raw_query}")
    print(f"Detected errors: {detected_errors}")
    print(f"Applied corrections: {applied_corrections}")
    print(f"Corrected query: {corrected_query}")

    return corrected_query

# from serverConnect import serverConnect
# dobj=serverConnect() #It should be first
# database_schema = dobj.fetch_database_structure() #It should be second
# checkSyntax(input("ENter queryL : "),database_schema)  