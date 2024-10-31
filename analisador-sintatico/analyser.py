'''
Problema 3 - Análise Sintática

EXA869 – MI Processadores de Linguagens de Programação

Equipe:
Luis Fernando do Rosario Cintra
Lucas Gabriel da Silva Lima Reis
Lucas Carneiro de Araújo Lima
Igor Figueredo Soares
João Gabriel Lima Almeida
Estéfane Carmo de Souza
Rogério dos Santos Cerqueira
Felipe Silva Queiroz
Francisco Ferreira
Georgenes Caleo Silva Pinheiro
'''
from tokenizer.lexicalAnalyzer import lexical_analise
from parser import Parser

def write_file(file_name, list, message):
	with open(file_name, "w", encoding="utf-8") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"{item}\n")


def main():

	TEST_FILE = './test/main.txt' # Exemplo: ./test/function_sample.txt 

	tokens = lexical_analise(TEST_FILE)
	if tokens :
		parser = Parser(tokens)
		parser.run()  

		if parser.get_error_list(): 
			print("Erros encontrados durante a análise sintática.")
		else:
			print("A análise sintática foi realizada com sucesso.")

		write_file("./saida/parser_result.txt", parser.get_error_list(), "A análise sintática foi realizada com sucesso.")
	else:
		print("Erro durante a análise léxica.")
		write_file("./saida/parser_result.txt", None, "Erro durante a análise léxica.")
		
if __name__ == "__main__":
    main()
