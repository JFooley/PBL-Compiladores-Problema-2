import re

from .tokenType import TokenType
from .tokens import Tokens

class LexicalFiniteAutomaton:

    def __init__(self):
        self.token_valid_list = []
        self.error_list = []
        self.lexeme = ''
        self.state = 0

    def find_lexeme(self, character, line_number):
        match self.state:
            case 0:
                if (re.match(r'[a-z]|[A-Z]',character)):
                    self.lexeme += character
                    self.state = 1   
                elif (re.match(r'[0-9]',character)):
                    self.lexeme += character
                    self.state = 2
                elif (character == '"'):
                    self.lexeme += character
                    self.state = 5
                elif (character == "'"):
                    self.lexeme += character
                    self.state = 7
                elif (character == "+"):
                    self.lexeme += character
                    self.state = 10
                elif (character == "-"):
                    self.lexeme += character
                    self.state = 11
                elif (character == "*"):
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.ARITHMETIC_MULTIPLICATION)
                elif (character == "/"):
                    self.lexeme += character
                    self.state = 12
                elif (character == "="):
                    self.lexeme += character
                    self.state = 15
                elif (character == "!"):
                    self.lexeme += character
                    self.state = 16
                elif (character == ">"):
                    self.lexeme += character
                    self.state = 17
                elif character == "<":
                    self.lexeme += character
                    self.state = 18
                elif character == "&":
                    self.lexeme += character
                    self.state = 19
                elif character == "|":
                    self.lexeme += character
                    self.state = 20
                elif character == ".":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.DOT_OPERATOR)
                elif character == ";":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.SEMICOLON)
                elif character == ",":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.COMMA)
                elif character == "(":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.OPEN_PARENTHESIS)
                elif character == ")":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.CLOSE_PARENTHESIS)
                elif character == "{":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.OPEN_CURLY_BRACE)
                elif character == "}":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.CLOSE_CURLY_BRACE)
                elif character == "[":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.OPEN_SQUARE_BRACKET)
                elif character == "]":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.CLOSE_SQUARE_BRACKET)
                elif 32<ord(character)<=126:
                    self.lexeme += character
                    self.register_error_and_restart(line_number,TokenType.CHARACTER_INVALID)
            case 1:
                if (re.match(r'[a-zA-Z0-9]',character)) or (re.match(r'_',character)):
                    self.lexeme += character
                else:
                    self.save_token_and_restart(line_number, TokenType.IDENTIFIER)
                    self.find_lexeme(character, line_number)
            case 2:
                if (re.match(r'[0-9]', character)) :
                    self.lexeme += character
                elif (character == "."):
                    self.lexeme += character
                    self.state = 3
                else:
                    self.save_token_and_restart(line_number, TokenType.NUMBER)
                    self.find_lexeme(character, line_number)
            case 3:
                if (re.match(r'[0-9]', character)) :
                    self.lexeme += character
                    self.state = 4
                else:
                    self.lexeme = self.lexeme.replace(".","")
                    self.save_token_and_restart(line_number, TokenType.NUMBER)

                    self.lexeme = "."
                    self.save_token_and_restart(line_number, TokenType.DOT_OPERATOR)

                    self.find_lexeme(character, line_number)
            case 4: 
                if (re.match(r'[0-9]', character)) :
                    self.lexeme += character
                else:
                    self.save_token_and_restart(line_number, TokenType.NUMBER)
                    self.find_lexeme(character, line_number)
            case 5:
                if (character == '"'):
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.STRING)
                elif (32<=ord(character)<=126 and character != "'"):
                    self.lexeme += character
                elif (character == "\n"):
                    self.register_error_and_restart(line_number,TokenType.MISSING_QUOTES)
                else:
                    self.lexeme += character
                    self.state = 6
            case 6:
                if character == '"':
                    self.lexeme += character
                    self.register_error_and_restart(line_number,TokenType.STRING_ERROR)
                elif (character == "\n"):
                    self.register_error_and_restart(line_number,TokenType.MISSING_QUOTES)
                else:
                    self.lexeme += character
            case 7:
                if ((32<=ord(character)<=126) and character != '"' and character != "'"):
                    self.lexeme += character
                    self.state = 8
                else:
                    self.register_error_and_restart(line_number,TokenType.CHARACTER_INVALID)
                    self.find_lexeme(character, line_number)
            case 8:
                if character == "'":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.CHARACTER)
                elif (character == "\n"):
                    self.register_error_and_restart(line_number,TokenType.MISSING_QUOTES)
                else:
                    self.lexeme += character
                    self.state = 9
            case 9:
                if (character == "'"):
                    self.lexeme += character
                    self.register_error_and_restart(line_number, TokenType.OVERFLOW)
                elif (character == "\n"):
                    self.register_error_and_restart(line_number,TokenType.MISSING_QUOTES)
                else:
                    self.lexeme += character
            case 10:
                if character == "+":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.INCREMENT)
                else:
                    self.save_token_and_restart(line_number, TokenType.ARITHMETIC_ADDITION)
                    self.find_lexeme(character, line_number)
            case 11:
                if re.match(r'-', character):
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.DECREMENT)
                else:
                    self.save_token_and_restart(line_number, TokenType.ARITHMETIC_SUBTRACTION)
                    self.find_lexeme(character, line_number)
            case 12:
                if character == "*": 
                    self.lexeme += character
                    self.state = 13
                elif character == "/": 
                    self.lexeme += character
                    self.state = 14
                else:
                    self.save_token_and_restart(line_number, TokenType.ARITHMETIC_DIVIDER)
                    self.find_lexeme(character, line_number)
            case 13:
                self.lexeme += character
                if character == "*":
                    self.state = 21
            case 14:
                if (character == "\n"):
                    self.save_token_and_restart(line_number, TokenType.LINE_COMMENT)
                else:
                    self.lexeme += character
            case 15: 
                if character == "=":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.EQUAL)
                else:
                    self.save_token_and_restart(line_number, TokenType.ASSIGNMENT)
                    self.find_lexeme(character, line_number)
            case 16:
                if character == "=":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.DIFFERENT)
                else:
                    self.register_error_and_restart(line_number, TokenType.CHARACTER_INVALID)
                    self.find_lexeme(character, line_number)
            case 17:
                if character == "=":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.GREATER_EQUAL_THAN)
                else:
                    self.save_token_and_restart(line_number, TokenType.GREATER_THAN)
                    self.find_lexeme(character, line_number)
            case 18:
                if character == "=":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.LESS_EQUAL_THAN)
                else:
                    self.save_token_and_restart(line_number, TokenType.LESS_THAN)
                    self.find_lexeme(character, line_number)
            case 19: 
                if character == "&":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.AND)
                else:
                    self.register_error_and_restart(line_number,TokenType.CHARACTER_INVALID)
                    self.find_lexeme(character, line_number)
            case 20:
                if character == "|" :
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.OR)
                else:
                    self.register_error_and_restart(line_number,TokenType.CHARACTER_INVALID)
                    self.find_lexeme(character, line_number)
            case 21:
                if character == "/":
                    self.lexeme += character
                    self.save_token_and_restart(line_number, TokenType.BLOCK_COMMENT)
                elif character == "*":
                    self.lexeme += character
                else:
                    self.lexeme += character
                    self.state = 13

                

    def save_token_and_restart(self, line_number, token_type):
        self.token_valid_list.append(Tokens.get_token(self.lexeme, token_type, line_number))
        self.lexeme = ''
        self.state = 0

    def register_error_and_restart(self, line_number, token_type):
        self.error_list.append(Tokens.get_token(self.lexeme, token_type, line_number))
        self.lexeme = ''
        self.state = 0

    def show_token_list(self):
        return self.token_valid_list

    def show_error_list(self):
        return self.error_list

    def recognize_tokens(self, file):
        for line_number, line in enumerate(file, start=1):
            for character in line:
                self.find_lexeme(character, line_number)
        if self.state == 13 or self.state == 21:
            self.register_error_and_restart(line_number, TokenType.BLOCK_COMMENT_ERROR)
        