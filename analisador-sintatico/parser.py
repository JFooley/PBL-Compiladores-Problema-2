class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0
    
    # Função match para verificar categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        self.index += 1 # Move to the next token
        if current_token['category'] != None and current_token['category'] in expected_token_category:
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_category, "received":current_token["category"]})
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        self.index += 1 # Move to the next token
        if current_token['lexeme'] != None and current_token['lexeme'] in expected_token_lexeme:
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
    
    # Fazer o resto, de constants, variables, functions
    def arithmetic_expression(self):
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
    
    def arithmetic_operating(self):
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()

    def arithmetic_value(self):
        if self.lookahead()["category"] == "number":
            self.match_category("number")
        elif self.lookahead()["lexeme"] == "(":
            self.match_lexeme("(")
            self.arithmetic_expression()
            self.match_lexeme(")")
        elif self.lookahead()["category"] == "identifier":
            if self.lookahead(1)["category"] == "(":
                #self.function_call()
                pass
            else:
                #self.attribute
                pass

    def arithmetic_sum(self):
        self.match_lexeme(['+', '-'])
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
      
    def arithmetic_multiplication(self):
        self.match_lexeme(['*', '/'])
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()
