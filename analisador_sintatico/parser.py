class Parser():
    def __init__(self, semantic_analyzer, token_list):
        self.validator = semantic_analyzer
        self.token_list = token_list
        self.error_list = []
        self.token_accumulator_list = []
        self.index = 0
    
    # Função match para verificar a categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        if current_token['category'] != None and current_token['category'] in expected_token_category:
            self.index += 1
            self.token_accumulator_list.append(current_token)
            return current_token
        else:
            self.error_recovery(current_token['line'], expected_token_category)
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        if current_token['lexeme'] != None and current_token['lexeme'] in expected_token_lexeme:
            self.index += 1
            self.token_accumulator_list.append(current_token)
            return current_token
        else:
            self.error_recovery(current_token['line'], expected_token_lexeme)

    # Função para recuperação de erros
    def error_recovery(self, line_number, expected_token):
        errors_sync = ['(',')','}','{',';']
        tokens_error = []
        while not self.lookahead()["lexeme"] in errors_sync:
            tokens_error.append(self.lookahead()["lexeme"])
            self.index += 1
        self.error_list.append({"position":line_number, "expected":expected_token, "received": tokens_error})
    
    # Função para retornar o token atual ou referente ao index K
    def lookahead(self, K = 0):
        if self.index + K < len(self.token_list):
            return self.token_list[self.index + K]
        return {"lexeme": None,"category": None,"line": None}

    def get_error_list(self):
        return self.error_list
    
    def run(self):
        self.start()
        return len(self.error_list) == 0

 #---------------------  ---------------------
    def start(self):
        if self.lookahead()["lexeme"] == "register": 
            self.registers()

        self.constants()
        self.variables() 
        
        if self.lookahead()["lexeme"] == "function":
            self.functions() 

        self.main() 

        current_token = self.lookahead()
        if current_token["lexeme"] != None:
            self.error_list.append({"position":current_token["line"], "expected": "Nenhum token", "received": current_token["lexeme"]})
    
 #--------------------- registers ---------------------
    def registers(self):
        self.register()
        if self.lookahead()["lexeme"] == "register":
            self.registers()

    def register(self):
        size_error = len(self.error_list)
        self.match_lexeme(["register"])
        self.token_accumulator_list = []
        self.match_category(["IDENTIFIER"])
        self.match_lexeme(['{'])
        self.register_body()
        self.match_lexeme(['}']) 
        
        if (len(self.error_list) == size_error):
            self.validator.add_registers_to_table(self.token_accumulator_list)

    def register_body(self):
        self.declaration()
        if self.lookahead()["category"] == "IDENTIFIER" or self.lookahead()["lexeme"] in ['integer','float','boolean','string']:
            self.register_body()

#--------------------- constants ---------------------
    def constants(self):
        self.match_lexeme(['constants']) 
        self.match_lexeme(['{'])
        if self.lookahead()["lexeme"] == "}":
            self.match_lexeme(['}']) 
        else:
            self.constants_declarations()  
            self.match_lexeme(['}']) 

    def constants_declarations(self):
        self.assignment_declaration()
        if self.lookahead()["lexeme"] in ['integer','float','boolean','string']:
            self.constants_declarations()

#--------------------- Variaveis ---------------------
    def variables(self):
        self.match_lexeme(['variables'])
        self.match_lexeme(['{'])
        self.token_accumulator_list = []
        size_error = len(self.error_list)
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()
        
        if (len(self.error_list) == size_error):
            self.validator.add_variables_to_table(self.token_accumulator_list)
        self.match_lexeme(['}'])

    def expression_variables(self):
        self.expression_declaration()
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()

#--------------------- Função ---------------------
    def functions(self):
        self.function()
        if self.lookahead()["lexeme"] == "function":
            self.functions()

    def function(self):
        self.match_lexeme(["function"])
        if self.lookahead()['lexeme'] == "empty": 
            self.match_lexeme(["empty"])
        else:
            self.type()
        self.match_category(["IDENTIFIER"])
        self.parameters()
        self.match_lexeme(["{"])
        self.statements()
        self.match_lexeme(["}"])

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
            self.match_lexeme([","])
            self.parameter()

#--------------------- main ---------------------
    def main(self):
        self.match_lexeme(["main"])
        self.match_lexeme(["("])
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        self.statements()
        self.match_lexeme(["}"])

#------------------- tipos e atribuições -------------------
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
    
    def declaration(self):
        self.type()
        self.match_category(['IDENTIFIER']) 
        self.match_lexeme([';']) 

    def assignment_declaration(self):
        self.token_accumulator_list = []
        size_erro = len(self.error_list)
        self.primitive_type()
        self.match_category(['IDENTIFIER']) 
        self.match_lexeme(['=']) 
        self.value() 
        self.match_lexeme([';']) 
        if (len(self.error_list) == size_erro):  #Verificar se houve erros sintáticos
            self.validator.add_constants_to_table(self.token_accumulator_list)


    def assignment(self):
        self.attribute()
        if self.lookahead()["lexeme"] == "=":
            self.match_lexeme(["="])
            self.value()
            self.match_lexeme([";"])
        else:
            self.increment_terminal()
            self.match_lexeme([";"])

    def value(self):
        if self.lookahead()["category"] == "STRING":
            self.match_category(["STRING"])
        elif self.lookahead()["category"] == "CHARACTER":
            self.match_category(["CHARACTER"])
        else:
            self.logic_expression()

    def expression_declaration(self):
        if self.lookahead()['category'] == 'IDENTIFIER':
            self.match_category(["IDENTIFIER"])
            self.match_category(["IDENTIFIER"])
        else:
            self.primitive_type()
            if self.lookahead()['category'] == 'IDENTIFIER' and self.lookahead(1)['lexeme'] != "[": 
                self.match_category(["IDENTIFIER"])
                if self.lookahead()['lexeme'] == '=':
                    self.match_lexeme(["="])
                    self.value()
            else:
                self.vector_position()
        self.match_lexeme([";"])

    def attribute(self):
        if self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == ".":
            self.register_position()
        elif self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "[":
            self.vector_position()
        else:
            self.match_category(["IDENTIFIER"])  
       

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

#--------------------- Comandos ---------------------
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
            self.return_statement()
        else:
            self.function_call()
            self.match_lexeme([";"])

#--------------------- for ---------------------
    def for_loop(self):
        self.match_lexeme(["for"])
        self.match_lexeme(["("])
        self.initialization()
        self.match_lexeme([";"])
        self.relational_expression()  
        self.match_lexeme([";"])
        self.match_category(["IDENTIFIER"])
        self.increment_terminal()
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        self.body()             
        self.match_lexeme(["}"])
    
    def initialization(self):
        if self.lookahead()["lexeme"] == "integer":
            self.match_lexeme(["integer"])
        self.match_category(["IDENTIFIER"])
        self.match_lexeme(["="])
        self.arithmetic_expression()    
    
    def increment_terminal(self):    
        self.match_lexeme(["++", "--"])
    
#--------------------- while ---------------------
    def while_loop(self):
        self.match_lexeme(["while"])
        self.match_lexeme(["("])
        self.logic_expression()  
        self.match_lexeme([")"])
        self.match_lexeme(["{"])
        self.body()             
        self.match_lexeme(["}"])

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

#--------------------- Return  ---------------------
    def return_statement(self):
        self.match_lexeme(["return"])  
        if self.lookahead()['lexeme'] not in [";"]:
            self.value()
        self.match_lexeme([";"])

#--------------------- Chamada de função  ---------------------
    def function_call(self):
        self.match_category(["IDENTIFIER"])
        self.arguments()

    def arguments(self):
        self.match_lexeme(["("])
        if self.lookahead()['lexeme'] == ")":
            self.match_lexeme([")"])  
        else:
            self.value() 
            self.argument() 
            self.match_lexeme([")"]) 

    def argument(self):
        while self.lookahead()["lexeme"] == ",":
            self.match_lexeme([","]) 
            self.value()  

#--------------------- statements ---------------------
    def statements(self):
        self.validator.create_local_table() #cria a tabela local para o escopo da função/main
        self.variables()
        self.body()            
        self.validator.remove_local_table()

#--------------------- body ---------------------
    def body(self):         
        if ((self.lookahead()["lexeme"] in ["for", "while", "if", "write", "read", "return"]) or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "(")):  
            self.commands()
        else:
            self.assignment() 
        if ((self.lookahead()["lexeme"] in ["for", "while", "if", "write", "read", "return"] or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] == "("))
            or (self.lookahead()["category"] == "IDENTIFIER" and self.lookahead(1)["lexeme"] in ["=", ".", "[", "++", "--"])):
            self.body()  

#--------------------- Expressões lógicas ---------------------

    def logic_expression(self):
        self.logic_value()
        while self.lookahead()["lexeme"] in ['||', '&&']:
            self.logic_operator()
            self.logic_value()

    def logic_value(self):
        if self.lookahead()["lexeme"] in ["true", "false"]:
            self.match_lexeme(["true", "false"])
        else:
            self.relational_expression()

    def logic_operator(self):
        self.match_lexeme(['||', '&&'])

#--------------------- Expressões relacionais ---------------------
    def relational_expression(self):
        self.arithmetic_expression()  
        if self.lookahead()["lexeme"] in ['>', '<', '!=', '>=', '<=', '==']:
            self.relational_operator()
            self.arithmetic_expression()

    def relational_operator(self):
        self.match_lexeme(['>', '<', '!=', '>=', '<=', '=='])

#--------------------- Expressões aritméticas ---------------------   
    def arithmetic_expression(self):
        self.arithmetic_term()
        while self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_operator()
            self.arithmetic_term()

    def arithmetic_term(self):
        self.arithmetic_value()
        while self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_operator()
            self.arithmetic_value()

    def arithmetic_value(self):
        if self.lookahead()["lexeme"] == "(":
            self.match_lexeme(["("])
            self.logic_expression()
            self.match_lexeme([")"])

        elif self.lookahead()["lexeme"] == "-":
            self.match_lexeme(["-"])
            self.match_category(["NUMBER"])

        elif self.lookahead()["category"] == "IDENTIFIER":
            if self.lookahead(1)["lexeme"] == "(":
                self.function_call()
            else:
                self.attribute()
        else:
            self.match_category(["NUMBER"])

    def arithmetic_operator(self):
        self.match_lexeme(['+', '-', '*', '/'])