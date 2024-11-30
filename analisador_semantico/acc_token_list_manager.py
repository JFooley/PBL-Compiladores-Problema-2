acc_map = dict()

def create_acc():
	new_id = len(acc_map.keys())
	acc_map[new_id] = []
	return new_id

def delete_acc(acc_id):
	del acc_map[acc_id]

def accumulate(token): # Usar dentro do match
	for key in acc_map: acc_map[key].append(token)

def get_acc(acc_id):
	return acc_map[acc_id]

# -------------------

# Cria a sua lista de acumulação e começa a acumular os tokens
acc_id = create_acc() 

# Faz a validação aqui
acc_list = get_acc(acc_id)

# Deleta a sua lista de acumulação
delete_acc(acc_id)
