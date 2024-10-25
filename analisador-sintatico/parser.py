class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0
    
    # Função match para verificar categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        if current_token['category'] in expected_token_category:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_category, "received":current_token["category"]})
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        if current_token['lexeme'] in expected_token_lexeme:
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
        return len(self.error_list) > 0
    
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
    
    # Fazer o resto, de constants, variables, functions

#<if>::= <fixed if>  | <fixed if> 'else' '{' <body> '}'
#<fixed if>::= 'if' '(' <logic expression> ')' 'then' '{' <body> '}' 
#--------------------- Condicionais ---------------------
    def condicional(self):
        self.match_lexeme("if")
        self.match_lexeme("(")
        #self.logic_expression()
        self.match_lexeme("expressao") #Remover quando tiver o logic_expression()
        self.match_lexeme(")")
        self.match_lexeme("then")
        self.match_lexeme("{")
        #self.body()
        self.match_lexeme("body") #Remover quando tiver o body()
        self.match_lexeme("}")

        if (self.lookahead()["lexeme"] == "else"):
            self.match_lexeme("else")
            self.match_lexeme("{")
            #self.body()
            self.match_lexeme("body") #Remover quando tiver o body()
            self.match_lexeme("}")


#<write>::= 'write' '(' <write list> ')' ';'
#<write list> ::= <value> ',' <write list> | <value>
#--------------------- Write ---------------------
    def write(self):
        self.match_lexeme("write")
        self.match_lexeme("(")
        
        #self.value()  
        self.match_lexeme("value") #Remover quando tiver
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme(",")  
            #self.value() 
            self.match_lexeme("value") #Remover quando tiver

        self.match_lexeme(")")
        self.match_lexeme(";")


#<read>::= 'read' '(' <read list> ')' ';'
#<read list>::= <attribute>  ',' <read list> | <attribute>
#--------------------- Read ---------------------
    def read(self):
        self.match_lexeme("read")
        self.match_lexeme("(")
        
        #self.attribute()  
        self.match_lexeme("attribute") #Remover quando tiver
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme(",")  
            #self.attribute() 
            self.match_lexeme("attribute") #Remover quando tiver

        self.match_lexeme(")")
        self.match_lexeme(";")
