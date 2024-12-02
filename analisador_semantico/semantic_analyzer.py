from analisador_semantico.tables import TabelaPares, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = -1
        
        # Tabela de registros
        self.registers_type_table = {}

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
        if (throw_erro and selected_entry == None): self.throw_error(f"{token['lexeme']} não existe nesse escopo.", token)

        return selected_entry

    def get_register(self, token, throw_erro = True):
        if token["lexeme"] in self.registers_type_table:
            return self.registers_type_table[token["lexeme"]]
        else:
            if throw_erro: self.throw_error(f"O register {token['lexeme']} não existe.", token)
            return None
    
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
    
    #------------------------------ JG e Caleo -----------------------------------

    def is_expresion(self, tokens):
        for token in tokens:
            if token["category"] == "OPERATOR" and token["lexeme"] != ".":
                return True
        return False

    def is_increment(self, token_list):
        for token in token_list:
            if token['lexeme'] in ['++', '--']:
                return True
        return False

    def is_function(self, token_list):
        return token_list[1]['lexeme'] == '('

    def printar_linha(self, token_list):
        for token in token_list:
            print(token['lexeme'], end=' ')
        print()

################################ Funções de Adicionar na tabela ################################

    # verificar se ja nao existe um id com o mesmo nome
    # chamar função que verifica se a função retorna algo
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
        function_entry = EntryIdentificadores(function_name, 'function', None, return_type, parameters_type_list, 0)
        self.pairs_table.tabela[0]['tabela'].append(function_entry)

    def add_registers_to_table(self,token_list):
        size_error = len(self.error_list)
        name = token_list[0]
        temporary_list = []

        if self.repeated_statement(self.current_table_index,name) == False:  #verificar se não existe variavel/funcao/register com o nome da instancia. se alterar o tipo de retorno da função tem que voltar para ajustar
            return 

        for i in range(2, len(token_list) - 1, 3):
            type = token_list[i]
            attribute = token_list[i+1]

            if(type["category"] == "IDENTIFIER"):
                registers = self.get_register(type) #Verifica se existe o register criado
        
            self.error_attribute_register_duplicate(attribute,temporary_list) #Verifica Declaração repetida entre 2 atributos dos registros;
            register_entry = {"nome_atributo": attribute["lexeme"], "tipo": type["lexeme"]}
            temporary_list.append(register_entry)
        
        if (size_error == len(self.error_list)):
            self.registers_type_table[name["lexeme"]] = temporary_list


    def add_register_instance_to_table(self,token_list): 
        register_type = token_list[0]
        instance_name = token_list[1]
        isIdentifier = False

        if self.repeated_statement(self.current_table_index,instance_name) == False:  #verificar se não existe variavel/funcao/register com o nome da instancia. se alterar o tipo de retorno da função tem que voltar para ajustar
            return 
        
        registers = self.get_register(register_type) #Verifica se existe o register foi criado
        if (registers == None):
            return
        
        if (len(token_list) > 4):
            if(token_list[2]["lexeme"] == "=" and (token_list[3]["category"] != "IDENTIFIER" or token_list[4]["lexeme"] != ";")):
                self.throw_error("Associação inválida de register", token_list[3])
                return

            if (token_list[3]["category"] == "IDENTIFIER" ):
                isIdentifier = True
                variable = self.find_table_entry(self.current_table_index,token_list[3])
                if (variable != None and variable.tipo != register_type["lexeme"]):
                    self.throw_error("Tipo de register incompatível",token_list[3])
                    return
        
        size_error = len(self.error_list)    
        instance_register = EntryIdentificadores(instance_name["lexeme"], register_type["lexeme"])
        self.pairs_table.tabela[self.current_table_index]['tabela'].append(instance_register)
       
        for register in registers:
            value = None
            attribute_name = instance_name["lexeme"]+"."+register["nome_atributo"]
            
            if (isIdentifier):
                name = token_list[3]["lexeme"]+"."+register["nome_atributo"]
                new_token = { "lexeme": name,"category": "IDENTIFIER","line": token_list[3]["line"]}
                line = self.find_table_entry(self.current_table_index,new_token)
                if (line != None):
                    value = line.valor

            if(size_error == len(self.error_list)):
                instance = EntryIdentificadores(attribute_name, register["tipo"], value, None, None, 0, False)
                self.pairs_table.tabela[self.current_table_index]['tabela'].append(instance)      
     
    def add_constants_to_table(self,token_list):
        type = token_list[0]
        name = token_list[1]
        value = ""
        value_list = []
        for token in token_list[3:len(token_list) - 1]:
            value = value + " " + token["lexeme"]
            value_list.append(token)

        size_error = len(self.error_list)

        if self.repeated_statement(self.current_table_index,name) == False: #Verifica se o identificador ja não existe como constante ou variaveis na tabela de simbolos
            return 
        
        if self.wrong_type_assign(self.current_table_index,name,value_list,type) == False: #Verificar se o tipo primitivo é do mesmo valor adicionado
            return 
        
        if(size_error == len(self.error_list)):
            constant_entry = EntryIdentificadores(name["lexeme"], type["lexeme"], value, None, None, 0, True)
            self.pairs_table.tabela[0]['tabela'].append(constant_entry)

    
    # Precisa analisar se já existe na tabela
    # Definir quando acaba o escopo da variável 
    # Verificar se já existe variavel com mesmo nome na tabela de simbolos
    # verificar tipo e valor, quando tem atibuição;
    # Se for vetor, verificar se o tamanho é int(number ou identificador)
  # Precisa analisar se já existe na tabela
    # Definir quando acaba o escopo da variável 
    # verificar tipo e valor, quando tem atibuição;
    # Se for vetor, verificar se o tamanho é int(number ou identificador)
    def add_variables_to_table(self, is_global, token_list):
        variable_type = ""
        variable_name = ""
        variable_value = ""
        vector_length = []
        for i in range(0, len(token_list)):
            token = token_list[i]
            if self.find_table_entry(0, token, False) != None:
                self.throw_error(f"{token['lexeme']} já foi declarada", token)
                return
            if token['category'] == 'KEYWORD':  #obs: o tipo pode ser tbm identifier, que é o caso de ser um register
                variable_type = token['lexeme']
            
            elif token['category'] == 'IDENTIFIER': # Falta verificar os registers
                if token_list[1]['lexeme'] == ".":
                    variable_type = token['lexeme']
                else:
                    variable_name = token['lexeme']
            
            elif token['category'] == 'OPERATOR' and token['lexeme'] == '=': # consumir tudo até o ;
                variable_value = token_list[i + 1]['lexeme']
            
            elif token['category'] == 'DELIMITER' and token['lexeme'] == '[': # verificar se é um vector ou matriz
                vector_length.append(token_list[i + 1]['lexeme'])
                    
            elif token['category'] == 'DELIMITER' and token['lexeme'] == ";":  # Encontrando o delimitador ';'
                variables_entry = EntryIdentificadores(variable_name, variable_type, variable_value, None, None, vector_length)
                self.pairs_table.tabela[0 if is_global == True else self.current_table_index]['tabela'].append(variables_entry)
                # Resetando as variáveis para a próxima variável
                variable_type, variable_name, variable_value = "", "", ""
                vector_length = []
        # print(self.pairs_table.tabela)

    def indetify_expression_return(self, current_scope_index, tokens):
        ## Identifica se a expressão aritimética passada é do tipo aritimética (retorna apenas number) ou do tipo logica/relacional (retorna boolean)
        ## A função da throw nos erros caso alguma das variáveis não existam ou sejam string e retorna None caso tenha falhado
        ## Caso não tenha falhado, ela vai retornar o tipo do retorno da expressão (number ou boolean)
        tipo = ["float", "integer"]

        # Encontra o tipo da função
        for token in tokens:
            if token["category"] == "OPERATOR" and token["lexeme"] != "." and token["lexeme"] in ["&&", "||", '>', '<', '!=', '>=', '<=', '==']:
                tipo = ["boolean"]
                break
        
        # Valida os atributos (se existem e são diferentes de string)
        variable_tokens = []
        for token in tokens:
            if token["category"] == "OPERATOR" and token["lexeme"] != ".":
                variable = self.identify_var_kind(variable_tokens)

                if variable["tipo"] == "IDENTIFIER" or variable["tipo"] == "REGISTER" or variable["tipo"] == "VECTOR":
                    variable_entry: EntryIdentificadores = self.find_table_entry(current_scope_index, variable["token"])

                    if variable_entry == None:
                        return None

                    if variable_entry.tipo not in ["integer", "float", "boolean"]:
                        self.throw_error(f"O tipo {variable_entry.tipo} não pode ser operado em uma expressão", variable["token"])
                        return None
                    
                elif variable["tipo"] == "FUNCTION CALL":
                    variable_entry: EntryIdentificadores = self.find_table_entry(current_scope_index, variable["token"])

                    if variable_entry == None:
                        return None

                    if variable_entry.tipoRetorno not in ["integer", "float", "boolean"]:
                        self.throw_error(f"O tipo {variable_entry.tipoRetorno} não pode ser operado em uma expressão", variable["token"])
                        return None
                variable_tokens.clear()

            else:
                variable_tokens.append(token)
        return tipo
        
    def identify_var_kind(self, tokens): ## identifica qual tipo é a variável ou value passado e devolve o tipo e o token necessário
        if len(tokens) == 1:
            ## Identifier
            if tokens[0]["category"] == "IDENTIFIER":
                return {"tipo":"IDENTIFIER", "token": tokens[0]}
            ## Literal
            else:
                return {"tipo":"LITERAL", "token": tokens[0]}
            
        else:
            ## Expresion
            if self.is_expresion(tokens):
                return {"tipo":"EXPRESSION", "token": tokens}

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

    def wrong_type_assign(self, current_table_index, variable, value, variable_type = None): 
        ## Identifica em uma atribuição variable = value se o tipo de a é diferente do tipo de b
        ## variable: lista de tokens do objeto varible (ex: "identifier" ou "identifier" "." "identifier" ou "identifier" "[" "number" "]" e etc)
        ## value: lista de tokens do objeto value (ex: "identifier" ou "identifier" "." "identifier" ou "identifier" "[" "number" "]" e "identnfier" "(" ")")

        variable_dict = self.identify_var_kind(variable)
        value_dict = self.identify_var_kind(value)

        variable = variable_dict["token"]
        value = value_dict["token"]

        ## Não é declaração
        if variable_type == None: 
            variable_entry: EntryIdentificadores = self.find_table_entry(current_table_index, variable)

            if variable_entry == None:
                return False
        
            if variable_entry.isConstant:
                self.throw_error(f"{variable["lexeme"]} é uma constante, não pode ter seu valor alterado.", variable)
                return False

            match value_dict["tipo"]:
                case "IDENTIFIER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

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
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)
                
                    if (value_entry == None):
                        return False

                    if (variable_entry.tipo != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                        return False

                case "VECTOR":                
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

                    if (value_entry == None):
                        return False

                    if (variable_entry.tipo != value_entry.tipo or variable_entry.tamanho == 0):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                        return False

                case "FUNCTION CALL":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

                    if (value_entry == None):
                        return False

                    if (variable_entry.tipo != value_entry.tipoRetorno or variable_entry.tamanho != value_entry.tamanho):                        
                        self.throw_error(f"{value_entry.tipoRetorno} não pode ser convertido em {variable_entry.tipo}.", value)
                        return False

                case "EXPRESSION":
                    value_type = self.indetify_expression_return(self.current_table_index, value)
                    
                    if value_type == None:
                        return False

                    if variable_entry.tipo not in value_type:
                        self.throw_error(f"{value_type} não pode ser convertido em {variable_entry.tipo}.", value)
                        return False
        
        ## É declaração
        else:
             match value_dict["tipo"]:
                case "IDENTIFIER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

                    if (value_entry == None):
                        return False
                    
                    if (variable_type["lexeme"] != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)
                        return False

                case "LITERAL":
                    match value["category"]:
                        case "NUMBER":
                            if (variable_type["lexeme"] != "float" and variable_type["lexeme"] != "integer" and ("." in value["lexeme"] and variable_type["lexeme"] == "integer")):
                                self.throw_error(f"{value["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value)
                                return False
                        
                        case "STRING":
                            if (variable_type["lexeme"] != "string"):
                                self.throw_error(f"{value["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value)
                                return False

                        case "CHARACTER":
                            if (variable_type["lexeme"] != "character"):
                                self.throw_error(f"{value["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value)
                                return False

                        case "BOOLEAN":
                            if (variable_type["lexeme"] != "boolean"):
                                self.throw_error(f"{value["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value)    
                                return False

                case "REGISTER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)
                
                    if (value_entry == None):
                        return False

                    if (variable_type["lexeme"] != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_type["lexeme"]}.", value)
                        return False

                case "VECTOR":                
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

                    if (value_entry == None):
                        return False

                    if (variable_type["lexeme"] != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_type["lexeme"]}.", value)
                        return False

                case "FUNCTION CALL":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value)

                    if (value_entry == None):
                        return False

                    if (variable_type["lexeme"] != value_entry.tipoRetorno):
                        self.throw_error(f"{value_entry.tipoRetorno} não pode ser convertido em {variable_type["lexeme"]}.", value)
                        return False

                case "EXPRESSION":
                    value_type = self.indetify_expression_return(self.current_table_index, value)
                    
                    if value_type == None:
                        return False

                    if variable_type["lexeme"] not in value_type:
                        self.throw_error(f"{value_type} não pode ser convertido em {variable_type["lexeme"]}.", value[0])
                        return False

        return True

    def repeated_statement(self, current_table_index, new_variable):
        ## Verifica se a variável definida pelo token new_variable já foi declarada
        ## new_variable: token do objeto que vai ser declarado

        ## Verifica se a variável existe no escopo
        if (self.find_table_entry(current_table_index, new_variable, throw_erro= False) != None):
            self.throw_error(f"{new_variable["lexeme"]} já existe neste escopo.", new_variable)
            return False

        ## Verifica se ele não possui um nome igual a de um tipo primitivo
        if (new_variable["lexeme"] in ["float", "integer", "string", "character", "boolean"]):
            self.throw_error(f"{new_variable["lexeme"]} não pode ter o nome de um tipo primitivo.", new_variable)
            return False

        ## Verifica se ele não possui um nome igual a de um tipo register
        for key in self.registers_type_table.keys():
            if key == new_variable["lexeme"]:
                self.throw_error(f"{new_variable["lexeme"]} não pode ter o nome de um tipo de registro.", new_variable)
                return False
        
        return True


    def non_declared_object(self, current_table_index, tokens):
        ## Verifica se um objeto não existe
        ## tokens: lista de tokens que definem o objeto (ex: "identifier" ou "identifier" "." "identifier" ou "identifier" "[" "number" "]" e etc)
        object_entry = self.identify_var_kind(tokens)
        if self.find_table_entry(current_table_index, object_entry["token"]) == None:
            return False
        else:
            return True
    #------------------------------ JG e Caleo -----------------------------------

    def error_attribute_register_duplicate(self,token,list_register):
        if any(entry["nome_atributo"] == token["lexeme"] for entry in list_register):
            self.throw_error(f"{token['lexeme']} já existe como atributo do registro.", token)
    
    ################################ Funções de Verificar na tabela ################################

    def validate_function_parameters(self, token_list):
        function_entry = self.find_table_entry(0, token_list[0])

        if function_entry == None:
            return
        
        if function_entry.tipo != 'function':
            self.throw_error(f"{token_list[0]['lexeme']} não é uma função", token_list[0])
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
                print(name)
                entry = self.find_table_entry(self.current_table_index, name)
                if entry == None:
                    return
                else:
                    arguments_types.append(entry.tipoRetorno)
            elif function_call_arguments[i]['category'] == 'NUMBER':
                if '.' in function_call_arguments[i]['lexeme']:
                    arguments_types.append('float')
                else:
                    arguments_types.append('integer')
            elif function_call_arguments[i]['category'] in ['STRING','CHARACTER']:
                arguments_types.append('string')
            elif function_call_arguments[i]['lexeme'] in ['true', 'false']:
                arguments_types.append('boolean')
            else:
                entry = self.find_table_entry(self.current_table_index, function_call_arguments[i])
                if entry == None:
                    return
                elif entry.tipo == 'function':
                     arguments_types.append(entry.tipoRetorno)
                else:
                    arguments_types.append(entry.tipo)
            i += 1
        
        # Compara os tipos da lista de parametros com o da lista de argumentos
        i = 0
        while i < len(function_entry.parametros):
            if arguments_types[i] != function_entry.parametros[i]:
                self.throw_error(f"{i+1}º parametro de {token_list[0]['lexeme']} é {arguments_types[i]}, espera-se {function_entry.parametros[i]}", token_list[0])
                return
            i += 1

    ################ Função para tratar o tipo do token ######################
       # Usei essa função pois, a categoria do token recebido não se encaixa com o token verificado
    def conversion(self, value):
        # Tentar converter para int
        if value == "NUMBER":
            return "integer"
        if value == "STRING":
            return "string"
        if value == "BOOLEAN" or value == "true" or value == "false":
            return "boolean"
        # Caso não seja nenhum dos anteriores, manter como string
        return "string"
    
    #################### Função para validar o return (inteiro / identificador) ##################
    def validate_function_return(self, token_list):
        return_entry = self.pairs_table.tabela[self.current_table_index]['tabela'][0]
        if len(token_list) == 1 :
            if not return_entry.tipoRetorno == "empty":
                self.throw_error("O retorno da função está vazio", token_list[0]['line'])   
            return 
        value_dict = self.identify_var_kind(token_list)
        
        match value_dict["tipo"]:
            case "IDENTIFIER":
                token = value_dict["token"]
                function_entry: EntryIdentificadores = self.find_table_entry(self.current_table_index, token)
                if (function_entry == None):
                    return False
                if function_entry.tipo != return_entry.tipoRetorno:
                    self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
            case "LITERAL":
                token = value_dict["token"]
                if self.conversion(token['category']) != return_entry.tipoRetorno:
                    self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
            
            case "FUNCTION CALL":
                token = value_dict["token"]
                function_entry: EntryIdentificadores = self.find_table_entry(self.current_table_index, token)

                if (function_entry == None):
                    return False
                
                if function_entry.tipoRetorno != return_entry.tipoRetorno:
                    self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)

            case "REGISTER":
                token = value_dict["token"]
                function_entry: EntryIdentificadores = self.find_table_entry(self.current_table_index, token)

                if (function_entry == None):
                    return False
                
                if function_entry.tipoRetorno != return_entry.tipoRetorno:
                    self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
                
            case "VECTOR":
                token = value_dict["token"]
                function_entry: EntryIdentificadores = self.find_table_entry(self.current_table_index, token)

                if (function_entry == None):
                    return False
                
                if function_entry.tipoRetorno != return_entry.tipoRetorno:
                    self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
               
            case "EXPRESSION":
                token = value_dict["token"]
                type_expression = self.indetify_expression_return(self.current_table_index, token)
                
                if (type_expression == None):
                    return False
                
                if return_entry.tipoRetorno in ["float", "integer", "boolean"]:
                    if type_expression not in ["float", "integer", "boolean"]:
                        self.throw_error("O tipo de retorno não corresponde ao tipo da função", token)
                    
                
                #print(token)


        #print(self.error_list)
                
        

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

    def util_is_attribute(self, reg_entry, attr_key):
        '''
        Função auxiliar para checar se um atributo existe em uma entrada da tabela de registro
        '''
        for e in reg_entry:
            if (attr_key in e.atributos): return True
        return False

    def util_is_register_access(self, prev_token, post_token):
        '''
        Função auxiliar usada para determinar se um
        '''
        entry = self.find_table_entry(self.current_table_index, prev_token)
        if (entry):
            reg_entry = self.get_register(dict(lexeme=entry.tipo))
            return bool(reg_entry) and bool(self.util_is_attribute(reg_entry, post_token['lexeme']))
        return False

    def validate_is_register_access(self, token_list):
        '''
        Verifica se a list de tokens acumaladas são usadas como parâmetros de accesso de um registro declarado. Usar essa função dentro de parser#register_position() e parser#register_access()
        É esperedo uma token_list do tipo: [TOKEN_IDENTIFIER, TOKEN_DOT, TOKEN_IDENTIFIER_1, ..., TOKEN_DOT, TOKEN_IDENTIFIER_N] -> identificador_register.identificador_atributo_1,.., .identificador_atributo_N
        '''

        is_analysis_ok = False
        try:
            for i, curr_token in enumerate(token_list):
                if "." in curr_token['lexeme']: 
                    prev_token = token_list[i - 1]
                    post_token = token_list[i + 1]
                    
                    is_analysis_ok = self.util_is_register_access(prev_token, post_token)
        except:
            is_analysis_ok = False

        if not is_analysis_ok:
            self.throw_error(f"Erro: Os tokens '{token_list}' não são tokens de acesso a um atributo de registro.", token_list[0])        

    def validate_body(self, token_list):
        #print(token_list)
        line = []
        on_for = False
        for token in token_list:
            if token['lexeme'] == 'for':
                on_for = True
            if token['lexeme'] == ';' and not on_for: 
                if line[0]['lexeme'] == 'write':
                    # verificar se existe
                    pass
                elif line[0]['lexeme'] == 'read':
                    # verificar se existe
                    pass
                else:
                    if self.is_increment(line):
                        # Variável NÃO atribuída
                        # self.validate_increment_decrement(line)
                        pass
                    elif self.is_function(line):
                        self.validate_function_parameters(line)
                    else:
                        # existe, mesmo tipo, Variável NÃO atribuída em expressões
                        # Chamada de função com identificador que não é uma função
                        # Usar o “.” e identificar que NÃO são registradores
                        # Usar [] em um identificador que não é vetor
                        pass
                self.printar_linha(line)
                line = []
            elif token['lexeme'] == '{':
                self.create_local_table()
                if line[0]['lexeme'] == 'for':
                    on_for = False
                    # chamada de função de verificação
                    # se vier sem integer tem que ser sido declarada antes e tem que ser do tipo inteiro
                    # se vier com o integer nao pode ter sido declarada
                    self.printar_linha(line)
                elif line[0]['lexeme'] in ['while', 'if']:
                    # o tipo tem que ser boolean
                    # chamada de função de verificação, Variável NÃO atribuída
                    # Chamada de função com identificador que não é uma função
                    # Usar o “.” e identificar que NÃO são registradores
                    # Usar [] em um identificador que não é vetor
                    self.printar_linha(line)
                line = []
            elif token['lexeme'] == '}':
                self.remove_local_table()
            else:
                line.append(token)