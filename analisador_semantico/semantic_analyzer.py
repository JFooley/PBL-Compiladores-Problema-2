from analisador_semantico.tables import TabelaPares, EntryRegisters, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = -1
        
        # Tabela de registros
        self.registers_type_table: list[EntryRegisters] = []

        # Tabela de pares
        self.pairs_table = TabelaPares()

        # Lista de erros semânticos
        self.error_list = []

        self.tokens = []
        self.create_global_table()

    ################################ Funções auxiliares ################################
    def get_error_list(self):
        return self.error_list

    ## Gera um erro na lista de erros ## 
    def throw_error(self, message, token):
        self.error_list.append({"position": token["line"], "message": message})

    ## Busca uma entrada específica na cadeia de tabelas designada ## 
    def find_table_entry(self, target_table_index, token, throw_erro = True):
        selected_entry = None

        # Busca no escopo atual
        for entry in self.pairs_table.tabela[target_table_index]["tabela"]:
            if entry.nome == token["lexeme"]:
                selected_entry = entry

        # Busca recursivamente no escopo pai até chegar na global, caso não tenha achado
        if selected_entry == None and target_table_index > 0:
            selected_entry = self.find_table_entry(self.pairs_table.tabela[target_table_index]["pai"], token, throw_erro)
        
        # Causa erro se necessário
        if (throw_erro and selected_entry == None): self.throw_error(f"{token["lexeme"]} não existe nesse escopo.", token)

        return selected_entry
    
    def get_registers(self, token):
        registers = []
        for entry in self.registers_type_table:
            if entry.nome == token["lexeme"]:
                registers.append(entry)
        
        if len(registers) == 0:
            return None
        return registers
    
    def create_local_table(self):
        local_table: list[EntryIdentificadores] = []
        self.pairs_table.adicionarPar(self.current_table_index, local_table)
        self.current_table_index = self.current_table_index + 1
    
    def create_global_table(self):
        global_table: list[EntryIdentificadores] = []
        self.pairs_table.adicionarPar(self.current_table_index, global_table)
        self.current_table_index = 0
        
    def remove_local_table(self):
        if (self.current_table_index != 0) :
            self.pairs_table.tabela.pop(self.current_table_index)
            self.current_table_index = self.current_table_index - 1

    ################################ Funções de erro ################################
    def is_int(self,token):
        return "." not in token["lexeme"]
    
    def identify_var_kind(self, tokens): ## identifica qual tipo é a variável ou value passado e devolve o tipo e o token necessário
        if len(tokens) == 1:
            ## Identifier
            if tokens[0]["category"] == "IDENTIFIER":
                return {"tipo":"IDENTIFIER", "token": tokens[0]}
            ## Literal
            else:
                return {"tipo":"LITERAL", "token": tokens[0]}
            
        else:
            ## Register
            if tokens[1]["lexeme"] == ".":
                new_lexeme = ""
                for token in tokens:
                    if token["lexeme"] == "[":
                        break
                    new_lexeme += token["lexeme"]

                new_token = {"lexeme": new_lexeme, "category": tokens[0]["category"], "line": tokens[0]["line"]}
                return {"tipo":"REGISTER", "token": new_token}
            
            ## Function call
            elif tokens[1]["lexeme"] == "(":
                return {"tipo":"FUNCTION CALL", "token": tokens[0]}

            ## Vector
            elif tokens[1]["lexeme"] == "[":
                return {"tipo":"VECTOR", "token": tokens[0]}
            
            ## Expresion
            else:
                return {"tipo":"EXPRESSION", "token": tokens}
    
    #------------------------------ JG e Caleo -----------------------------------
    def wrong_type_assign(self, current_table_index, variable, value): ## Identifica em uma atribuição a = b se o tipo de a é diferente do tipo de b
        variable_dict = self.identify_var_kind(variable)
        value_dict = self.identify_var_kind(value)

        variable = variable_dict["token"]
        value = value_dict["token"]

        variable_entry: EntryIdentificadores = self.find_table_entry(current_table_index, variable["lexeme"])

        if variable_entry == None:
            return False

        match value_dict["tipo"]:
            case "IDENTIFIER":
                value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value["lexeme"])

                if (value_entry == None):
                    return False
                
                if (variable_entry.tipo != value_entry.tipo):
                    self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                    return False

            case "LITERAL":
                match value["category"]:
                    case "NUMBER":
                        if (variable_entry.tipo != "float" and variable_entry.tipo != "integer" and ("." in value["lexeme"] and variable_entry.tipo == "integer")):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)
                            return False
                    
                    case "STRING":
                        if (variable_entry.tipo != "string"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)
                            return False

                    case "CHARACTER":
                        if (variable_entry.tipo != "character"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)
                            return False

                    case "BOOLEAN":
                        if (variable_entry.tipo != "boolean"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)    
                            return False

            case "REGISTER":
                value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value["lexeme"])
            
                if (value_entry == None):
                    return False

                if (variable_entry.tipo != value_entry.tipo):
                    self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                    return False

            case "VECTOR":                
                value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value["lexeme"])

                if (value_entry == None):
                    return False

                if (variable_entry.tipo != value_entry.tipo):
                    self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                    return False

            case "FUNCTION CALL":
                value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value["lexeme"])

                if (value_entry == None):
                    return False

                if (variable_entry.tipo != value_entry.tipoRetorno):
                    self.throw_error(f"{value_entry.tipoRetorno} não pode ser convertido em {variable_entry.tipo}.", value)
                    return False

            case "EXPRESSION":
                pass

        return True

    def repeated_statement(self, current_table_index, new_variable):
        ## Verifica se a variável existe no escopo
        if (self.find_table_entry(current_table_index, new_variable, throw_erro= False) == None):
            self.throw_error(f"{new_variable["lexeme"]} já existe neste escopo.", new_variable)
            return False

        ## Verifica se ele não possui um nome igual a de um tipo primitivo
        if (new_variable["lexeme"] in ["float", "integer", "string", "character", "boolean"]):
            self.throw_error(f"{new_variable["lexeme"]} não pode ter o nome de um tipo primitivo.")
            return False

        ## Verifica se ele não possui um nome igual a de um tipo register
        for entry in self.registers_type_table:
            if entry.nome == new_variable["lexeme"]:
                self.throw_error(f"{new_variable["lexeme"]} não pode ter o nome de um tipo de registro.")
                return False
        
        return True

    def non_declared_object(self, current_table_index, token):
        object_entry = self.identify_var_kind(token)
        if self.find_table_entry(current_table_index, object_entry) == None:
            return False
        else:
            return True
    #------------------------------ JG e Caleo -----------------------------------

    ################################ Funções de Adicionar na tabela ################################

    # verificar se ja nao existe um id com o mesmo nome
    def add_function_to_table(self, token_list):
        if self.find_table_entry(0, token_list[1], False) != None:
            self.throw_error(f"{token_list[1]['lexeme']} já foi declarada", token_list[1])
            return

        return_type = token_list[0]['lexeme']
        function_name = token_list[1]['lexeme']
        parameters_type_list = []
        i = 3
        while i < len(token_list):
            parameters_type_list.append(token_list[i]['lexeme'])
            i += 3
        function_entry = EntryIdentificadores(function_name, 'function', None, return_type, parameters_type_list, None)
        self.pairs_table.tabela[0]['tabela'].append(function_entry)

    def add_registers_to_table(self,token_list):
        size_error = len(self.error_list)
        nome = token_list[0]
        temp = []
        #verificar se o nome do registro já não está na tabela de simbolos, ou como constants
        for i in range(2, len(token_list) - 1, 3):
            tipo = token_list[i]
            atributo = token_list[i+1]
            
            #Se o tipo for um identificador, verificar se existe como registro
            #Declaração repetida entre 2 atributos dos registros;
            register_entry = EntryRegisters(nome["lexeme"], {atributo["lexeme"]: {"tipo": tipo["lexeme"]}})
            temp.append(register_entry)
        
        if(size_error == len(self.error_list)):
            self.registers_type_table.append(temp)

    '''deve enviar a lista de tokens assim: Cadastro pessoa; ou Cadastro pessoa = pessoa1;
      Para o caso de Cadastro pessoa = pessoa1 precisa criar outra função para verificar o pessoa1  
    
    def add_register_instance_to_table(self,token_list): 
        register_type = token_list[0]
        instance_name = token_list[1]
        #Verificar o erro se existe o register criado
        #Verificar se não existe variavel/funcao/register com o nome da instancia
        instance_register = EntryIdentificadores(instance_name, register_type)
        self.pairs_table.tabela[0]['tabela'].append(instance_register)
        registers = self.get_registers(register_type)
       
        if (token_list[2] == "="):
            #verificar se a instancia passada já existe e se é um register, se for: precisa preencher os valores
            print(".")
        print(self.pairs_table.tabela[0]['tabela'])
    ''' 
    def add_constants_to_table(self,token_list):
        tipo = token_list[0]
        nome = token_list[1] 
        valor = token_list[3]
        
        size_error = len(self.error_list)
        #Verificar se o identificador ja não existe como constante ou variaveis na tabela de simbolos
        #error_já_exite
        #Verificar se o tipo primitivo é do mesmo valor adicionado
        #erro_valor
        #se list error size = list error size anterior pode adicionar
        #Se nenhum desses casos ser vdd, adicionar na tabela global
        if(size_error == len(self.error_list)):
            constant_entry = EntryIdentificadores(nome["lexeme"], tipo["lexeme"], valor["lexeme"], None, None, 0, True)
            self.pairs_table.tabela[0]['tabela'].append(constant_entry)

    
    # Precisa analisar se já existe na tabela
    # Definir quando acaba o escopo da variável 
    # Verificar se já existe variavel com mesmo nome na tabela de simbolos
    # verificar tipo e valor, quando tem atibuição;
    # Se for vetor, verificar se o tamanho é int(number ou identificador)
    def add_variables_to_table(self, is_global, token_list):
        variable_type = ""
        variable_name = ""
        variable_value = ""
        vector_length = 0
        for i in range(0, len(token_list)):
            token = token_list[i]
            if token['category'] == 'KEYWORD':  #obs: o tipo pode ser tbm identifier, que é o caso de ser um register
                variable_type = token['lexeme']
            
            elif token['category'] == 'IDENTIFIER':
                variable_name = token['lexeme']
            
            elif token['category'] == 'OPERATOR' and token['lexeme'] == '=':
                variable_value = token_list[i + 1]['lexeme']
            
            elif token['category'] == 'DELIMITER' and token['lexeme'] == '[':
                vector_length =  token_list[i + 1]['lexeme']
                    
            elif token['category'] == 'DELIMITER' and token['lexeme'] == ";":  # Encontrando o delimitador ';'
                variables_entry = EntryIdentificadores(variable_name, variable_type, variable_value, None, None, vector_length)
                # self.create_local_table()
                self.pairs_table.tabela[0 if is_global == True else self.current_table_index]['tabela'].append(variables_entry)
                # Resetando as variáveis para a próxima variável
                variable_type, variable_name, variable_value = "", "", ""
                vector_length = []
    
    ################################ Funções de Verificar na tabela ################################

    def validate_function_parameters(self, token_list):
        function_entry = self.find_table_entry(0, token_list[0])

        if function_entry == None:
            return
        
        # Retira da lista de tokens acumulados apenas os tokens referentes aos argumentos passados na chamda
        function_call_arguments = []
        i = 1
        while i < len(token_list):
            if token_list[i]['lexeme'] == '(' or token_list[i]['lexeme'] == ',':
                if token_list[i+2]['lexeme'] == '.': # caso seja um objeto o id depois do . importa
                    function_call_arguments.append([])
                else:
                    function_call_arguments.append(token_list[i+1])

            if type(function_call_arguments[-1]) == list and token_list[i]['category'] == 'IDENTIFIER':
                function_call_arguments[-1].append(token_list[i])

            i += 1

        #print(function_call_arguments)

        if len(function_call_arguments) != len(function_entry.parametros):
            self.throw_error(f"{token_list[0]} espera {len(function_entry.parametros)} parametro(s), mas recebeu {len(function_call_arguments)}", token_list[0])
            return

        # Constroi a lista de tipos dos argumentos acessando a tabela de simbolos
        arguments_types = []
        i = 0
        while i < len(function_call_arguments):
            if type(function_call_arguments[i]) == list:
                name = function_call_arguments[i][0]
                j = 1
                while j < len(function_call_arguments[i]):
                    name['lexeme'] += '.' + function_call_arguments[i][j]['lexeme']
                    j += 1
                entry = self.find_table_entry(self.current_table_index, name)
            else:
                entry = self.find_table_entry(self.current_table_index, function_call_arguments[i])

            if entry == None:
                return
            
            if type(function_call_arguments[i]) == list or entry.tipo == 'function':
                arguments_types.append(entry.tipoRetorno)
            else:
                arguments_types.append(entry.tipo)
        
            i += 1
        
        # Compara os tipos da lista de parametros com o da lista de argumentos
        i = 0
        while i < len(function_entry.parametros):
            if arguments_types[i] != function_entry.parametros[i]:
                self.throw_error(f"{i}º parametro de {token_list[0]} é diferente de {arguments_types[i]}", token_list[0])
                return
            i += 1

    ################ Função para tratar o tipo do token ######################
    # Usei essa função pois, a categoria do token recebido não se encaixa com o token verificado
    def conversion(self, value):
        # Tentar converter para int
        try:
            return "integer"
        except ValueError:
            pass

        # Tentar converter para float
        try:
            return "float"
        except ValueError:
            pass

        # Tentar converter para bool
        if value.lower() in ("true", "false"):
            return "boolean"

        # Caso não seja nenhum dos anteriores, manter como string
        return "string"
    
    #################### Função para validar o return (inteiro / identificador) ##################
    def validate_function_return(self, token_list):
        # Recebendo o tipo do que está sendo retornado
        token = {"lexeme": None,"category": None,"line": None}
        
        if token_list[1]['lexeme'] == ';':
            token = token_list[0]
            
        # Busca pelo identificador na tabela
        function_entry = None
        if token['category'] == "IDENTIFIER":
            function_entry = self.find_table_entry(self.current_table_index, token=token)
            
        # busca o retorno da função a partir da tabela de símbolos
        return_entry = self.pairs_table.tabela[self.current_table_index]['tabela'][0]
        
        if function_entry != None and function_entry.tipo != return_entry.tipoRetorno:
            self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
        elif function_entry == None and token['lexeme'] != None: # Verificar se o valor é igual ao tipo da função
            if(self.conversion(token['lexeme']) != return_entry.tipoRetorno):
                self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)

    #################### Função para validar o incremento ou decremento  ####################
    def validate_increment_decrement(self, token_list: list):
        token = token_list[0]  # Identificador deve ser o primeiro da lista de tokens
        token_entry = self.find_table_entry(self.current_table_index, token)  # Busca a variável nas tabelas - Se não encontrou o elemento nas tabelas o erro é contabilizado pela propria função
        if token_entry != None:  # Se encontrou o identificador na tabela
            if (token_entry.tipoRetorno != None and (token_entry.tipoRetorno != "integer")):  # Para registrador
                self.throw_error("A variável deve ser do tipo inteiro", token)
            elif (token_entry.tipo != "integer"): # Para variável ou vetor
                self.throw_error("A variável deve ser do tipo inteiro", token) 

    #------------------------------ Metas Estéfane e felipe -----------------------------------
    def error_vector_size(self,token):
        if (token["category"] == "NUMBER" and not self.is_int(token)):
            self.throw_error("O indíce do vetor deve ser inteiro", token)
        elif (token["category"] == "IDENTIFIER"):
            object = self.find_table_entry(self.current_table_index,token)
            if(object != None and not object.tipo == "int"):
                self.throw_error("O indíce do vetor deve ser inteiro", token)   

    def error_has_value(self,token):
        if (token["category"] == "IDENTIFIER"):
            object = self.find_table_entry(self.current_table_index,token)
            if(object != None and object.valor == None):
                self.throw_error("A variável não foi inicializada", token)

    '''Modificar valor de uma constante  (Felipe e Estéfane); Essa função precisa ser verificada junto com de  atribuição do valor igual ao tipo
    então o jeito que ela está não verifica se está no formato a = 5; só verifica se "a" não é uma constante. Provavel que essa função se junta com outras.
    '''
    def error_modify_constant(self,token):
        if (token["category"] == "IDENTIFIER"):
            object = self.find_table_entry(self.current_table_index,token,False)
            if(object != None and object.isConstant):
                self.throw_error("O valor de uma constante não pode ser alterado.", token)

    #--------------------------------------------------------

    def error_function_call(self,token_list):
        #Verificar erro se a função existe
        #Verificar erro dos parametros
        return

tokens = [
    {"lexeme" : "integer", "category": "KEYWORD", "line": 1},
    {"lexeme" : "integer", "category": "IDENTIFIER", "line": 1},
    {"lexeme" : "integer", "category": "OPERATOR", "line": 1},
    {"lexeme" : "10", "category": "NUMBER", "line": 1},
    {"lexeme" : ";", "category": "NUMBER", "line": 1},
    ]

analizer = SemanticAnalyzer()
analizer.add_variables_to_table()
