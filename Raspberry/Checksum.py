import random

def gera_certo(qtd = 5):
	pack = []
	for i in range(qtd):
		pack.append(str(random.randint(0,10)))
	print("Pacote gerado = ", pack)
	return pack

"""
50% das palavras geradas contem erros injetados
"""
def simulation(value):
	pack = gera_certo()
	somatorio = calculate_sum(pack)
	if value % 2 != 0: checksum = emissor(somatorio,4,True)
	else: checksum = emissor(somatorio,4)
	pack.append(checksum)
	return pack
	
def complemento(s):
	ret = ""
	t = len(s)
	for i in range(t):
		if s[i] == '0': ret += '1'
		elif s[i] == '1': ret += '0'
	return ret
	
"""
Convert int to binary (4 bits)
"""
def toBinary(n):
	return "{0:04b}".format(n)
	
def toDecimal(n):
	decimalNumber = 0
	i = 0
	remainder = 0
	while n != 0:
		remainder = n % 10
		n /= 10
		decimalNumber += remainder*pow(2,i)
		i += 1
	return decimalNumber

def binaryStringToint(s):
    return int(s,2)

def soma(a,b):
    return toBinary(a + b)    

def calculate_sum(g):
    for i in range(len(g)):	g[i] = int(g[i])
    return sum(g)
    
"""
Gera um número aleatório pra somar com o pacote enviado
"""
def gera_erro(checksum):
	erro = random.randint(1,10)
	print("Erro gerado = ", erro)
	return checksum + erro
	
"""
Faz o cálculo da soma no checksum
Ex.: 11011 -> 1011
			+	 1
"""
def checksum_sum(word,size):
	word_length = len(word)
	n = word_length - size # números da frente que tem que retirar
	sup = ""
	inf = ""
	for i in range(n,word_length): sup += word[i] # números que vão somar com os retirados
	for i in range(n): inf += word[i] # retirados
	s = soma(binaryStringToint(sup),binaryStringToint(inf))
	return s

def emissor(somatorio,size,error = False):
	print("\n----------Emissor-----------")
	word = ""
	word += toBinary(somatorio) # soma convertida em binário
	word_length = len(word)
	# soma em binário <= tamanho da palavra
	if word_length <= size: checksum = binaryStringToint(complemento(word)) # soma vai ser o próprio word
	else: # soma em binário > tamanho da palavra
		s = checksum_sum(word,size)
		while len(s) > size: # enquanto a soma der maior que size bits (palavras de size bits)
			s = checksum_sum(s,size)
		checksum = binaryStringToint(complemento(s))
	print("Checksum = ", checksum)
	if error: return gera_erro(checksum)
	else: return checksum
	
if __name__ == "__main__":
	package = input("Digite o pacote de entrada: ")
	in_list = package.split()
	somatorio = calculate_sum(in_list)
	checksum = emissor(somatorio,4)
