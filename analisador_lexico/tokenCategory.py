class TokenCategory:

    @staticmethod
    def get_category(token_type):
        category_type = {    
            "IDENTIFIER": "IDENTIFIER",
            "NUMBER": "NUMBER",
            "STRING": "STRING",
            "CHARACTER": "CHARACTER",
            "ARITHMETIC_ADDITION": "OPERATOR",
            "ARITHMETIC_SUBTRACTION": "OPERATOR",
            "ARITHMETIC_MULTIPLICATION": "OPERATOR",
            "ARITHMETIC_DIVIDER": "OPERATOR",
            "EQUAL": "OPERATOR",
            "DIFFERENT": "OPERATOR",
            "GREATER_THAN": "OPERATOR",
            "GREATER_EQUAL_THAN": "OPERATOR",
            "LESS_THAN": "OPERATOR",
            "LESS_EQUAL_THAN": "OPERATOR", 
            "AND": "OPERATOR",
            "OR": "OPERATOR",
            "ASSIGNMENT": "OPERATOR",
            "INCREMENT": "OPERATOR",
            "DECREMENT": "OPERATOR",
            "DOT_OPERATOR": "OPERATOR",
            "SEMICOLON": "DELIMITER",
            "COMMA": "DELIMITER",
            "OPEN_PARENTHESIS": "DELIMITER",
            "CLOSE_PARENTHESIS": "DELIMITER",
            "OPEN_CURLY_BRACE": "DELIMITER",
            "CLOSE_CURLY_BRACE": "DELIMITER",
            "OPEN_SQUARE_BRACKET": "DELIMITER",
            "CLOSE_SQUARE_BRACKET": "DELIMITER",
            "BLOCK_COMMENT": "COMMENTS",
            "LINE_COMMENT": "COMMENTS",
            "NUMBER_ERROR": "ERROR",
            "STRING_ERROR": "ERROR",
            "CHARACTER_INVALID": "ERROR",
            "MISSING_QUOTES": "ERROR",
            "OVERFLOW": "ERROR",
            "BLOCK_COMMENT_ERROR": "ERROR"
        }
        return category_type.get(token_type)