from parser import Parser 

def analyser():
	lexicalTokenList = []  #IMPLEMENTAR PARA CHAMAR O LEXICO QUE RETORNARÁ APENAS 1 LISTA
	
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
