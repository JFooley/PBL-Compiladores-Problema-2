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
    
    def identify_var_kind(self, tokens): ## identifica qual tipo é a variável ou value passado e devolve só o token necessário
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
    
    def wrong_type_assign(self, current_table_index, variable, value):
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
                    
                    case "STRING":
                        if (variable_entry.tipo != "string"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)

                    case "CHARACTER":
                        if (variable_entry.tipo != "character"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)

                    case "BOOLEAN":
                        if (variable_entry.tipo != "boolean"):
                            self.throw_error(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)    

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

analizador = SemanticAnalyzer()
analizador.create_global_table()