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
        return self.error_list
    
    # Validar parametro (luis)
    def func_parameter_validator(token_list):
        parameter_list = []
        for token in token_list:
            if token['category'] == 'IDENTIFIER':
                parameter_list.append(token)
        function_name = parameter_list.pop(0)
        function_name = function_name['lexeme']
    
        parameters_types = self.symbol_map['global'][function_name]['parameters']
    
        n = 0
        while n  < len(parameter_list):
            if parameter_list[0]['category'] == 'IDENTIFIER':
                parameter_type = self.symbol_map[self.scope][parameter['lexeme']]['type']
                if parameter_type != parameters_types[n]:
                    self.error_list.append("parametro invalido") #falta deixar bonitinho ainda
            # demais casos, numeros, strings...
    
            n += 1
