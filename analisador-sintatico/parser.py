class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0
    
    # Função match para verificar categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        if current_token['category'] != None and current_token['category'] in expected_token_category:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_category, "received":current_token["category"]})
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        if current_token['lexeme'] != None and current_token['lexeme'] in expected_token_lexeme:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_lexeme, "received":current_token["lexeme"]})
    
    # Acessa o token atual ou examina os proximos
    def lookahead(self, K = 0):
        if self.index + K < len(self.token_list):
            return self.token_list[self.index + K]
        return {"lexeme": None,"category": None,"line": None}
    
    # Executa o algorítimo
    def run(self):
        self.start()
        return len(self.error_list) == 0
    
    ### Produções ###
    def start(self):
        # <start>::= <registers> <constants> <variables> <functions> <main> 
        #           | <registers> <constants> <variables> <main> 
        #           | <constants> <variables> <functions> <main>
        #           | <constants> <variables> <main>
        
        if self.lookahead()["lexeme"] == "register":
            self.registers()

        self.constants()
        self.variables()
        
        if self.lookahead()["lexeme"] == "function":
            self.functions()

        self.main()
    
    def registers(self):
        self.match_lexeme("register")
    
    # ---- Laços de repetição ---

    # <for> ::= 'for' '(' <initialization> ';' <relational expression> ';' identifier <increment terminal> ')' '{' <body> '}'
    def for_statement(self):
        """ Regra para <for> ::= 'for' '(' <initialization> ';' <relational expression> ';' identifier <increment terminal> ')' '{' <body> '}' """
        self.match_lexeme(["for"])
        self.match_lexeme(["("])
        #self.initialization()          # Remover comentário ao implementar função
        self.match_lexeme([";"])
        #self.relational_expression()   # Remover comentário ao implementar função
        self.match_lexeme([";"])
        self.match_category(["IDENTIFIER"])
        #self.increment_terminal()      # Remover comentário ao implementar função
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        #self.body()                    # Remover comentário ao implementar função
        self.match_lexeme(["}"])

    # <initialization> ::= "integer" identifier "=" <arithmetic expression> | identifier "=" <arithmetic expression>
    def initialization(self):
        """ Regra para <initialization> ::= "integer" identifier "=" <arithmetic expression> | identifier "=" <arithmetic expression> """
        if self.lookahead()["lexeme"] == "integer":
            self.match_lexeme(["integer"])
        self.match_category(["IDENTIFIER"])
        self.match_lexeme(["="])
        #self.arithmetic_expression()      # Remover comentário ao implementar função
    
    # <increment terminal> ::= '++' | '--'
    def increment_terminal(self):
        """ Regra para <increment terminal> ::= '++' | '--' """    
        self.match_lexeme(["++", "--"])
    
    # <while>::= 'while' '(' <logic expression> ')' '{' <body> '}'
    def while_statement(self):
        """ Regra para <while>::= 'while' '(' <logic expression> ')' '{' <body> '}' """
        self.match_lexeme(["while"])
        self.match_lexeme(["("])
        #self.logic_expression()    # Remover comentário ao implementar função
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        #self.body()                # Remover comentário ao implementar função
        self.match_lexeme(["}"])