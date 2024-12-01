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

		analizer = SemanticAnalyzer()
		analizer.registers_type_table["documento"] = {"nome":"string","idade":"integer"}
		entry1 = EntryIdentificadores(nome= "a", tipo= "float", valor="1,5", tipoRetorno=None, parametros=None, tamanho=0, isConstant=False)
		entry2 = EntryIdentificadores(nome= "b", tipo= "documento", valor=None, tipoRetorno=None, parametros=None, tamanho=0, isConstant=False)
		entry3 = EntryIdentificadores(nome= "b.nome", tipo= "string", valor="fulano", tipoRetorno=None, parametros=None, tamanho=0, isConstant=False)
		entry4 = EntryIdentificadores(nome= "b.idade", tipo= "integer", valor="10", tipoRetorno=None, parametros=None, tamanho=0, isConstant=False)
		entry5 = EntryIdentificadores(nome= "vetor", tipo= "integer", valor=None, tipoRetorno=None, parametros=None, tamanho=10, isConstant=False)
		analizer.pairs_table.tabela[0]["tabela"].append(entry1)
		analizer.pairs_table.tabela[0]["tabela"].append(entry2)
		analizer.pairs_table.tabela[0]["tabela"].append(entry3)
		analizer.pairs_table.tabela[0]["tabela"].append(entry4)
		analizer.pairs_table.tabela[0]["tabela"].append(entry5)

		print("Entradas na tabela global")
		print(len(analizer.pairs_table.tabela[0]["tabela"]))

		print("-------------------------")
		print("teste atribuição de tipo errado: " + str(analizer.wrong_type_assign(0, 
				variable= [{"lexeme" : "a", "category": "IDENTIFIER", "line": 1}], 
				value= [{"lexeme" : "1", "category": "NUMBER", "line": 1}, {"lexeme" : "+", "category": "OPERATOR", "line": 1}, {"lexeme" : "b", "category": "IDENTIFIER", "line": 1}, {"lexeme" : ".", "category": "OPERATOR", "line": 1}, {"lexeme" : "idade", "category": "IDENTIFIER", "line": 1}, {"lexeme" : "/", "category": "OPERATOR", "line": 1},  {"lexeme" : "1", "category": "NUMBER", "line": 1}],
				variable_type= {"lexeme" : "float", "category": "IDENTIFIER", "line": 1})	
			)
		)

		print("Lista de erros semanticos: ")
		print(analizer.get_error_list())


		if len(validator.get_error_list()) > 0: 
			print("Erros foram encontrados durante a análise semântica.")
		else:
			print("A análise semântica foi realizada com sucesso.")			

	else:
		print("Erro durante a análise léxica.")
		#write_file("./analisador_sintatico/saida/parser_result.txt", None, "Erro durante a análise léxica.")
		
if __name__ == "__main__":
    main()


