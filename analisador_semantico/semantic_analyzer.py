from analisador_semantico.tables import TabelaPares, EntryRegistradores, EntryIdentificadores

class SemanticAnalyzer:
    def __init__(self):
        self.current_table_index = 0
        
        # Tabela de pares
        self.registers_type_table: list[EntryRegistradores] = []

        # Tabela de pares
        self.pairs_table = TabelaPares()

        # Lista de erros semânticos
        self.error_list = []

        # Index do scopo atual
        self.current_scope_index = 0

        self.tokens = []

    ################################ Funções auxiliares ################################
    def get_error_list(self):
        return self.error_list
    
    ## Gera um erro na lista de erros ## 
    def throw_erro(self, message, token):
        self.error_list.append({"position": token["line"], "message": message})

    ## Busca uma entrada específica na tabela designada ## 
    def find_variable_entry(self, target_table_index, token, throw_erro = True):
        for entry in self.pairs_table.tabela[target_table_index]["tabela"]:
            if entry.nome == token["lexeme"]:
                return entry
        
        if (throw_erro): self.throw_erro(f"{token["lexeme"]} não existe nesse escopo.", token)
        return None

    ################################ Funções de erro ################################
    def wrong_type_assign(self, current_table_index, variable, value):
        # Caso valor = variável
        if value["category"] == "IDENTIFIER":
            variable_entry: EntryIdentificadores = self.find_variable_entry(current_table_index, variable["lexeme"])
            value_entry: EntryIdentificadores = self.find_variable_entry(current_table_index, value["lexeme"])

            if (variable_entry == None or value_entry == None):
                return False
            
            else:
                if (variable_entry.tipo != value_entry.tipo):
                    self.throw_erro(f"{value_entry.tipo} não pode ser convertido em {variable_entry.tipo}.", value)

        # Caso valor = literal
        else:
            variable_entry: EntryIdentificadores = self.find_variable_entry(current_table_index, variable["lexeme"])
            
            if (variable_entry == None):
                return False
            else:
                match value["category"]:
                    case "NUMBER":
                        if (variable_entry.tipo != "float" and variable_entry.tipo != "integer" and ("." in value["lexeme"] and variable_entry.tipo == "integer")):
                            self.throw_erro(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)
                    
                    case "STRING":
                        if (variable_entry.tipo != "string"):
                            self.throw_erro(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)

                    case "CHARACTER":
                        if (variable_entry.tipo != "character"):
                            self.throw_erro(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)

                    case "BOOLEAN":
                        if (variable_entry.tipo != "boolean"):
                            self.throw_erro(f"{value["category"]} não pode ser convertido em {variable_entry.tipo}.", value)
        return True
    
    def repeated_statement(self, current_table_index, new_variable):
        new_variable_entry: EntryIdentificadores = self.find_variable_entry(current_table_index, new_variable["lexeme"], throw_erro= False)
        
        if (new_variable_entry != None):
            self.throw_erro(f"{new_variable["lexeme"]} já existe neste escopo.", new_variable)
            return False
        else:
            return True
