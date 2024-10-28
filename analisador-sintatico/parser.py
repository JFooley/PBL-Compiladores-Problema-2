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
        return len(self.error_list) == 0
    
    ### Produções ###
    def start(self):
        # <start>::= <registers> <constants> <variables> <functions> <main> 
        #           | <registers> <constants> <variables> <main> 
        #           | <constants> <variables> <functions> <main>
        #           | <constants> <variables> <main>
        
        #if self.lookahead()["lexeme"] == "register": # TODO Ainda não implementado
        #    self.registers()

        #self.constants() # TODO Ainda não implementado
        #self.variables() # TODO Ainda não implementado
        
        if self.lookahead()["lexeme"] == "function":
            self.functions() 

        #self.main() TODO Ainda não implementado

 #--------------------- Expressões aritméticas ---------------------                             
    def expression_declaration(self):
        if self.lookahead()['category'] == 'IDENTIFIER':
            self.match_category(["IDENTIFIER"])
            self.match_category(["IDENTIFIER"])
        else:
            self.primitive_type()
            if self.lookahead()['category'] == 'IDENTIFIER':
                self.match_category(["IDENTIFIER"])
                if self.lookahead()['lexeme'] == '=':
                    self.match_lexeme(["="])
                    self.value()
            else:
                self.vector_position()
        self.match_lexeme([";"])
            
    def expression_variables(self):
        self.expression_declaration()
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()
       
    def variables(self):
        self.match_lexeme(['variables'])
        self.match_lexeme(['{'])
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()
        self.match_lexeme(['}'])
              
    def arithmetic_expression(self):
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()

    def arithmetic_operating(self):
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()
  
    def arithmetic_value(self):
        if self.lookahead()["category"] == "NUMBER":
            self.match_category("number")
        elif self.lookahead()["category"] == "IDENTIFIER":
            if self.lookahead(1)["category"] == "(":
                self.function_call()
            else:
                self.attribute()
        else:
            self.match_lexeme("(")
            self.arithmetic_expression()
            self.match_lexeme(")")

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

#--------------------- Função ---------------------
#DESENVOLVER O FUNCTIONS
    def function(self):
        self.match_lexeme("function")
        self.type()
        self.match_category("IDENTIFIER")
        self.parameters()
        self.match_lexeme("{")
        self.statements()
        self.match_lexeme("}")

#--------------------- Parâmetros ---------------------
    def parameters(self):
        self.match_lexeme(["("])
        if self.lookahead()['lexeme'] == ")" :
            self.match_lexeme([")"])
        else: 
            self.parameter()
            self.match_lexeme([")"])
        
    def parameter(self):
        self.type()
        self.match_category("IDENTIFIER")
        if self.lookahead()['lexeme'] == ",":
            self.match_lexeme(",")
            self.parameter()

    def function_call(self):
        # Passo 1: Verificar o identificador da função
        self.match_category(["IDENTIFIER"])  # Espera um identificador
        self.arguments()

    def arguments(self):
        self.match_lexeme("(")
        if self.lookahead()['lexeme'] == ")":
            # Caso: parênteses vazios, correspondendo a '()'
            self.match_lexeme(")")  # Consome o ')'
        else:
            # Caso: parêntese de abertura seguido de valores
            self.value()  # Processa o primeiro argumento
            self.argument()  # Processa os argumentos adicionais, se houver
            self.match_lexeme(")")  # Consome o ')'

    def argument(self):
        # Processa os argumentos adicionais separados por vírgula
        while self.lookahead()["lexeme"] == ",":
            self.match_lexeme(",")  # Consome a vírgula
            self.value()  # Processa o próximo argumento

#--------------------- Expressões lógicas ---------------------
    def logic_expression(self):
        current_token = self.lookahead()
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("]) 
            self.logic_expression() 
            self.match_lexeme([")"]) 
            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal() 
                self.logic_expression()
        else:
            self.logic_value()
            if self.lookahead()["lexeme"] in ['&&', '||']:
                self.logic_terminal()
                self.logic_expression()
                            
    def logic_value(self):
        current_token = self.lookahead()
        if current_token["lexeme"] in ['true', 'false']: 
            self.match_lexeme(['true', 'false'])
        else:
            self.relational_expression()  

    def logic_terminal(self):
        self.match_lexeme(['&&', '||']) 

#--------------------- Expressões relacionais ---------------------
    def relational_expression(self):
        current_token = self.lookahead()
        if current_token["lexeme"] == "(":
            self.match_lexeme(["("])
            self.relational_expression()
            self.match_lexeme([")"]) 
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()
        else:
            self.arithmetic_expression()
            if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
                self.relational_terminal()
                self.relational_expression()

    def relational_terminal(self):
        self.match_lexeme(['>', '<', '!=', '>=', '<=', '=='])

#--------------------- Condicionais ---------------------
    def condicional(self):
        self.match_lexeme(["if"])
        self.match_lexeme(["("])
        self.logic_expression()
        self.match_lexeme([")"])
        self.match_lexeme(["then"])
        self.match_lexeme(["{"])
        self.body()
        self.match_lexeme(["}"])

        if (self.lookahead()["lexeme"] == "else"):
            self.match_lexeme(["else"])
            self.match_lexeme(["{"])
            self.body()
            self.match_lexeme(["}"])

#--------------------- Write ---------------------
    def write(self):
        self.match_lexeme(["write"])
        self.match_lexeme(["("])
        
        self.value()  
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme([","])  
            self.value() 

        self.match_lexeme([")"])
        self.match_lexeme([";"])

#--------------------- Read ---------------------
    def read(self):
        self.match_lexeme(["read"])
        self.match_lexeme(["("])
        
        self.attribute()  
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme([","])  
            self.attribute() 

        self.match_lexeme([")"])
        self.match_lexeme([";"])

    def value(self):
        if self.lookahead()["category"] == "STRING":
            self.match_category(["STRING"])
        elif self.lookahead()["category"] == "CHARACTER":
            self.match_category(["CHARACTER"])
        else:
            self.logic_expression()

    def type(self):
        if self.lookahead()["category"] == "IDENTIFIER":
             self.match_category(["IDENTIFIER"])
        else:
            self.primitive_type()

    def primitive_type(self):
        if self.lookahead()["lexeme"] == "integer":
            self.match_lexeme(["integer"])
        elif self.lookahead()["lexeme"] == "float":
            self.match_lexeme(["float"])
        elif self.lookahead()["lexeme"] == "boolean":
            self.match_lexeme(["boolean"])
        else:
            self.match_lexeme(["string"])

    def assignment(self):
        self.attribute()
        if self.lookahead()["lexeme"] == "=":
            self.match_lexeme(["="])
            self.value()
            self.match_lexeme([";"])
        else:
            self.increment_terminal()
            self.match_lexeme([";"])

    def attribute(self):
        if self.lookahead()["category"] == "IDENTIFIER":
            self.match_category(["IDENTIFIER"])
            if self.lookahead()["lexeme"] == ".":
                self.register_position()
            elif self.lookahead()["lexeme"] == "[":
                self.vector_position()
        else: 
            self.match_category(["IDENTIFIER"])

    #<commands>::= <for> | <while> | <if> | <write> | <read> | <return> | <function call> ';'
    def commands(self):
        if self.lookahead()["lexeme"] == "for":
            self.for_loop()
        elif self.lookahead()["lexeme"] == "while":
            self.while_loop()
        elif self.lookahead()["lexeme"] == "if":
            self.condicional()
        elif self.lookahead()["lexeme"] == "write":
            self.write()
        elif self.lookahead()["lexeme"] == "read":
            self.read()
        elif self.lookahead()["lexeme"] == "return":
            #self.return()
            pass
        else:
            self.function_call()
            self.match_lexeme([";"])

    def vector_position(self):
        self.match_category(["IDENTIFIER"])
        self.vector_index()

    def vector_index(self):
        self.match_lexeme(["["])
        if self.lookahead()["category"] == "NUMBER" and self.lookahead(1)["lexeme"] == "]":
            self.match_category("NUMBER")
        elif self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "]":
            self.match_category("IDENTIFIER")
        else:
            self.arithmetic_expression()
        self.match_lexeme(["]"])

        if self.lookahead()["lexeme"] == "[" and (self.lookahead(1)["category"] in ["NUMBER", "IDENTIFIER"] or self.lookahead(1)["lexeme"] == "("):
            self.vector_index()
            
    def register_position(self):
        self.match_category(["IDENTIFIER"])
        self.register_access()
    
    def register_access(self):
        self.match_lexeme(["."])
        if self.lookahead()["category"] == "IDENTIFIER":
            self.match_category(["IDENTIFIER"])
            if self.lookahead()["lexeme"] == ".":
                self.register_access()
        else:
            self.vector_position()

