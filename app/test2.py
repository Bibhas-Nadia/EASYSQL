# import difflib
# import re

# SQL_KEYWORDS = {
#     "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
#     "UPDATE", "SET", "DELETE", "JOIN", "GROUP", "BY", "ORDER",
#     "HAVING", "CREATE", "TABLE", "DROP", "ALTER", "AS", "AND",
#     "OR", "IN", "NOT", "NULL", "DISTINCT", "LIMIT"
# }

# def detectSyntaxErrors(query: str, table_names: list, field_names: list):
#     errors = []
#     q = query.strip().upper()
#     valid = set(SQL_KEYWORDS) | {t.upper() for t in table_names} | {f.upper() for f in field_names}

#     # 1) Keyword / identifier checks
#     for tok in q.split():
#         if tok not in valid:
#             if difflib.get_close_matches(tok, SQL_KEYWORDS, n=1, cutoff=0.8):
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
#         fldp = "|".join(re.escape(f.upper()) for f in field_names)
#         if re.search(rf"\b({fldp})\s+(?:'[^']*'|\d)", cond, re.IGNORECASE):
#             errors.append("operator_missing")

#     return list(set(errors)) or ["no_error"]


# def correctSyntax(query, table_names, field_names):
#     errors = []
#     valid = set(SQL_KEYWORDS) | {t.upper() for t in table_names} | {f.upper() for f in field_names}

#     # Phase 1: normalize every token
#     tokens = []
#     for tok in query.strip().split():
#         up = tok.upper()
#         if up in SQL_KEYWORDS:
#             tokens.append(up)
#         elif up not in valid:
#             # typo?
#             km = difflib.get_close_matches(up, SQL_KEYWORDS, n=1, cutoff=0.8)
#             if km:
#                 tokens.append(km[0])
#                 errors.append("wrong_keyword")
#             else:
#                 tokens.append(tok)
#                 errors.append("unknown_identifier")
#         else:
#             tokens.append(tok)
#     fixed = " ".join(tokens)

#     # Phase 2: insert commas in SELECT … FROM now that both SELECT and FROM are spelled correctly
#     '''
#     def comma_inserter(m):
#         fields = m.group(1).split()
#         if len(fields) > 1:
#             errors.append("comma_missing")
#             return "SELECT " + ", ".join(fields) + " FROM"
#         return m.group(0)
#     '''
#     def comma_inserter(m):
#         cols = m.group(1)
#         if "," not in cols and len(cols.split()) > 1:
#             errors.append("comma_missing")
#             return "SELECT " + ", ".join(cols.split()) + " FROM"
#         return m.group(0)

#     fixed = re.sub(r"SELECT\s+(.+?)\s+FROM",
#                    comma_inserter,
#                    fixed,
#                    flags=re.IGNORECASE)

#     # Phase 3: balance parens, quotes, split VALUES/WHERE, semicolon

#     # balance parentheses
#     o,c = fixed.count("("), fixed.count(")")
#     if o>c:
#         fixed += ")"*(o-c)
#         errors.append("missing_closing_bracket")
#     elif c>o:
#         fixed = fixed.rstrip(")")
#         errors.append("extra_closing_bracket")

#     # balance quotes
#     if fixed.count("'")%2:
#         fixed += "'"
#         errors.append("quote_unbalanced")
#     if fixed.count('"')%2:
#         fixed += '"'
#         errors.append("quote_unbalanced")

#     # protect inner WHERE inside VALUES(...)
#     def prot(m):
#         inner = m.group(1).replace(" WHERE ", " __KW_WH__ ")
#         return f"VALUES({inner})"
#     fixed = re.sub(r"VALUES\s*\(\s*(.*?)\s*\)", prot, fixed, flags=re.IGNORECASE)

#     # split outer WHERE
#     fixed = re.sub(r"\)\s*(WHERE)\b", r") \1", fixed, flags=re.IGNORECASE)

#     # restore inner
#     fixed = fixed.replace("__KW_WH__", " WHERE ")

#     # semicolon
#     if not fixed.strip().endswith(";"):
#         fixed += ";"
#         errors.append("semicolon_missing")

#     return fixed, list(set(errors))






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

    # 2) Semicolon at end
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

    # 6) Operator in WHERE clause
    where_match = re.search(r"WHERE\s+(.*?)(?:;|$)", q, re.IGNORECASE)
    if where_match:
        cond = where_match.group(1)
        if re.search(r"\b\w+\s*=\s*('[^']*'|\d+)", cond):
            errors.append("operator_missing")

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
    
    fixed = re.sub(
        r"SELECT\s+(.+?)\s+FROM",
        fix_select,
        fixed,
        flags=re.IGNORECASE
    )

    # Phase 3: Parenthesis balancing
    open_paren = fixed.count("(")
    close_paren = fixed.count(")")
    if open_paren > close_paren:
        fixed += ")" * (open_paren - close_paren)
        errors.append("missing_closing_bracket")
    elif close_paren > open_paren:
        fixed = re.sub(r"\)+$", ")", fixed)
        errors.append("extra_closing_bracket")

    # Phase 4: Intelligent quote handling
    def fix_quotes(match):
        value = match.group(2)
        quote = "'" if "'" in value else '"'
        
        if not any(c in value for c in ["'", '"']):
            errors.append("quote_missing")
            return f"{match.group(1)}'{value}'"
            
        if (value.count("'") % 2 != 0) or (value.count('"') % 2 != 0):
            errors.append("quote_unbalanced")
            return f"{match.group(1)}{value}{quote}"
            
        return match.group(0)

    fixed = re.sub(
        r"(=\s*)([^;]+?)(?=\s+(?:AND|OR|ORDER|GROUP|LIMIT|;|$))",
        fix_quotes,
        fixed,
        flags=re.IGNORECASE
    )

    # Phase 5: Semicolon termination
    if not fixed.endswith(";"):
        fixed = re.sub(r";?$", ";", fixed)
        errors.append("semicolon_missing")

    # Phase 6: WHERE clause protection
    fixed = re.sub(
        r"VALUES\s*\((.*?)\)",
        lambda m: f"VALUES({m.group(1).replace(' WHERE ', ' __WHERE__ ')})",
        fixed,
        flags=re.IGNORECASE
    )
    fixed = re.sub(r"\)\s*WHERE", ") WHERE", fixed, flags=re.IGNORECASE)
    fixed = fixed.replace("__WHERE__", " WHERE ")

    return fixed.strip(), list(set(errors))

def checkSyntax(raw_query: str, database_schema: dict[str, dict[str, list[str]]]) -> str:
    print("Raw QUery : ", raw_query)
    tables = []
    fields = []
    for table, desc in database_schema.items():
        tables.append(table)
        fields.extend(desc.keys())

    #print("Tables:", tables)
    #print("Fields:", fields)

    detected = detectSyntaxErrors(raw_query, tables, fields)
    #print("Detected Errors:", detected)

    corrected, applied = correctSyntax(raw_query, tables, fields)
    print("Corrected Query:", corrected)
    print("Corrections Applied:", applied)

    return corrected




# from serverConnect import serverConnect

# dobj = serverConnect()
# schema = dobj.fetch_database_structure()

# raw = input("Enter query: ")
# print("You typed:  ", raw)

# checkSyntax(raw, schema)