from .finiteAutomaton import LexicalFiniteAutomaton

def lexical_analise(file_name=None):
	if not file_name:
		file_name = input("Digite o nome do arquivo de leitura (ex: './input/teste.txt'): ")

	file = open_file(file_name)
 
	if (file):
		finiteAutomaton = LexicalFiniteAutomaton()
		finiteAutomaton.recognize_tokens(file)
		file.close()
		write_file("./saidas/lexical_result.txt", finiteAutomaton.show_error_list(), "Sucesso. Nenhum erro foi encontrado.")
		if finiteAutomaton.show_error_list():
			print("Erros foram encontrados durante a análise léxica")
		return finiteAutomaton.show_token_list()
	return None

def open_file(file_name):
	try:
		file = open(file_name, "r")
	except FileNotFoundError:
		print("O Arquivo não foi encontrado.")
	else:
		return file
	
def write_file(file_name, list, message):
	with open(file_name, "w") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"Lexeme: {item['lexeme']} | Category: {item['category']} | Line: {item['line']}\n")

if __name__ == "__main__":
    lexical_analise()