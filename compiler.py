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
from analisador_semantico.tables import EntryIdentificadores

def write_file(file_name, list, message):
	with open(file_name, "w", encoding="utf-8") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"{item}\n")


def main():

	TEST_FILE = './analisador_semantico/test/test_function.txt' # Exemplo: ./test/function_sample.txt 

	tokens = lexical_analise(TEST_FILE)
	if tokens :
		validator = SemanticAnalyzer()
		parser = Parser(validator, tokens)
		parser.run()  

		tokens = [
			{"lexeme" : "integer", "category": "KEYWORD", "line": 1},
			{"lexeme" : "var", "category": "IDENTIFIER", "line": 1},
			{"lexeme" : "=", "category": "OPERATOR", "line": 1},
			{"lexeme" : "10", "category": "NUMBER", "line": 1},
			{"lexeme" : ";", "category": "NUMBER", "line": 1},
			]

		analizer = SemanticAnalyzer()
		entry = EntryIdentificadores(nome= "var", tipo= "integer", valor="10", tipoRetorno=None, parametros=None, tamanho=0, isConstant=False)
		analizer.pairs_table.tabela[0]["tabela"].append(entry)

		print("Entradas na tabela global")
		print(len(analizer.pairs_table.tabela[0]["tabela"]))

		print("-------------------------")

		print("teste não declarado: " + str(analizer.non_declared_object(0, [{"lexeme" : "var", "category": "IDENTIFIER", "line": 1}])))
		print("teste declaração repetida: " + str(analizer.repeated_statement(0, {"lexeme" : "var2", "category": "IDENTIFIER", "line": 1})))
		print("Lista de erros semanticos: ")
		print(analizer.get_error_list())


		if len(parser.get_error_list()) > 0: 
			print("Erros foram encontrados durante a análise sintática.")
		else:
			print("A análise sintática foi realizada com sucesso.")

		if len(validator.get_error_list()) > 0: 
			print("Erros foram encontrados durante a análise semântica.")
		else:
			print("A análise semântica foi realizada com sucesso.")			

		write_file("./analisador_sintatico/saida/parser_result.txt", parser.get_error_list(), "A análise sintática foi realizada com sucesso.")
		write_file("./analisador_semantico/saida/semantic_result.txt", validator.get_error_list(), "A análise semantica foi realizada com sucesso.")

	else:
		print("Erro durante a análise léxica.")
		#write_file("./analisador_sintatico/saida/parser_result.txt", None, "Erro durante a análise léxica.")
		
if __name__ == "__main__":
    main()


