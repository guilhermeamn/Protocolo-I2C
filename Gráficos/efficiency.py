"""
Lê o arquivo de saída do Arduíno, extrai o número de erros detectados e calcula a eficiência
"""

import sys

"""
Search for the given string in file and return lines containing that string, along with line numbers
(https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/)
"""
def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

"""
Escreve as eficiências em um arquivo
"""
def write_file(efficiency,mode):
    file = open("Output/eficiencias_{}.txt".format(mode),"a")
    file.write(str(efficiency) + '\n')
    file.close()

"""
Conta quantas linhas tem no arquivo
"""
def count_lines(file):
    nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
    line_count = len(nonempty_lines)
    file.close()
    print(line_count)
    return line_count
    
"""
Abre o arquivo de saída do Arduíno e calcula a eficiência do gerador/modo
@param: mode -> CRC, CRC-8, CRC-10 ou CHECKSUM
"""
def read_file(mode):
    crc_modes = ["CRC","CRC-8","CRC-10"]

    # acha as linhas onde tem resultado d(x)
    if mode in crc_modes: search = "d(x)"
    elif mode == "CHECKSUM": search = "Checksum"
    matched_lines = search_string_in_file("Output/output_{}.txt".format(mode),search)
    total = len(matched_lines) # número total de pacotes enviados

    num_rejeitou = 0
    if mode in crc_modes:
        # verifica quantas d(x) foram descartadas
        for elem in matched_lines:
            if elem[1] == "d(x) descartada": num_rejeitou += 1
    
    elif mode == "CHECKSUM":
        # pegando só o valor do checksum na linha encontrada
        checksums = []
        for elem in matched_lines:
            checksums.append([int(x) for x in elem[1].split() if x.isdigit()][0])
        
        # quantos pacotes tiveram erro detectado
        for checksum in checksums:
            if checksum != 0: num_rejeitou += 1

    efficiency = (num_rejeitou / 50) * 100
    print("Descartadas: ", num_rejeitou, "de 50")
    print("Eficiência = ", efficiency, "%")

    write_file(efficiency,mode)

if __name__ == "__main__":
    modes = ["CRC","CRC-8","CRC-10","CHECKSUM"]

    if len(sys.argv) < 2:
        print("Usage: python3 efficiency.py [mode]")
        print("[CRC,CRC-8,CRC-10,CHECKSUM]")
    else:
        mode = sys.argv[1]
        if mode not in modes:
            print("Modo digitado não existe. Digite novamente.")
            print("Usage: python3 efficiency.py [mode]")
            print("[CRC,CRC-8,CRC-10,CHECKSUM]")
        else: read_file(mode)