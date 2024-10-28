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
    
def function_call(self):
    # Passo 1: Verificar o identificador da função
    if self.lookahead()['category'] == "identifier":
        self.match_category("identifier")  # Espera um identificador

        # Passo 2: Abrir parênteses
        if self.lookahead()['lexeme'] == "(":
            self.match_lexeme("(")  # Espera '('

            # Passo 3: Processar a lista de argumentos (opcional)
            # Se o próximo token não for ')', há ao menos um argumento
            if self.lookahead()['lexeme'] != ")":
                self.argument()  # Chama a função para processar o primeiro argumento
                self.argument_list()  # Processa os argumentos restantes, se houver

            # Passo 4: Fechar parênteses
            self.match_lexeme(")")  # Espera ')'
        else:
            self._log_error("(")  # Caso não haja '(', registra o erro
    else:
        self._log_error("identifier")  # Caso não haja identificador, registra o erro

    def arguments(self):
        if self.lookahead()['lexeme'] == "(" and self.lookahead(1)['lexeme'] == ")":
            # Caso: parênteses vazios, correspondendo a '()'
            self.match_lexeme(["("])  # Consome o '('
            self.match_lexeme([")"])  # Consome o ')'
        elif self.lookahead()['lexeme'] == "(":
            # Caso: parêntese de abertura seguido de valores
            self.match_lexeme(["("])  # Consome o '('
            self.value()  # Processa o primeiro argumento
            self.argument_tail()  # Processa os argumentos adicionais, se houver
            self.match_lexeme([")"])  # Consome o ')'
        else:
            # Caso de erro se nenhum dos formatos válidos foi encontrado
            self._log_error("expected '()' or '(' with arguments")

    def argument_tail(self):
        # Processa os argumentos adicionais separados por vírgula
        while self.lookahead()["lexeme"] == ",":
            self.match_lexeme([","])  # Consome a vírgula
            self.value()  # Processa o próximo argumento

    def return_statement(self):
        # Verifica se o token atual é a palavra-chave "return"
        if self.lookahead()['lexeme'] == "return":
            self.match_lexeme(["return"])  # Consome o token "return"
            
            # Verifica se há uma expressão a ser retornada usando lookahead
            if self.lookahead()['lexeme'] not in [";"]:
                # Caso não seja o token de fim, processa a expressão a ser retornada
                self.parse_expression()
            # Finaliza a instrução com ponto e vírgula
            self.match_lexeme([";"])


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
                         
    def logic_value(self):
        current_token = self.lookahead()
        if current_token["lexeme"] in ['true', 'false']: 
            self.match_lexeme(['true', 'false'])
        else:
            self.relational_expression()  

    def logic_terminal(self):
        self.match_lexeme(['&&', '||']) 

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

    def relational_terminal(self):
        self.match_lexeme(['>', '<', '!=', '>=', '<=', '=='])

    def function(self):
        if self.lookahead()['lexeme'] == "function":
            self.match_lexeme("function")
            self.match_category("KEYWORD")
            self.match_category("IDENTIFIER")
            self.parameters()
            self.match_lexeme("{")
            #self.parse_statements() # TODO
            self.match_lexeme("}")
        else:
            self._log_error('function')

    def parameters(self):
        if self.lookahead()['lexeme'] == "(":
            self.match_lexeme("(")
            self.parameter()
        else:
            self._log_error('(')

    def parameter(self):
        if self.lookahead()['category'] == "KEYWORD":
            self.match_category("KEYWORD")
            self.match_category("IDENTIFIER")
            self.parameter_list()
        elif self.lookahead()['lexeme'] == ")":
            self.match_lexeme(")")
        else:
            self._log_error(')')  

    def parameter_list(self):
        if self.lookahead()['lexeme'] == ",":
            self.match_lexeme(",")
            self.parameter()
        elif self.lookahead()['lexeme'] == ")":
            self.match_lexeme(")")
        else:
            self._log_error("',' or ')'")