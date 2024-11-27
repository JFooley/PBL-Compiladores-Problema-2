from analisador_semantico.tables import TabelaPares, EntryRegistradores, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = -1
        
        # Tabela de registradores
        self.registers_type_table: list[EntryRegistradores] = []

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



    # Precisa analisar se já existe na tabela
    # Definir quando acaba o escopo da variável 
    def add_variables_to_table(self, is_global, token_list):
        variable_type = ""
        variable_name = ""
        variable_value = ""
        vector_length = 0
        for i in range(0, len(token_list)):
            token = token_list[i]
            if token['category'] == 'KEYWORD':
                variable_type = token['lexeme']
            
            elif token['category'] == 'IDENTIFIER':
                variable_name = token['lexeme']
            
            elif token['category'] == 'OPERATOR' and token['lexeme'] == '=':
                variable_value = token_list[i + 1]['lexeme']
            
            elif token['category'] == 'DELIMITER' and token['lexeme'] == '[':
                vector_length =  token_list[i + 1]['lexeme']
                    
            elif token['category'] == 'DELIMITER' and token['lexeme'] == ";":  # Encontrando o delimitador ';'
                variables_entry = EntryIdentificadores(variable_name, variable_type, variable_value, None, None, vector_length)
                self.create_local_table()
                self.pairs_table.tabela[0 if is_global == True else self.current_table_index]['tabela'].append(variables_entry)
                # Resetando as variáveis para a próxima variável
                variable_type, variable_name, variable_value = "", "", ""
                vector_length = []
    
    
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
    def add_registers_to_table(self,token_list):
        #percorrer a lista
        #verificar se o nome do registro já não está na tabela de simbolos, ou como constants
        #Declaração repetida entre 2 atributos dos registros;
        #Declação de vetor, se o identificador ou number do tamanho é int
        #criar na tabela global
        return
        
    def add_constants_to_table(self,token_list):
        tipo = token_list[0]
        nome = token_list[1] 
        valor = token_list[3]
        #Verificar se o identificador ja não existe como constante ou variaveis na tabela de simbolos
        #Verificar se o tipo primitivo é do mesmo valor adicionado
        #Se nenhum desses casos ser vdd, adicionar na tabela global
        return
    

    def add_variables_to_table(self,token_list):
        #Verificar se já existe variavel com mesmo nome na tabela de simbolos
        #verificar tipo e valor, quando tem atibuição;
        #Se for vetor, verificar se o tamanho é int(number ou identificador)
        #criar linha na tabela
        return

    def error_function_call(self,token_list):
        #Verificar erro se a função existe
        #Verificar erro dos parametros
        return
