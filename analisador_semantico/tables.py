class EntryIdentificadores():
    def __init__(self, nome, tipo, valor=None, tipoRetorno=None, parametros=None, tamanho=0):
        self.nome = nome # nome da varíavael/função/constante -- vai salvar Constantes com: constants:nome_constante
        self.tipo = tipo # tipo, primitivo ou register, da variável
        self.valor = valor # Valor da variável
        self.tipoRetorno = tipoRetorno # Para entrys de funções
        self.parametros = parametros # ex: [int, int, float, bool]
        self.tamanho = tamanho # =0: variável, >0: vetor 
    
    def __repr__(self):
        pass
    
class EntryRegistradores():
    def __init__(self, nome, atributos):
        self.nome = nome
        self.atributos = atributos # {“nome atributo”: {tipo: “...”, “tamanho”: “...”} }

    def __repr__(self):
            pass

class TabelaPares():
    def __init__(self):
         self.tabela = []
         
    def adicionarPar(self, pai, tabelaIdentificadores: list[EntryIdentificadores]):
        novoPar = {
            "pai": pai, # índice da tabela "pai" da atual
            "tabela": tabelaIdentificadores # Tabela list[EntryIdentificadores]
        }
        
        self.tabela.append(novoPar)
    
    def __repr__(self):
            pass
        
