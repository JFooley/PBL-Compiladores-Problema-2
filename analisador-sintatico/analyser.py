from parser import Parser 

def analyser():
	lexicalTokenList = []  #IMPLEMENTAR PARA CHAMAR O LEXICO QUE RETORNARÁ APENAS 1 LISTA
	
	lexicalTokenList.append({"lexeme": "\"string\"" , "category": "STRING", "line": 1})
	lexicalTokenList.append({"lexeme": "'c'", "category": "CHARACTER", "line": 1})
	lexicalTokenList.append({"lexeme":"integer", "category":"KEYWORD", "line":1})
	lexicalTokenList.append({"lexeme":"boolean", "category":"KEYWORD", "line":1})
	lexicalTokenList.append({"lexeme":"string", "category":"KEYWORD", "line":1})
	lexicalTokenList.append({"lexeme":"float", "category":"KEYWORD", "line":1})
	lexicalTokenList.append({"lexeme":"abcde", "category":"IDENTIFIER", "line":1})
	lexicalTokenList.append({"lexeme":"id", "category":"IDENTIFIER", "line":1})
	lexicalTokenList.append({"lexeme":"=", "category":"DELIMITED", "line":1})
	lexicalTokenList.append({"lexeme":"'C'", "category":"CHARACTER", "line":1})
	lexicalTokenList.append({"lexeme":";", "category":"DELIMITED", "line":1})

	lexicalTokenList.append({"lexeme":"increment_terminal", "category":"DELIMITED", "line":1})
	lexicalTokenList.append({"lexeme":";", "category":"DELIMITED", "line":1})

	lexicalTokenList.append({"lexeme":".", "category":"DELIMITED", "line":1})
	lexicalTokenList.append({"lexeme":"register_position", "category":"DELIMITED", "line":1})

	lexicalTokenList.append({"lexeme":"[", "category":"DELIMITED", "line":1})
	lexicalTokenList.append({"lexeme":"vector_position", "category":"DELIMITED", "line":1})


	if lexicalTokenList:
		parser = Parser(lexicalTokenList)
		parser.run()  
		write_file("./saida/parser_result.txt", parser.show_error_list(), "A análise sintática foi realizada com sucesso.")
		return parser
	return None

	
def write_file(file_name, list, message):
	print(len(list))
	with open(file_name, "w") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"{item}\n")

if __name__ == "__main__":
    analyser()
