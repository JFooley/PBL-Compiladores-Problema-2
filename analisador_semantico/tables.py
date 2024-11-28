class EntryIdentificadores():
    def __init__(self, nome, tipo, valor=None, tipoRetorno=None, parametros=None, tamanho=0, isConstant=False):
        self.nome = nome # nome da varíavael/função/constante
        self.tipo = tipo # tipo, primitivo ou register, da variável
        self.valor = valor # Valor da variável
        self.tipoRetorno = tipoRetorno # Para função e o tipo de atributo do regitro
        self.parametros = parametros # ex: [int, int, float, bool]
        self.tamanho = tamanho # =0: variável, >0: vetor 
        self.isConstant = isConstant
    
    def __repr__(self):
        pass
    
class EntryRegisters():
    def __init__(self, nome, atributos):
        self.nome = nome #nome dos registro
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
        
