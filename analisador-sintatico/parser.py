class Parser():
    def __init__(self, token_list):
        self.token_list = token_list
        self.error_list = []
        self.index = 0
    
    # Função match para verificar categoria
    def match_category(self, expected_token_category):
        current_token = self.lookahead()
        if current_token['category'] != None and current_token['category'] in expected_token_category:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_category, "received":current_token["category"]})
            
    # Função match para verificar o lexema
    def match_lexeme(self, expected_token_lexeme):
        current_token = self.lookahead()
        if current_token['lexeme'] != None and current_token['lexeme'] in expected_token_lexeme:
            self.index += 1 # Move to the next token
            return current_token
        else:
            self.error_list.append({"position":current_token["line"], "expected":expected_token_lexeme, "received":current_token["lexeme"]})
    
    # Acessa o token atual ou examina os proximos
    def lookahead(self, K = 0):
        if self.index + K < len(self.token_list):
            return self.token_list[self.index + K]
        return {"lexeme": None,"category": None,"line": None}
    
    # Executa o algorítimo
    def run(self):
        self.start()
        if len(self.error_list) < 0:
            print("sucesso")
        else:
            for item in token_list:
                print(item)

    
    ### Produções ###
    def start(self):
        # <start>::= <registers> <constants> <variables> <functions> <main> 
        #           | <registers> <constants> <variables> <main> 
        #           | <constants> <variables> <functions> <main>
        #           | <constants> <variables> <main>
        self.value()
        '''    
        if self.lookahead()["lexeme"] == "register":
            self.registers()

        self.constants()
        self.variables()
        
        if self.lookahead()["lexeme"] == "function":
            self.functions()

        self.main()
        '''
    
    def registers(self):
        self.match_lexeme("register")
    
    # Fazer o resto, de constants, variables, functions

#<if>::= <fixed if>  | <fixed if> 'else' '{' <body> '}'
#<fixed if>::= 'if' '(' <logic expression> ')' 'then' '{' <body> '}' 
#--------------------- Condicionais ---------------------
    def condicional(self):
        self.match_lexeme(["if"])
        self.match_lexeme(["("])
        #self.logic_expression()
        self.match_lexeme("expressao") #Remover quando tiver o logic_expression()
        self.match_lexeme([")"])
        self.match_lexeme(["then"])
        self.match_lexeme(["{"])
        #self.body()
        self.match_lexeme("body") #Remover quando tiver o body()
        self.match_lexeme(["}"])

        if (self.lookahead()["lexeme"] == "else"):
            self.match_lexeme(["else"])
            self.match_lexeme(["{"])
            #self.body()
            self.match_lexeme("body") #Remover quando tiver o body()
            self.match_lexeme(["}"])


#<write>::= 'write' '(' <write list> ')' ';'
#<write list> ::= <value> ',' <write list> | <value>
#--------------------- Write ---------------------
    def write(self):
        self.match_lexeme(["write"])
        self.match_lexeme(["("])
        
        self.value()  
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme([","])  
            self.value() 

        self.match_lexeme([")"])
        self.match_lexeme([";"])

#<read>::= 'read' '(' <read list> ')' ';'
#<read list>::= <attribute>  ',' <read list> | <attribute>
#--------------------- Read ---------------------
    def read(self):
        self.match_lexeme(["read"])
        self.match_lexeme(["("])
        
        self.attribute()  
        while self.lookahead()["lexeme"] == ",":  
            self.match_lexeme([","])  
            self.attribute() 

        self.match_lexeme([")"])
        self.match_lexeme([";"])

#<value>::= stringDeclarate | character | <logic expression>
    def value(self):
        if self.lookahead()["category"] == "STRING":
            self.match_category(["STRING"])
        elif self.lookahead()["category"] == "CHARACTER":
            self.match_category(["CHARACTER"])
        else:
            #self.logic_expression()
            self.match_lexeme(["expressao"]) #Remover quando tiver o logic_expression()

# <type>::= <primitive type> | identifier
    def type(self):
        if self.lookahead()["category"] == "IDENTIFIER":
             self.match_category(["IDENTIFIER"])
        else:
            self.primitive_type()
    
#<primitive type>::= 'integer' | 'float' | 'boolean' | 'string'
    def primitive_type(self):
        if self.lookahead()["lexeme"] == "integer":
            self.match_lexeme(["integer"])
        elif self.lookahead()["lexeme"] == "float":
            self.match_lexeme(["float"])
        elif self.lookahead()["lexeme"] == "boolean":
            self.match_lexeme(["boolean"])
        else:
            self.match_lexeme(["string"])


#<assignment>::= <attribute> '=' <value> ';'| <attribute> <increment terminal> ';'
    def assignment(self):
        self.attribute()
        if self.lookahead()["lexeme"] == "=":
            self.value()
            self.match_lexeme([";"])
        else:
            #self.increment_terminal()
            self.match_lexeme(["increment_terminal"]) #REMOVER
            self.match_lexeme([";"])

#<attribute>::= identifier | <register position> | <vector position>
    def attribute(self):
        if self.lookahead()["category"] == "IDENTIFIER":
            self.match_category(["IDENTIFIER"])
            if self.lookahead()["lexeme"] == ".":
                #self.register_position()
                self.match_lexeme(["register_position"]) #REMOVER
            elif self.lookahead()["lexeme"] == "[":
                #self.vector_position()
                self.match_lexeme(["vector_position"]) #REMOVER
        else: 
            self.match_category(["IDENTIFIER"])

#<commands>::= <for> | <while> | <if> | <write> | <read> | <return> | <function call> ';'
def commands(self):
    if self.lookahead()["lexeme"] == "for":
        #self.for()
        self.match_lemexe(["for"]) #REMOVER
    elif self.lookahead()["lexeme"] == "while":
        #self.while()
        self.match_lemexe(["while"]) #REMOVER
    elif self.lookahead()["lexeme"] == "if":
        self.condicional()
    elif self.lookahead()["lexeme"] == "write":
        self.write()
    elif self.lookahead()["lexeme"] == "read":
        self.read()
    elif self.lookahead()["lexeme"] == "return":
        #self.return()
        self.match_lexeme(["return"])
    else:
        self.function_call()
        self.match_lexeme([";"])
    

'''
token_list = []
token_list.append({"lexeme": "\"string\"" , "category": "STRING", "line": 1})
token_list.append({"lexeme": "'c'", "category": "CHARACTER", "line": 1})
token_list.append({"lexeme":"integer", "category":"KEYWORD", "line":1})
token_list.append({"lexeme":"boolean", "category":"KEYWORD", "line":1})
token_list.append({"lexeme":"string", "category":"KEYWORD", "line":1})
token_list.append({"lexeme":"float", "category":"KEYWORD", "line":1})
token_list.append({"lexeme":"abcde", "category":"IDENTIFIER", "line":1})
token_list.append({"lexeme":"id", "category":"IDENTIFIER", "line":1})
token_list.append({"lexeme":"=", "category":"DELIMITED", "line":1})
token_list.append({"lexeme":"'C'", "category":"CHARACTER", "line":1})
token_list.append({"lexeme":";", "category":"DELIMITED", "line":1})

token_list.append({"lexeme":"increment_terminal", "category":"DELIMITED", "line":1})
token_list.append({"lexeme":";", "category":"DELIMITED", "line":1})

token_list.append({"lexeme":".", "category":"DELIMITED", "line":1})
token_list.append({"lexeme":"register_position", "category":"DELIMITED", "line":1})

token_list.append({"lexeme":"[", "category":"DELIMITED", "line":1})
token_list.append({"lexeme":"vector_position", "category":"DELIMITED", "line":1})


p = Parser(token_list)

p.run()
'''