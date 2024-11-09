class SemanticAnalyzer:
    def __init__(self):
        '''
            dict(
                parent=integer(referência de escopo),
                dict(
                    name=string, 
                    type=string(function, register, tipos_primitivos)
                    value=any,
                    return_type=string(tipos_primitivos, empty),
                    parameters=string(tipos_primitivos, register)
                    size=integer(para size > 0 é vetor/matriz, caso contrário é um variável unidmensional)
                )
            )
        '''
        self.symbol_map = dict()

        '''
            dict(
                name=string(nome do register),
                attribute_name=string(nome do atributo),
                attribute_type=string(tipo do atributo)
            )
        '''
        self.register_symbol_map = dict()

        '''
            Lista de erros semânticos
        '''
        self.error_list = []

    def get_error_list(self):
        return error_list
