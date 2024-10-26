from .tokenCategory import TokenCategory

class Tokens:
    @staticmethod
    def __get_keyword(lexeme):
        keywords = {
            "variables": "VARIABLES",
            "function": "FUNCTION",
            "constants": "CONSTANTS",
            "class": "CLASS",
            "return": "RETURN",
            "empty": "EMPTY",
            "main": "MAIN",
            "if": "IF",
            "then": "THEN",
            "else": "ELSE",
            "while": "WHILE",
            "for": "FOR",
            "read": "READ",
            "write": "WRITE",
            "integer": "INTEGER",
            "float": "FLOAT",
            "boolean": "BOOLEAN",
            "string": "STRING",
            "true": "TRUE",
            "false": "FALSE",
            "extends": "EXTENDS",
            "register": "REGISTER"
        }
        return keywords.get(lexeme)
    
    @staticmethod
    def get_token(lexeme, token_type, line):
        type = token_type.name
        category = TokenCategory.get_category(type)

        keyword_type = Tokens.__get_keyword(lexeme)
        if type == "IDENTIFIER" and keyword_type:
           category = "KEYWORD"
           
        token = {
          "lexeme": lexeme,
          "category": category,
          "line": line
        }
        return token
       