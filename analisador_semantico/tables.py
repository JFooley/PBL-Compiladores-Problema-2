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
        return (f"\nEntryIdentificadores(nome={self.nome!r}, tipo={self.tipo!r}, "
                f"valor={self.valor!r}, tipoRetorno={self.tipoRetorno!r}, "
                f"parametros={self.parametros!r}, tamanho={self.tamanho!r}, "
                f"isConstant={self.isConstant!r})")
    
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
        pares_formatados = "\n\n".join(
            f"Pai: {par['pai']}, Tabela: {par['tabela']!r}" for par in self.tabela
        )
        return f"TabelaPares(\n{pares_formatados}\n)"
    
    def alterar_caracteristica_identificador(self, pai, nome_identificador, atributo, valor):
        variavel = None
        # Busca no escopo atual
        for identificador in self.tabela[pai]["tabela"]:
            if identificador.nome == nome_identificador:
                if hasattr(identificador, atributo):
                    setattr(identificador, atributo, valor)
                    return
        # Busca recursivamente no escopo pai até chegar na global, caso não tenha achado
        if variavel == None and pai> 0:
            self.alterar_caracteristica_identificador(self.tabela[pai]["pai"], nome_identificador, atributo, valor)