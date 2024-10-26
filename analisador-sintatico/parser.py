class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0
    
    def show_error_list(self):
        return self.error_list
    
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

    def _log_error(self, expected_token):
        current_token = self.lookahead()
        self.error_list.append({
            "position": current_token["line"], 
            "expected": expected_token, 
            "received": current_token["lexeme"]
        })

    def get_error_list(self):
        return self.error_list
    
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
