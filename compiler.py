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
from analisador_lexico.lexicalAnalyzer import lexical_analise
from analisador_sintatico.parser import Parser
from analisador_semantico.semantic_analyzer import SemanticAnalyzer

def write_file(file_name, list, message):
	with open(file_name, "w", encoding="utf-8") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"{item}\n")


def main():

	TEST_FILE = 'analisador_semantico\\test\\test_header_for.txt'#'./analisador_semantico/test/test_function.txt' # Exemplo: ./test/function_sample.txt 

	tokens = lexical_analise(TEST_FILE)
	if tokens :
		validator = SemanticAnalyzer()
		parser = Parser(validator, tokens)
		parser.run()  
		

		# for item in parser.validator.pairs_table.tabela[0]['tabela']:print(item.nome)

		print("\n--------------- tabela de registro ---------------")
		print(validator.registers_type_table)
		print("\n--------------- tabela global ---------------")
		print(validator.pairs_table)

		if parser.get_error_list(): 
			print("Erros foram encontrados durante a análise sintática.")
		else:
			print("A análise sintática foi realizada com sucesso.")

		if validator.get_error_list(): 
			print("Erros foram encontrados durante a análise semântica.")
		else:
			print("A análise semântica foi realizada com sucesso.")			

		write_file("./saidas/parser_result.txt", parser.get_error_list(), "A análise sintática foi realizada com sucesso.")
		write_file("./saidas/semantic_result.txt", validator.get_error_list(), "A análise semantica foi realizada com sucesso.")

	else:
		print("Erro durante a análise léxica.")
		#write_file("./analisador_sintatico/saida/parser_result.txt", None, "Erro durante a análise léxica.")
		
if __name__ == "__main__":
    main()
