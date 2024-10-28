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
    
    #--------------------- main ---------------------
    # <main>::= 'main' '(' ')' '{' <statements> '}'
    def main(self):
        self.match_lexeme(["main"])
        self.match_lexeme(["("])
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        self.statements()
        self.match_lexeme(["}"])
    
    #--------------------- statements ---------------------
    # <statements>::= <variables> <body>      TODO TESTAR COM A PRODUÇÃO DE variables
    def statements(self):
        #self.variables()      #Remover comentário ao implementar função
        self.body()            

    #--------------------- body ---------------------
    # <body>::= <commands> | <assignment> | <commands> <body>| <assignment> <body>     TODO TESTAR COM AS PRODUÇÕES DE commands E assignment
    def body(self):         
        # <commands>::= <for> | <while> | <if> | <write> | <read> | <return> | <function call> ';'
        if ((self.lookahead()["lexeme"] in ["for", "while", "if", "write", "read", "return"]) or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "(")):
            pass    
            #self.commands()    # Remover comentário ao implementar função

        # <assignment>::= <attribute> '=' <value> ';' | <attribute> <increment terminal> ';'
        else:
            pass
            #self.assignment()  # Remover comentário ao implementar função
        
        # <commands> <body> | <assignment> <body>
        if ((self.lookahead()["lexeme"] in ["for", "while", "if", "write", "read", "return"] or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "("))
            or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] in ["=", ".", "[", "++", "--"])):
            self.body()     # Recursividade


    def registers(self):
        self.match_lexeme(["register"])
        self.match_category(["IDENTIFIER"])
        if self.lookahead()["lexeme"] == "{":
            self.match_lexeme(['{'])
            self.register_body()
            self.match_lexeme(['}']) 

    def register_body(self):
        if self.lookahead()["lexeme"] != '}':
            self.declaration()  
            self.register_body()

    def declaration(self):
        if self.lookahead()["category"] == "IDENTIFIER":
            self.match_category(["IDENTIFIER"]);    
        else:
            self.match_lexeme(['integer','float','boolean','string'])
        self.match_category(['IDENTIFIER']) 
        self.match_lexeme([';']) 
    
    def constants(self):
        self.match_lexeme(['constants']) 
        if self.lookahead()["lexeme"] == "{":
            self.match_lexeme(['{'])
            self.constants_declarations()  
            self.match_lexeme(['}']) 

    def constants_declarations(self):
        if self.lookahead()["lexeme"] != '}':
            self.assignment_declaration()  
            self.constants_declarations()
    
    def assignment_declaration(self):
        self.match_lexeme(['integer','float','boolean','string'])
        self.match_category(['IDENTIFIER']) 
        self.match_lexeme(['=']) 
        self.value() 
        self.match_lexeme([';']) 

    def value(self):
        if self.lookahead()["category"] in ['NUMBER','STRING','CHARACTER']:
            self.match_category(['NUMBER','STRING','CHARACTER']) # Falta parte de logical expression

    #--------------------- for ---------------------
    # <for>::= 'for' '(' <initialization> ';' <relational expression> ';' identifier <increment terminal> ')' '{' <body> '}'
    def for_loop(self):
        self.match_lexeme(["for"])
        self.match_lexeme(["("])
        self.initialization()
        self.match_lexeme([";"])
        #self.relational_expression()   # Remover comentário ao implementar função
        self.match_lexeme([";"])
        self.match_category(["IDENTIFIER"])
        self.increment_terminal()
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        #self.body()                    # Remover comentário ao implementar função
        self.match_lexeme(["}"])
    
    #--------------------- initialization ---------------------
    # <initialization>::= "integer" identifier "=" <arithmetic expression> | identifier "=" <arithmetic expression>
    def initialization(self):
        if self.lookahead()["lexeme"] == "integer":
            self.match_lexeme(["integer"])
        self.match_category(["IDENTIFIER"])
        self.match_lexeme(["="])
        #self.arithmetic_expression()      # Remover comentário ao implementar função
    
    #--------------------- increment terminal ---------------------
    # <increment terminal> ::= '++' | '--'
    def increment_terminal(self):    
        self.match_lexeme(["++", "--"])
    
    #--------------------- while ---------------------
    # <while>::= 'while' '(' <logic expression> ')' '{' <body> '}'
    def while_loop(self):
        self.match_lexeme(["while"])
        self.match_lexeme(["("])
        #self.logic_expression()    # Remover comentário ao implementar função
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        #self.body()                # Remover comentário ao implementar função
        self.match_lexeme(["}"])