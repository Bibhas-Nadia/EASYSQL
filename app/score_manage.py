
from os import path as p
import json

DIR="/opt/easysql/"
#DIR='./'

class score_manage():
    def __init__(self, database_schema: dict[str, dict[str, list[str]]]) -> None:
        self.filename = DIR+"scores.json"
        if not p.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        
        self.tables = []
        self.fields = []

        # Extract tables and fields from the database schema
        for table, fields in database_schema.items():
            self.tables.append(table)
            for field, desc in fields.items():
                self.fields.append(field)
        
        # print(self.tables)
        # print(self.fields)
        ...

    def is_keywords(self, token: str) -> bool:
        # If token belongs to SQL reserved keywords, return True else False
        sql_keywords = {
            "ADD", "ALL", "ALTER", "AND", "ANY", "AS", "ASC", "BACKUP", "BETWEEN", "CASE", "CHECK", "COLUMN",
            "CONSTRAINT", "CREATE", "DATABASE", "DEFAULT", "DELETE", "DESC", "DISTINCT", "DROP", "EXEC", "EXISTS", "FOREIGN",
            "FROM", "FULL", "GROUP", "HAVING", "IN", "INDEX", "INNER", "INSERT", "INTO", "IS", "JOIN", "KEY", "LEFT", "LIKE",
            "LIMIT", "NOT", "NULL", "OR", "ORDER", "OUTER", "PRIMARY", "PROCEDURE", "RIGHT", "ROWNUM", "SELECT", "SET", 
            "TABLE", "TOP", "TRUNCATE", "UNION", "UNIQUE", "UPDATE", "VALUES", "VIEW", "WHERE"
        }
        return token.upper() in sql_keywords
        ...

    def updateScore(self, token: str) -> None:
        scores = dict()
        with open(self.filename, "r") as f:
            score = f.read()
            if score:
                scores = json.loads(score)
        
        #print(f"the token is to save:  {token} type : {type(token)}")
        #print(f"score: {scores}")
        
        # If token is not present, assign an initial score of 1
        if token not in scores.keys() and token.upper() not in scores.keys():
            if self.is_keywords(token.upper()):
                scores[token.upper()] = 1  # Store SQL keywords in uppercase
            elif token in self.fields or token in self.tables:
                scores[token] = 1  # Store fields and tables as-is
        else:
            # If token is already present, increment its score
            if self.is_keywords(token.upper()):
                scores[token.upper()] += 1
            else:
                scores[token] += 1
        
        # Write the updated scores back to the file
        with open(self.filename, "w") as f:
            f.write(json.dumps(scores))
        ...

    def showScore(self, token: str) -> float:
        with open(self.filename, "r") as f:
            score = f.read()
            if score:
                scores = json.loads(score)
                return scores.get(token, 0.0)  # Return 0.0 if token is not found
        return 0.0
        ...

    def increaseScore(self, token: str) -> None:
        # Increase the token's score by 1
        with open(self.filename, "r") as f:
            score = f.read()
            if score:
                scores = json.loads(score)
                if token in scores:
                    scores[token] += 1
                else:
                    scores[token] = 1  # Initialize score if token does not exist
                with open(self.filename, "w") as f2:
                    f2.write(json.dumps(scores))
        ...

    def decreaseScore(self, token: str) -> None:
        # Decrease the token's score by 1, but not below 0
        with open(self.filename, "r") as f:
            score = f.read()
            if score:
                scores = json.loads(score)
                if token in scores:
                    scores[token] = max(0, scores[token] - 1)  # Ensure score does not go below 0
                with open(self.filename, "w") as f2:
                    f2.write(json.dumps(scores))
        ...

    def getScore(self) -> dict[str, float]:
        with open(self.filename, "r") as f:
            score = f.read()
            if score:
                return json.loads(score)
        return {}
        ...

    def arrangeSuggestions(self, suggestions: list[str]) -> list[str]:
        scores = self.getScore()
        # Sort suggestions based on their scores in descending order
        return sorted(suggestions, key=lambda x: scores.get(x, 0), reverse=True)
        ...





#database = {'Songs': {'id': ['int(11)', 'NO', 'PRI', ''], 'song_name': ['varchar(255)', 'NO', '', ''], 'singer': ['varchar(100)', 'YES', '', ''], 'movie_name': ['varchar(255)', 'YES', '', ''], 'release_date': ['date', 'YES', '', ''], 'composer': ['varchar(100)', 'YES', '', ''], 'writer': ['varchar(100)', 'YES', '', ''], 'music_director': ['varchar(100)', 'YES', '', ''], 'awards': ['varchar(255)', 'YES', '', '']},
#            'avengers': {'id': ['int(11)', 'NO', 'PRI', ''], 'name': ['varchar(50)', 'NO', '', ''], 'age': ['int(11)', 'NO', '', ''], 'address': ['varchar(100)', 'YES', '', ''], 'father': ['varchar(50)', 'YES', '', ''], 'contactNO': ['varchar(20)', 'YES', '', ''], 'power': ['varchar(100)', 'YES', '', '']}}

#suggestion = ['name','id','address','age','FROM','INSERT','SELECT']
#ob = score_manage(database)
#print(ob.getScore())
#print(ob.showScore('avengers'))
#print(ob.arrangeSuggestions(suggestion))
#ob.increaseScore('avengers')
#print(ob.showScore('avengers'))