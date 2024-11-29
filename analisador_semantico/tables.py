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
        return (f"EntryIdentificadores(nome={self.nome!r}, tipo={self.tipo!r}, "
                f"valor={self.valor!r}, tipoRetorno={self.tipoRetorno!r}, "
                f"parametros={self.parametros!r}, tamanho={self.tamanho!r}, "
                f"isConstant={self.isConstant!r})")
    
class EntryRegisters():
    def __init__(self, nome, atributos):
        self.nome = nome #nome dos registro
        self.atributos = atributos # {“nome atributo”: {tipo: “...” }  #não estamos permitindo vetor em register kkkk

    def __repr__(self):
        return f"EntryRegisters(nome={self.nome!r}, atributos={self.atributos!r})"

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
        return f"TabelaPares(tabela={self.tabela!r})"
        
