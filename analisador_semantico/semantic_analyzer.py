from analisador_semantico.tables import TabelaPares, EntryRegistradores, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = 0
        
        # Tabela de registradores
        self.registers_type_table: list[EntryRegistradores] = []

        # Tabela de pares
        self.pairs_table = TabelaPares()

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
    

    ################################ Tratamento de Erros Semânticos ################################

    def validate_is_register_access(self, token_list):
    	'''
    	Verifica se a list de tokens acumaladas são parâmetros de accesso de um registro. Usar essa função dentro de parser#register_position() e parser#register_access()
    	É esperedo uma token_list do tipo: [TOKEN_IDENTIFIER, TOKEN_DOT, TOKEN_IDENTIFIER_1, ..., TOKEN_DOT, TOKEN_IDENTIFIER_N] -> identificador_register.identificador_atributo_1,.., .identificador_atributo_N
    	'''
    	if (len(token_list) < 3): 
    		self.throw_error(f"Erro: Os tokens '{token_list}' não são tokens de acesso a um atributo de registro.", token_list)
    		return
    
    	is_analysis_ok = False
    	for i, curr_token in enumerate(token_list):
    		if i > 0 and i < len(token_list) - 2 and "." in curr_token['lexeme']: 
    			is_analysis_ok = (token_list[i - 1]['category'] == 'IDENTIFIER' and token_list[i + 1]['category'] == 'IDENTIFIER')
    
    	if not is_analysis_ok:
    		self.throw_error(f"Erro: Os tokens '{token_list}' não são tokens de acesso a um atributo de registro.", token_list)

    def verificar_chamada_funcao(self, token):
        """
        Verifica se um identificador chamado como função é de fato uma função.
        """
        entry = self.find_table_entry(self.current_table_index, token)
        if entry and entry.tipoRetorno is None:
            self.throw_error(f"Erro: Identificador '{token['lexeme']}' não é uma função.", token)

    def verificar_acesso_vetor(self, token):
        """
        Verifica se um identificador acessado como vetor é de fato um vetor.
        """
        entry = self.find_table_entry(self.current_table_index, token)
        if entry and entry.tamanho <= 1:
            self.throw_error(f"Erro: Identificador '{token['lexeme']}' não é um vetor.", token)
