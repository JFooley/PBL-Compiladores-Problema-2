    # Caso: <primitive type> identifier ';' | identifier identifier ';' | <primitive type> identifier '=' <value> ';' | <primitive type> <vector position> ';'                                
    def expression_declaration(self):
        if self.lookahead()['category'] == 'IDENTIFIER':
            self.match_category("IDENTIFIER")
        else:
            #self.primitive_type()
            if self.lookahead()['category'] == 'IDENTIFIER':
                self.match_category("IDENTIFIER")
                if self.lookahead()['lexeme'] == '=':
                    #self.value()
                    pass
            else:
                #self.vector_position()
                pass
        self.match_lexeme([";"])
            
    # Caso: <expression declaration> <expression variables> | <expression declaration>
    def expression_variables(self):
        self.expression_declaration()
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()
       
    
    def variables(self):
        self.match_lexeme('variables')
        self.match_lexeme('{')
        if self.lookahead()['category'] == 'IDENTIFIER' or self.lookahead()['lexeme'] in ['integer', 'float', 'boolean', 'string']:
            self.expression_variables()
        self.match_lexeme(['}'])


 def arithmetic_expression(self):
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
    
    def arithmetic_operating(self):
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()

    def arithmetic_value(self):
        if self.lookahead()["category"] == "NUMBER":
            self.match_category("number")
        elif self.lookahead()["category"] == "IDENTIFIER":
            if self.lookahead(1)["category"] == "(":
                #self.function_call()
                pass
            else:
                #self.attribute()
                pass
        else:
            self.match_lexeme("(")
            self.arithmetic_expression()
            self.match_lexeme(")")

    def arithmetic_sum(self):
        self.match_lexeme(['+', '-'])
        self.arithmetic_operating()
        if self.lookahead()["lexeme"] in ['+', '-']:
            self.arithmetic_sum()
      
    def arithmetic_multiplication(self):
        self.match_lexeme(['*', '/'])
        self.arithmetic_value()
        if self.lookahead()["lexeme"] in ['*', '/']:
            self.arithmetic_multiplication()
