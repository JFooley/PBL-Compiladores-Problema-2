from tokenizer.lexicalAnalyzer import lexical_analise
from parser import Parser

def write_file(file_name, list, message):
	with open(file_name, "w") as file:
		if not list:
			file.write(message)
			return
		for item in list:
			file.write(f"{item}\n")


def main():
	'''
		Como testar o seu código e utilizar as produções já existentes nesse repositório:
		- Adicione o seu código para parser.py;
 		- Modifique TEST_FILE com o caminho do arquivo teste da produção que você está trabalhando no momento;
		- Use parser.nome_da_producao_que_estou_trabalhando() para testar o seu código;

	'''
	#TEST_FILE = './test/nome_do_arquivo_de_teste_que_estou_trabalhando.txt' # Exemplo: ./test/function_sample.txt (não esquecer de remover antes antes de enviar para o repositório)

	tokens = lexical_analise(TEST_FILE)
	if tokens :
		#print(tokens)
		parser = Parser(tokens)
		#parser.run()  
	
		#parser.nome_da_producao_que_estou_trabalhando() # Usar para testar o seu código (não esquecer de remover antes antes de enviar para o repositório)
		
		print("Número de erros encontrados: {num_errors}".format(num_errors=len(parser.get_error_list())))
		if parser.get_error_list(): print("Erros:", parser.get_error_list())

		#write_file("./saida/parser_result.txt", parser.get_error_list(), "A análise sintática foi realizada com sucesso.")
	else:
		print("Erro durante a análise léxica.")
		
if __name__ == "__main__":
    main()
