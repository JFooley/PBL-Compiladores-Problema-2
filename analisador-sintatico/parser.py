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
    # <start>::= <registers> <constants> <variables> <functions> <main> 
    #           | <registers> <constants> <variables> <main> 
    #           | <constants> <variables> <functions> <main>
    #           | <constants> <variables> <main>
    def start(self):
        self.logic_expression()
    
    # <registers>::= <register> | <register> <registers>
    def registers(self):
        self.match_lexeme("register")
    
    # <logic expression> ::= 
    #       <logic value> 
    #     | <logic value> <logic terminal> <logic expression> 
    #     | '(' <logic expression> ')' 
    #     | '(' <logic expression> ')' <logic terminal> <logic expression>
    def logic_expression(self):
        current_token = self.lookahead()

        # Caso: '(' <logic expression> ')' ou '(' <logic expression> ')' <logic terminal> <logic expression>
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("]) 
            self.logic_expression() 
            self.match_lexeme([")"]) 
            
            # Check for the optional <logic terminal> and further <logic expression>
            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal() 
                self.logic_expression()

        # Caso: <logic value> ou <logic value> <logic terminal> <logic expression>
        else:
            self.logic_value()

            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal()
                self.logic_expression()
                            
    # <logic value> ::= booleanDeclarate | <relational expression>
    def logic_value(self):
        current_token = self.lookahead()
        
        if current_token["lexeme"] in ['true', 'false']: 
            self.match_lexeme(['true', 'false'])
        else:
            self.relational_expression()  

    # <logic terminal> ::= '&&' | '||'
    def logic_terminal(self):
        self.match_lexeme(['&&', '||']) 
    
    # <relational expression>::= 
    #         <arithmetic expression> <relational terminal> <relational expression> 
    #       | <arithmetic expression>
    #       | '(' <relational expression> ')' <relational terminal> <relational expression> 
    #       | '(' <relational expression> ')' 
    def relational_expression(self):
        current_token = self.lookahead()

        # Caso: '(' <relational expression> ')' ou '(' <relational expression> ')' <relational terminal> <relational expression>
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("])
            self.relational_expression()
            self.match_lexeme([")"]) 
            
            # Verify <relational terminal> and further <relational expression>
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()

        # Caso: <arithmetic expression> ou <arithmetic expression> <relational terminal> <relational expression>
        else:
            self.arithmetic_expression()
            
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()

    # <relational terminal> ::= '>' | '<' | '!=' | '>=' | '<=' | '=='
    def relational_terminal(self):
        self.match_lexeme(['>', '<', '!=', '>=', '<=', '=='])


# Testando a classe
token_list = []
token_list.append({"lexeme": "(", "category": "OPEN_PARENTHESIS", "line": 1})
token_list.append({"lexeme": "true", "category": "boolean","line": 1})
token_list.append({"lexeme": "&&", "category": "operator","line": 1})
token_list.append({"lexeme": "false", "category": "boolean","line": 1})
token_list.append({"lexeme": ")", "category": "CLOSE_PARENTHESIS", "line": 1})
token_list.append({"lexeme": "||", "category": "operator","line": 1})
token_list.append({"lexeme": "true", "category": "number","line": 1})

for item in token_list:
    print(item["lexeme"], end=" ")
print('')

p = Parser(token_list)

if p.run():
    print("Passou sem erros")
else:
    print("Falhou, erros:")
    for erro in p.error_list:
        print(erro)