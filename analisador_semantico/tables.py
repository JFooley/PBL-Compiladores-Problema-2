class EntryIdentificadores():
    def __init__(self, nome, tipo, valor=None, tipoRetorno=None, parametros=None, tamanho=0):
        self.nome = nome # nome da varíavael/função/constante
        self.tipo = tipo # tipo, primitivo ou register, da variável
        self.valor = valor # Valor da variável
        self.tipoRetorno = tipoRetorno # Para entrys de funções
        self.parametros = parametros # ex: [int, int, float, bool]
        self.tamanho = tamanho # =1: variável, >1: vetor 
    
    def __repr__(self):
        return f"Entry(nome={self.nome}, tipo={self.tipo}, valor={self.valor}, tipoR={self.tipoRetorno} )"

    
class EntryRegistradores():
    def __init__(self, nome, atributos):
        self.nome = nome
        self.atributos = atributos # {“nome atributo”: {tipo: “...”, “tamanho”: “...”} }

    def __repr__(self):
            return f"Entry(nome={self.nome}, tipo={self.atributos})"

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
        linhas = ["Tabela de Pares:"]
        for i, par in enumerate(self.tabela):
            linhas.append(f"Par {i + 1}:")
            linhas.append(f"  Pai: {par['pai']}")
            linhas.append(f"  Tabela Identificadores: {par['tabela']}")
        return "\n".join(linhas)
        
