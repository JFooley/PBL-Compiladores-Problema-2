class PushdownAutomanton:

    def __init__(self):
        self.token_list = []
        self.i = 0
        self.error_list = []

#def next_index(self):
#  if(self.token_list[self.i + 1] != None):
#     self.i += 1
#  else:
#     self.error_list.append("erro sla")
  
def logic_expression(self):
  return

def body(self):
    return

#def condicional(self):
#  next_index(self)
#  if(token_list[i]['lexeme'] == '('):
#    logic_expression(self)
#    next_index(self)
#    if(token_list[i]['lexeme'] == ')'):
#        next_index(self)
#        if(token_list[i]['lexeme'] == 'then'):
#           next_index(self)


def condicional(self):
    self.index += 1
    
    if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == '('):
        return "Error: unexpected Lexemme"
    
    logic_expression(self)
    self.index += 1
    
    if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == ')'):
        return "Error: unexpected Lexemme" 
    
    self.index += 1
    
    if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == 'then'):
        return "Error: unexpected Lexemme"

    self.index += 1

    if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == '{'):
        return "Error: unexpected Lexemme"
    
    body(self) 
    self.index += 1

    if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == '}'):
        return "Error: unexpected Lexemme"
    
    self.index += 1
    
    if (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == 'else'):

        self.index += 1

        if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == '{'):
            return "Error: unexpected Lexemme"
    
        body(self) 
        self.index += 1

        if not (self.index < len(self.token_list) and self.token_list[self.index]['lexeme'] == '}'):
            return "Error: unexpected Lexemme"
    else:
        return "success" #Aq acaba

    

        

