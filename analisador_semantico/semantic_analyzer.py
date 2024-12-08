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

        # Cria tabela global
        self.create_global_table()

        self.last_function_type = ""

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
            selected_entry = self.find_table_entry(self.pairs_table.tabela[target_table_index]["pai"], token, False)
        
        # Causa erro se necessário
        if (throw_erro and selected_entry == None): self.throw_error(f"O {token['lexeme']} não existe nesse escopo.", token)

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
    
    def is_int(self,token):
        return "." not in token["lexeme"]
    
    def is_expression(self, tokens):
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
    
    #Separa a lista de token em partes por um delimitador
    def split_list_token(self,token_list,delimiter):
        result = []
        current_segment = []

        for token in token_list:
            if token['lexeme'] == delimiter:
                result.append(current_segment)
                current_segment = []
            else:
                current_segment.append(token)
        
        if current_segment:
            result.append(current_segment)

        return result

    def get_concatenated_lexemes(self,token_list):
        value = ""
        for token in token_list:
            value = value + " " + token["lexeme"]
        return value

    def split_list_token_write(self,token_list,delimiter):
        result = []
        current_segment = []
        open_parentheses = False

        for token in token_list:
            if token['lexeme'] == "(":
                open_parentheses = True
            elif token['lexeme'] == ")":
                open_parentheses = False

            if token['lexeme'] == delimiter and not open_parentheses:
                result.append(current_segment)
                current_segment = []
            else:
                current_segment.append(token)
        
        if current_segment:
            result.append(current_segment)

        return result
    
    def get_index_vector(self, token_list): #deve passar a[5][5] por exemplo
        result = []
        for i in range(len(token_list) - 1):
                if token_list[i]['lexeme'] == "[":
                    result.append(token_list[i+1])
        return result

################################ Funções de Adicionar na tabela ################################

    # verificar se ja nao existe um id com o mesmo nome
    # chamar função que verifica se a função retorna algo
    def add_function_to_table(self, token_list):
        if self.find_table_entry(0, token_list[1], False) != None:
            self.throw_error(f"{token_list[1]['lexeme']} já foi declarada", token_list[1])
            return
        
        return_type = token_list[0]['lexeme']
        self.last_function_type = token_list[0]
        function_name = token_list[1]['lexeme']
        parameters_list = []
        parameters_type_list = []
        i = 3
        while i < len(token_list):
            parameters_list.append(token_list[i])
            parameters_list.append(token_list[i+1])
            parameters_list.append({ "lexeme": "=","category": "OPERATOR","line": token_list[i]["line"]})
            parameters_list.append({ "lexeme": "None","category": "KEY-WORD","line": token_list[i]["line"]})
            parameters_list.append({ "lexeme": ";","category": "DELIMITER","line": token_list[i]["line"]})
            parameters_type_list.append(token_list[i]['lexeme'])
            i += 3
        function_entry = EntryIdentificadores(function_name, 'function', None, return_type, parameters_type_list, 0)
        self.pairs_table.tabela[0]['tabela'].append(function_entry)

        return parameters_list

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
        
        if self.wrong_type_assign(self.current_table_index,[name],value_list,type) == False: #Verificar se o tipo primitivo é do mesmo valor adicionado
            return 
        
        if(size_error == len(self.error_list)):
            constant_entry = EntryIdentificadores(name["lexeme"], type["lexeme"], value, None, None, 0, True)
            self.pairs_table.tabela[0]['tabela'].append(constant_entry)

    
       
    
    
    def add_variables_to_table(self, is_global, token_list):
        variable_type = ""
        variable_name = ""
        vector_length = []
        value_list = []
        values = ""
        consume_values = False
        for i in range(0, len(token_list)):
            token = token_list[i]
            
            
            if token['category'] == 'KEYWORD':  #obs: o tipo pode ser tbm identifier, que é o caso de ser um register
                if(token['lexeme'] not in ['true', "false"]):
                    variable_type = token
                else:
                    if(consume_values==True):
                        value_list.append(token)
                        values = values + token["lexeme"]
            
            elif token['category'] == 'IDENTIFIER': # Falta verificar os registers
                if token_list[i + 1]['category'] == "IDENTIFIER":
                    variable_type = token
                elif token_list[i+1]['lexeme'] != ']':
                    variable_name = token   
            
            elif token['category'] == 'OPERATOR' and token['lexeme'] == '=': # consumir tudo até o ;
                consume_values = True
            
            elif token['category'] == 'DELIMITER' and token['lexeme'] == '[': # verificar se é um vector ou matriz
                vector_length.append(token_list[i + 1])
                    
            elif token['category'] == 'DELIMITER' and token['lexeme'] == ";":  # Encontrando o delimitador ';'
                consume_values = False
                error = len(self.error_list)
                self.repeated_statement(self.current_table_index,variable_name)#Verifica se o identificador ja não existe como constante ou variaveis na tabela de simbolos
                 
                # Atribuição de valor
                if not len(value_list) == 0:
                    self.wrong_type_assign(self.current_table_index,[variable_name],value_list,variable_type)
                    
                    #TODO Talvez nao é necessario pq o sintatico da erro
                    if (variable_type['category'] == "IDENTIFIER"):
                        if error == len(self.error_list):
                            register = [variable_type, variable_name, {"lexeme":"=", "category":"DELIMITER", "line":variable_name["line"]}].extend(value_list).append({"lexeme":";", "category":"DELIMITER", "line":variable_name["line"]})
                            self.add_register_instance_to_table(register)
                    else:
                        if error == len(self.error_list):
                            variables_entry = EntryIdentificadores(variable_name['lexeme'], variable_type['lexeme'], values , None, None, vector_length if vector_length != [] else 0)
                            self.pairs_table.tabela[0 if is_global == True else self.current_table_index]['tabela'].append(variables_entry)
              
                    value_list = []
                    values = ""
                    
                # Declaração de variável
                else:
                    error_size = len(self.error_list)
                    vector_size = []
                    if (vector_length != []): # No caso é um vetor 
                        for index in vector_length:
                            self.error_vector_size(index) # Verifica se o indice do vetor é int ou identifier
                        if(error_size == len(self.error_list)):
                            for item in vector_length:
                                vector_size.append(item['lexeme'])
                        else: 
                            return
                    elif (variable_name['category']== "IDENTIFIER" and variable_type['category'] == "IDENTIFIER"):
                        self.add_register_instance_to_table([variable_type, variable_name])
                        variable_type = ""
                        
                    if variable_type != "": # Verifica se não é um registrador, caso não seja adiciona na tabela de símbolos
                        variables_entry = EntryIdentificadores(variable_name['lexeme'], variable_type['lexeme'], None , None, None, vector_size if vector_size != [] else 0)
                        self.pairs_table.tabela[0 if is_global == True else self.current_table_index]['tabela'].append(variables_entry)
                        variable_type, variable_name, variable_value = "", "", ""
                        vector_length = []
                        value_list = []
                        values = ""
            else: # Consome tudo o que não fizer parte de nome ou tipo da variável
                if consume_values == True:
                    value_list.append(token)
                    values = values + token["lexeme"]
                
                
    ################################ Funções de erro ################################

    def identify_expression_return(self, current_scope_index, tokens: list):
        ## Identifica se a expressão aritimética passada é do tipo aritimética (retorna apenas number) ou do tipo logica/relacional (retorna boolean)
        ## A função da throw nos erros caso alguma das variáveis não existam ou sejam string e retorna None caso tenha falhado
        ## Caso não tenha falhado, ela vai retornar o tipo do retorno da expressão (number ou boolean)
        type = ["float", "integer"]
        
        # Encontra o tipo da função
        for token in tokens:
            if token["category"] == "OPERATOR" and token["lexeme"] != "." and token["lexeme"] in ["&&", "||", '>', '<', '!=', '>=', '<=', '==']:
                type = ["boolean"]
                break

        # Valida os atributos (se existem, se foi inicializado e são diferentes de string)
        variable_tokens = []
        for token in tokens:
            if (token["category"] == "OPERATOR" and token["lexeme"] != ".") or token == tokens[-1]:
                if (token == tokens[-1]): variable_tokens.append(token) # Caso do ultimo token

                variable = self.get_variable_type(variable_tokens)
                if variable["tipo"] == "IDENTIFIER" or variable["tipo"] == "REGISTER" or variable["tipo"] == "VECTOR":
                    variable_entry: EntryIdentificadores = self.find_table_entry(current_scope_index, variable["token"][0])

                    if variable_entry == None:
                        return None
                    
                    if variable["tipo"] == "VECTOR":  # Usar [] em um identificador que não é vetor
                        if (variable_entry.tamanho == [] or variable_entry.tamanho == 0):
                            self.throw_error(f"A variável {variable_entry.nome} não é um vetor",variable["token"][0])
                            return None
                        
                        #Verifica se o vetor tem index correto
                        index_list = self.get_index_vector(variable_tokens)
                        if index_list == None:
                            return None
                        
                        for index in index_list:
                            if self.error_vector_size(index):
                                return None
                    
                    if variable_entry.tipo not in ["integer", "float", "boolean"]:
                        self.throw_error(f"O tipo {variable_entry.tipo} não pode ser operado em uma expressão", variable["token"][0])
                        return None
                    
                    if variable["tipo"] != "VECTOR" and variable_entry.valor == None: #Valida se foi inicializada
                        self.throw_error(f"A variável {variable_entry.nome} não foi inicializada", token)
                        return None
                    
                elif variable["tipo"] == "FUNCTION CALL":
                    variable_entry: EntryIdentificadores = self.find_table_entry(current_scope_index, variable["token"][0])
                
                    if variable_entry == None:
                        return None
                    
                    if variable_entry.tipo != "function": #Verifica se chamada de função está com identificador que não é uma função
                        self.throw_error(f"{variable_entry.nome} não é uma função", variable["token"][0])
                        return None

                    if variable_entry.tipoRetorno not in ["integer", "float", "boolean"]:
                        self.throw_error(f"O tipo {variable_entry.tipoRetorno} não pode ser operado em uma expressão", variable["token"][0])
                        return None
                
                    self.validate_function_parameters(variable_tokens)  #valida os parametros
                
                elif variable["tipo"] == "LITERAL":
                    if variable["token"][0]["category"] == "STRING":
                        self.throw_error("String não pode compor expressão.", variable["token"][0])
                        return None

                variable_tokens.clear()

            else:
                variable_tokens.append(token)
        return type
        
    def get_variable_type(self, tokens: list): ## identifica qual tipo é a variável ou value passado e devolve o tipo e o token necessário
        if tokens == None or tokens == []:
            return None
        # Trata os parenteses
        if tokens[0]["lexeme"] == "(": 
            tokens.pop(0) ## Remove os parenteses do início

        if tokens[-1]["lexeme"] == ")" and tokens[1]["lexeme"] != "(":
            tokens.pop(-1) ## Remove os parenteses inúteis do final (que não são os da cahamada de função)
        
        if len(tokens) == 1:
            ## Identifier
            if tokens[0]["category"] == "IDENTIFIER":
                return {"tipo":"IDENTIFIER", "token": tokens}
            ## Literal
            else:                    
                return {"tipo":"LITERAL", "token": tokens}
            
        else:
            ## Expresion
            if self.is_expression(tokens):
                return {"tipo":"EXPRESSION", "token": tokens}
            ## Register
            if tokens[1]["lexeme"] == ".":
                new_lexeme = ""
                for token in tokens:
                    if token["lexeme"] == "[":
                        break
                    new_lexeme += token["lexeme"]

                new_tokens = [{"lexeme": new_lexeme, "category": tokens[0]["category"], "line": tokens[0]["line"]}]
                return {"tipo":"REGISTER", "token": new_tokens}
            
            ## Function call
            elif self.is_function(tokens):
                return {"tipo":"FUNCTION CALL", "token": tokens} 

            ## Vector
            elif tokens[1]["lexeme"] == "[":
                value_entry: EntryIdentificadores = self.find_table_entry(self.current_table_index, tokens[0])
                if (value_entry != None and value_entry.tamanho == 0):
                    return None                
                return {"tipo":"VECTOR", "token": tokens}

    def wrong_type_assign(self, current_table_index, variable, value, variable_type = None): 
        ## Identifica em uma atribuição variable = value se o tipo de a é diferente do tipo de b
        ## variable: lista de tokens do objeto varible (ex: "identifier" ou "identifier" "." "identifier" ou "identifier" "[" "number" "]" e etc)
        ## value: lista de tokens do objeto value (ex: "identifier" ou "identifier" "." "identifier" ou "identifier" "[" "number" "]" e "identnfier" "(" ")")

        variable_dict = self.get_variable_type(variable)
        value_dict = self.get_variable_type(value)

        if variable_dict == None or value_dict == None: return None

        variable = variable_dict["token"]
        value = value_dict["token"]

        
        ## Atribuição de valor a variavel existente
        if variable_type == None: 
            variable_entry: EntryIdentificadores = self.find_table_entry(current_table_index, variable[0])
            

            if variable_entry == None:
                return False
        
            if variable_entry.isConstant:
                self.throw_error(f"{variable[0]["lexeme"]} é uma constante, não pode ter seu valor alterado.", variable[0])
                return False
            match value_dict["tipo"]:
                case "IDENTIFIER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])

                    if (value_entry == None):
                        return False
                    
                    if ((variable_entry.tipo == "float" or variable_entry.tipo == "integer") and value_entry.tipo == "string") or (variable_entry.tipo == "string" and value_entry.tipo != "string"):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value[0])
                        return False

                case "LITERAL": 
                    match value[0]["category"]:
                        case "NUMBER":
                            if (variable_entry.tipo == "string" or variable_entry.tipo == "character"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_entry.tipo}.", value[0])
                                return False
                        
                        case "STRING":
                            if (variable_entry.tipo != "string"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_entry.tipo}.", value[0])
                                return False

                        case "CHARACTER":
                            if (variable_entry.tipo != "character"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_entry.tipo}.", value[0])
                                return False

                        case "BOOLEAN":
                            if (variable_entry.tipo == "string" or variable_entry.tipo == "character"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_entry.tipo}.", value[0])    
                                return False
                        
                        
                       
                            

                case "REGISTER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])
                
                    if (value_entry == None):
                        return False

                    if (variable_entry.tipo != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value[0])
                        return False

                case "VECTOR":         
                    index_list = self.get_index_vector(value)

                    if index_list == None:
                        return None
                    
                    for index in index_list:
                        if self.error_vector_size(index):
                            return None
                    
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])
                    

                    if (value_entry == None):
                        return False
                    
                    if (value_entry.tamanho == 0):
                       
                        self.throw_error(f"{value[0]['lexeme']} não é um vator e por isso não pode posições acessadas.", value[0])
                        return False

                    if (variable_entry.tamanho == 0):
                        self.throw_error(f"{variable[0]['lexeme']} ", value[0])
                        return False

                    if (variable_entry.tipo != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value[0])
                        return False

                case "FUNCTION CALL":
                    self.validate_function_parameters(value)
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])

                    if (value_entry == None):
                        return False

                    if (variable_entry.tipo != value_entry.tipoRetorno or variable_entry.tamanho != value_entry.tamanho):                        
                        self.throw_error(f"{value_entry.tipoRetorno} não pode ser convertido em {variable_entry.tipo}.", value[0])
                        return False

                case "EXPRESSION":
                    value_type = self.identify_expression_return(self.current_table_index, value)
                    
                    if value_type == None:
                        return False

                    if variable_entry.tipo not in value_type:
                        self.throw_error(f"{value_type} não pode ser convertido em {variable_entry.tipo}.", value[0])
                        return False
        
        ## É declaração
        else:
             match value_dict["tipo"]:
                case "IDENTIFIER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])

                    if (value_entry == None):
                        return False
                        
                    if ((variable_type["lexeme"] == "float" or variable_type["lexeme"] == "integer") and value_entry.tipo == "string") or (variable_type["lexeme"] == "string" and value_entry.tipo != "string"):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_type["lexeme"]}.", value[0])
                        return False

                case "LITERAL":
                    match value[0]["category"]:
                        case "NUMBER":
                            if (variable_type["lexeme"] == "string" or variable_type["lexeme"] == "character"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value[0])
                                return False
                        
                        case "STRING":
                            if (variable_type["lexeme"] != "string"):
                                self.throw_error(f"{value[0]['category']} não pode ser convertido em {variable_type['lexeme']}.", value[0])
                                return False

                        case "CHARACTER":
                            if (variable_type["lexeme"] != "character"):
                                self.throw_error(f"{value[0]['category']} não pode ser convertido em {variable_type['lexeme']}.", value[0])
                                return False

                        case "BOOLEAN":
                            if (variable_type["lexeme"] == "string" or variable_type["lexeme"] == "character"):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value[0])    
                                return False
                            
                        # Quando os valores forem true or false
                        case "KEYWORD":
                            if(value[0]['lexeme'] not in ['true', 'false']):
                                self.throw_error(f"{value[0]["category"]} não pode ser convertido em {variable_type["lexeme"]}.", value[0])    
                                return False
                       

                case "REGISTER":
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])
                
                    if (value_entry == None):
                        return False

                    if (variable_type["lexeme"] != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_type['lexeme']}.", value)
                        return False

                case "VECTOR":
                    index_list = self.get_index_vector(value)

                    if index_list == None:
                        return None
                    
                    for index in index_list:
                        if self.error_vector_size(index):
                            return None       
                           
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])

                    if (value_entry == None):
                        return False
                    
                    if (value_entry.tamanho == 0):
                        self.throw_error(f"{value[0]['lexeme']} não é um vator e por isso não pode posições acessadas.", value[0])
                        return False
                    
                    if (variable_type["lexeme"] != value_entry.tipo):
                        self.throw_error(f"{value_entry.tipo} não pode ser convertido em {variable_type['lexeme']}.", value[0])
                        return False
                    
                    

                case "FUNCTION CALL":
                    self.validate_function_parameters(value)
                    value_entry: EntryIdentificadores = self.find_table_entry(current_table_index, value[0])

                    if (value_entry == None):
                        return False

                    if (variable_type["lexeme"] != value_entry.tipoRetorno):
                        self.throw_error(f"{value_entry.tipoRetorno} não pode ser convertido em {variable_type['lexeme']}.", value[0])
                        return False

                case "EXPRESSION":
                    value_type = self.identify_expression_return(self.current_table_index, value)
                    
                    if value_type == None:
                        return False

                    if variable_type["lexeme"] not in value_type:
                        self.throw_error(f"{value_type} não pode ser convertido em {variable_type['lexeme']}.", value[0])
                        return False

        return True

    def repeated_statement(self, current_table_index, new_variable):
        ## Verifica se a variável definida pelo token new_variable já foi declarada
        ## new_variable: token do objeto que vai ser declarado
        # tst

        ## Verifica se a variável existe no escopo
        if (self.find_table_entry(current_table_index, new_variable, throw_erro= False) != None):
            self.throw_error(f"{new_variable['lexeme']} já existe neste escopo.", new_variable)
            return False

        ## Verifica se ele não possui um nome igual a de um tipo primitivo
        if (new_variable["lexeme"] in ["float", "integer", "string", "character", "boolean"]):
            self.throw_error(f"{new_variable['lexeme']} não pode ter o nome de um tipo primitivo.", new_variable)
            return False

        ## Verifica se ele não possui um nome igual a de um tipo register
        for key in self.registers_type_table.keys():
            if key == new_variable["lexeme"]:
                self.throw_error(f"{new_variable['lexeme']} não pode ter o nome de um tipo de registro.", new_variable)
                return False
        
        return True


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
        
        other_func_call = [] # token_list para validar chamadas de função nos parametros
        is_func = False
        # Retira da lista de tokens acumulados apenas os tokens referentes aos argumentos passados na chamda
        function_call_arguments = []
        i = 1
        while i < len(token_list):
            if is_func:
                other_func_call.append(token_list[i])
                if token_list[i]['lexeme'] == ')':
                    self.validate_function_parameters(other_func_call)
                    other_func_call = []
                    is_func = False
            else:
                if token_list[i]['lexeme'] == '(' or token_list[i]['lexeme'] == ',':
                    if token_list[i+2]['lexeme'] == '.': # caso seja um objeto o id depois do . importa
                        function_call_arguments.append([])
                    else:
                        if token_list[i+2]['lexeme'] == '(':
                            is_func = True
                        function_call_arguments.append(token_list[i+1])

                if type(function_call_arguments[-1]) == list and token_list[i]['category'] == 'IDENTIFIER':
                    function_call_arguments[-1].append(token_list[i])

            i += 1
            

        if len(function_call_arguments) != len(function_entry.parametros):
            self.throw_error(f"{token_list[0]['lexeme']} espera {len(function_entry.parametros)} parametro(s), mas recebeu {len(function_call_arguments)}", token_list[0])
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
                if entry == None:
                    return
                else:
                    arguments_types.append(entry.tipoRetorno)
            elif function_call_arguments[i]['category'] == 'NUMBER':
                if '.' in function_call_arguments[i]['lexeme']: #TODO Já existe a função is_int
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
        value = ""
        value_list = []
        # Verificar se só tem apenas o return na lista
        if len(token_list) == 1:
            if self.last_function_type != None and self.last_function_type['lexeme'].lower() != "empty":
                self.throw_error("O retorno da função está vazio", token_list[0])
                return
            else:
                return
        else:
            for token in token_list[1:len(token_list)]:
                value = value + " " + token["lexeme"]
                value_list.append(token)
     
        size_error = len(self.error_list)
        if(self.last_function_type != None and self.last_function_type['lexeme'] == "empty" and len(value_list) > 0): # verifica se tem empty e recebe return + alguma coisa
            self.throw_error("A função deve retornar vazio", token_list[0])
        else:
            if(size_error == len(self.error_list)):
                return_entry = self.wrong_type_assign(self.current_table_index,[{"lexeme":"valid", "category":"STRING", "line":value_list[0]["line"]}],value_list,self.last_function_type)
                if return_entry == False:
                    return
        
    # Chamada dentro ou após a adição da função na tabela
    def validate_consistent_return(self, token_list):
        function_name = token_list[1]['lexeme']
        
        if any(token['lexeme'] == "return" for token in token_list) == True:
            # valida o retorno da função
            # self.validate_function_return(token_list)
            print()
        else:
            self.throw_error(f"A função {function_name} não possui retorno", token_list[1])
            
                
        

    #################### Função para validar o incremento ou decremento  ####################
     #AJUSTES NECESSÁRIO:
    #precisa verifica se variável não foi inicializada
    #Precisa verificar se a variavel existe (falta testar)
    #Se a variavel for um vetor sem passar as posições é erro: por exemplo, vetor v, não pode fazer v++
    #Se a varivel for um vetor, pode fazer incremento, desde que o vetor seja inteiro

    #PRECISA ACUMULAR TODOS OS TOKENS ATÉ ENCONTRAR O "++" ou "--"
    def validate_increment_decrement(self, token_list: list):
        if (token_list[0]["category"] == "IDENTIFIER" and  token_list[1]['lexeme'] in ['++', '--']):
            token_entry = self.find_table_entry(self.current_table_index, token_list[0])
            token = token_list[0]
            if token_entry == None:
                return
            if token_entry.valor == None and (token_entry.tamanho == [] or token_entry.tamanho == 0): #variavel não inicializada
                self.throw_error(f"A variável {token_entry.nome} não foi inicializada", token)
                return
            if token_entry.tipo != "integer": # Para variável, register e vetor, deve ser do tipo inteiro
                self.throw_error(f"A variável {token_entry.nome} não é do tipo inteiro", token)
                return
            if token_entry.isConstant:  # Não pode ser uma constante
                self.throw_error(f"A variável {token_entry.nome} é uma constante. Não é possível alterar o valor de constantes.", token)
                return
            if ((token_entry.tamanho != [] and token_entry.tamanho != 0)): # incremento direto na matriz ou vetor
                    self.throw_error(f"A Variável não é do tipo inteiro. A variável '{token_entry.nome}' é um vetor ou matriz", token)  # matriz ou vetor sem [] ou [][]
                    return


        else:
            identifier = []
            for token in token_list:
                if token['lexeme'] in ["++", "--"]: 
                    break  
                identifier.append(token) 
        
            variable = self.get_variable_type(identifier)
            token_entry = self.find_table_entry(self.current_table_index, variable["token"][0])
            if token_entry == None:
                return
            
            if variable["tipo"] == "VECTOR":
                if (token_entry.tamanho == [] or token_entry.tamanho == 0): # Usar [] em um identificador que não é vetor
                    self.throw_error(f"A variável {token_entry.nome} não é um vetor",variable["token"][0])
                    return      
                #Verifica se o vetor tem index correto
                index_list = self.get_index_vector(identifier)
                if index_list == None:
                    return 
                for index in index_list:
                    if self.error_vector_size(index):
                        return 
            elif variable["tipo"] == "IDENTIFIER" or variable["tipo"] == "REGISTER":
                if token_entry.valor == None: #variavel não inicializada
                    self.throw_error(f"A variável {token_entry.nome} não foi inicializada", variable["token"][0])
                    return
                if token_entry.tipo != "integer": # Para variável, register e vetor, deve ser do tipo inteiro
                    self.throw_error(f"A variável {token_entry.nome} não é do tipo inteiro", variable["token"][0])
                    return
            
        

    #------------------------------ Metas Estéfane e felipe -----------------------------------
    def error_vector_size(self,token):
        if (token["category"] == "NUMBER" and not self.is_int(token)):
            self.throw_error("O indíce do vetor deve ser inteiro", token)
            return True
        elif (token["category"] == "IDENTIFIER"):
            object = self.find_table_entry(self.current_table_index,token)
            if (object == None):
                return True
            if (object != None and not object.tipo == "integer"):
                self.throw_error("O indíce do vetor deve ser inteiro", token)   
                return True
        return False


    def error_has_value(self,token):
        object = self.find_table_entry(self.current_table_index,token)
        if(object != None and object.valor == None):
            self.throw_error(f"A variável {object.nome} não foi inicializada", token)
            True
        False


    def validate_body(self, token_list): 
        line = []
        on_for = False
        on_return = False
        for token in token_list:
            if token['lexeme'] == 'for':
                on_for = True
            if token['lexeme'] == ';' and not on_for: 
                if line[0]['lexeme'] == 'write':
                    self.validate_write(line[2:-1])
                elif line[0]['lexeme'] == 'read':
                    self.validate_read(line[2:-1])
                elif line[0]['lexeme'] == 'return':
                    on_return = True
                    self.validate_function_return(line) # line linha escrita return, sem ;
            
                else:
                    if self.is_increment(line):
                        self.validate_increment_decrement(line)
                    elif self.is_function(line):
                        self.validate_function_parameters(line)
                        on_return = False
                    else:
                        self.validate_assignment(line)
                        #validar os parametros de função
                        # existe, mesmo tipo, Variável NÃO atribuída em expressões(error_has_value)
                        # Chamada de função com identificador que não é uma função
                        # Usar o “.” e identificar que NÃO são registradores
                        # Usar [] em um identificador que não é vetor(em declaração (2 lados da igualdade), em expressoes aritméticas)
                        #Verificar se o identificador passado como index do vetor é inteiro (error_vector_size)
                line = []
            
            elif token['lexeme'] == '{':
                self.create_local_table()
                
                if line[0]['lexeme'] == 'for':
                    on_for = False
                    self.validate_for(line)
                elif line[0]['lexeme'] == 'while':
                    self.validate_conditional(line[2:-1])
                elif line[0]['lexeme'] == 'if':
                    self.validate_conditional(line[2:-2])    

                line = []               
                
            
            elif token['lexeme'] == '}':                
                self.remove_local_table()
            else:                
                line.append(token)
        if(self.last_function_type != None):
            if(on_return == False and self.last_function_type['lexeme'] != "empty"):
                self.throw_error(f"A função exige um retorno",self.last_function_type)
        print(token_list)

        # print("\n--------------- tabelas locais e global---------------")
        # print(self.pairs_table)
        
 #----------------------- Valida o while e if ----------------------------
    def validate_conditional(self,token_list):
        # verifica se o tipo tem que ser boolean
        type = self.identify_expression_return(self.current_table_index, token_list)

        if type != None and "boolean" not in type:
            self.throw_error(f"O resultado da expressão não é do tipo boolean",token_list[0])
                    
        # chamada de função de verificação, Variável NÃO atribuída (error_has_value) (ok)
        # Chamada de função com identificador que não é uma função (ok)
        # Usar o “.” e identificar que NÃO são registradores (ok)
        # Usar [] em um identificador que não é vetor (em declaração (2 lados da igualdade), em expressoes aritméticas) (ok)
        #Verificar se o identificador passado como index do vetor é inteiro (error_vector_size) (ok)
        #validar os parametros da função (ok)
        
 #---------------------- Valida assignment ------------------------------
    def validate_assignment(self,token_list):
    #validar os parametros de função
    # existe, mesmo tipo, Variável NÃO atribuída em expressões(error_has_value)
    # Chamada de função com identificador que não é uma função
    # Usar o “.” e identificar que NÃO são registradores (ok)
    # Usar [] em um identificador que não é vetor(em declaração (2 lados da igualdade), em expressoes aritméticas)
    #Verificar se o identificador passado como index do vetor é inteiro (error_vector_size)
    #Verificar se não está atribuindo a uma constant
        assignment_list = self.split_list_token(token_list,"=")
        
        if assignment_list == None : return 
        name_list = assignment_list[0]
        value_list = assignment_list[1]
        
        
        if self.wrong_type_assign(self.current_table_index,name_list,value_list) == True: #Verificar se o tipo primitivo é do mesmo valor adicionado
            value = self.get_concatenated_lexemes(value_list)

            variable = self.get_variable_type(name_list)
           
           
            
            if (variable != None and variable["tipo"] != "VECTOR"):
                self.pairs_table.alterar_caracteristica_identificador(self.current_table_index,variable["token"][0]["lexeme"],"valor",value)
        else: # Erro no tipo, não é vetor 
            variable = self.get_variable_type(name_list)
            brakets = any(token['lexeme']=='[' for token in name_list)
         
            if variable == None and brakets:
                self.throw_error(f"{name_list[0]['lexeme']} não é um vetor e por isso não pode ter posições acessadas.", name_list[0])

 #------------------------- Valida erro no for ------------------
    def validate_for(self,token_list):
        list_for = self.split_list_token(token_list,";")
        size_error = len(self.error_list)
        #Primeira parte do for
        first_part = list_for[0]
        if (first_part[2]["category"] == "KEYWORD"):
            value_list = []
            value = ""
            type = first_part[2]
            name = first_part[3]
            self.repeated_statement(self.current_table_index,name) #Verifica se o identificador ja não existe como constante ou variaveis na tabela de simbolos
            
            for token in first_part[5:len(first_part)]:
                value_list.append(token)
                value = value + " " + token["lexeme"]
            self.wrong_type_assign(self.current_table_index,[name],value_list,type) #Verificar se a igualdade é do tipo integer
            
            if(size_error == len(self.error_list)):
                variable_entry = EntryIdentificadores(name["lexeme"], type["lexeme"], value)
                self.pairs_table.tabela[self.current_table_index]['tabela'].append(variable_entry)
        elif (first_part[2]["category"] == "IDENTIFIER"):
            name = first_part[2]
            self.error_conditional_for(name,first_part,4)

        #Verifica segunda parte do for
        second_parte = list_for[1]
        if(size_error == len(self.error_list)):
            name = second_parte[0]
            self.error_conditional_for(name,second_parte,2)
        
        #Verifica terceira parte
        if(size_error == len(self.error_list)):
            self.validade_third_part(list_for[2][0])

    def validade_third_part(self,token):
        entry = self.find_table_entry(self.current_table_index,token)
        if entry != None and entry.tipo != "integer":
            self.throw_error(f"A váriavel {token['lexeme']} não é do tipo integer.",token)
    
    #Verifica se a variavel existe, se é inteira e se o valor depois da igualdade é inteiro
    def error_conditional_for(self,name_token,token_list,index):
        if(len(token_list)>0):
            value_list = []
            entry = self.find_table_entry(self.current_table_index,name_token)
            if entry == None:
                return True
            if entry.tipo != "integer":
                self.throw_error(f"A váriavel {name_token['lexeme']} não é do tipo integer.",name_token)
                return True
            for token in token_list[index:len(token_list)]:
                value_list.append(token)

            if self.wrong_type_assign(self.current_table_index,[name_token],value_list) == False:
                return True
            return False
        else:
            return False
    
    #----------------------- Valida read ----------------------------
    def validate_read(self,token_list):
        list_parameters = self.split_list_token(token_list,",")
        if (len(list_parameters)>0):
            for parameters in list_parameters:
                token = self.get_variable_type(parameters)
                entry = self.find_table_entry(self.current_table_index,token["token"][0])
                if (token["tipo"] == "VECTOR" and entry != None):
                    if (entry.tamanho == [] or entry.tamanho == 0):
                        self.throw_error(f"A variável {entry.nome} não é um vetor",token["token"][0])
    
    #----------------------- Valida Write ----------------------------
    def validate_write(self,token_list):
        list_parameters = self.split_list_token_write(token_list,",")
        if (len(list_parameters)>0):
            for parameters in list_parameters:
                token = self.get_variable_type(parameters)
                if (token["tipo"] == "EXPRESSION"):
                    self.identify_expression_return(self.current_table_index,token["token"])
                elif (token["tipo"] == "FUNCTION CALL"):
                    self.validate_function_parameters(parameters)
                elif (token["tipo"] != "LITERAL"):
                    entry = self.find_table_entry(self.current_table_index,token["token"][0])
                    if (token["tipo"] == "VECTOR" and entry != None):
                        if (entry.tamanho == [] or entry.tamanho == 0):
                            self.throw_error(f"A variável {entry.nome} não é um vetor",token["token"][0])
