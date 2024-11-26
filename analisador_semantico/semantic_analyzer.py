from analisador_semantico.tables import TabelaPares, EntryRegistradores, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = 0
        
        # Tabela de registradores
        self.registers_type_table: list[EntryRegistradores] = []

        # Tabela de pares
        self.pairs_table = TabelaPares()
        self.pairs_table.adicionarPar(-1, []) # Inicializa a tabela global

        # Lista de erros semânticos
        self.error_list = []

        self.tokens = []

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
        TabelaPares.adicionarPar(self.current_table_index, local_table)
        self.current_table_index = self.current_table_index + 1
    
    def create_global_table(self):
        global_table: list[EntryIdentificadores] = []
        TabelaPares.adicionarPar(self.current_table_index, global_table)
        self.current_table_index = 0
        
    def remove_local_table(self):
        if (self.current_table_index != 0) :
            self.pairs_table.pop(self.current_table_index)
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
        
        