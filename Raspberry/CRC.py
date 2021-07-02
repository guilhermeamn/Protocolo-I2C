import random

def gera_certo(qtd = 6):
	dataword = ""
	for i in range(qtd):
		dataword += str(random.randint(0,1))
	print("Dataword gerada = ", dataword)
	return dataword

"""
50% das palavras geradas contem 2 erros injetados
"""
def simulation(value,g,mode):
	if mode == "CRC": qtd = 4
	elif mode == "CRC-8": qtd = 10
	elif mode == "CRC-10": qtd = 11
	
	dataword = gera_certo(qtd)
	codeword = ""
	
	if value % 2 != 0: codeword,_ = encoder(dataword,g,2)
	else: codeword,_ = encoder(dataword,g)
	
	return codeword
	
def XOR(a, b):
	if a == b: return '0'
	else: return '1'

def divisao(a,b,k,n):
	dividendo = ""
	divisor = ""
	quociente = ""
	resto = ""
	prox = ""
	i = 0

	for m in range(len(b)): dividendo += a[m]

	while i < n:
		if dividendo[0] == '1': divisor = b
		elif dividendo[0] == '0':
			divisor = ""
			for l in range(len(b)): divisor += '0'
		
		for j in range(1,len(b)): prox += XOR(dividendo[j],divisor[j])

		if i == 0: i += len(b)
		else: i += 1

		if i < n: prox += a[i]

		dividendo = prox
		prox = ""

	resto = dividendo
	return resto
	
"""
Insere qtd 1s em um binário 000000 e faz XOR com o codeword
@param: qtd -> quantidade de erros
		size -> tamanho da palavra
@return: codeword com erro nas posições geradas aleatórias
"""
def gera_erros(codeword,qtd,size):
	send = ""
	positions = random.sample(range(0,size),qtd)
	print("posicoes: ", positions)
	for i in range(size):
		if i in positions: send += '1'
		else: send += '0'
	
	codeword_erro = ""
	for i in range(size): codeword_erro += XOR(codeword[i],send[i])
	print("Codeword com erro gerado = ", codeword_erro)
	return codeword_erro

"""
@param: qtd_erro -> se != 0, envia codeword com qtd_erro erros
@return: codeword -> codeword gerada, com ou sem erro 
		 original -> codeword original, caso a opção com erro tenha sido selecionada (usado para o gráfico)
					 caso opção sem erro selecionada, original == codeword
"""
def encoder(dataword,g,qtd_erro = 0):
	print("----------Encoder--------------")
	k = len(dataword)
	r = len(g) - 1
	n = r + k # r = n - k
	bits_paridade = ""
	for i in range(r):
		bits_paridade += "0"
	print("Bits de paridade = ",bits_paridade)

	data_paridade = ""
	data_paridade += dataword + bits_paridade
	print("Dataword com bits de paridade = ",data_paridade)
	
	resto = divisao(data_paridade,g,k,n)

	codeword = dataword + resto
	print("Codeword = ", codeword)
	
	original = codeword
	if(qtd_erro): return gera_erros(codeword,qtd_erro,n), original
	else: return codeword, original

if __name__ == "__main__":
	g_x = "1011"

	bits = input('Digite a entrada de bits: ')
	encoder(bits,g_x)
