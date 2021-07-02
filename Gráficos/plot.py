"""
Plota o gráfico de eficiência de todos os modos/geradores
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

def read_efficiency(mode):
    file = open("Output/eficiencias_{}.txt".format(mode),"r")
    content = file.readlines()
    content = [line.strip("\n") for line in content if line != "\n"] # remove \n
    values = [float(x) for x in content] # convert to float array
    return values

def plot():
    values_crc = read_efficiency("CRC")
    values_crc8 = read_efficiency("CRC-8")
    values_crc10 = read_efficiency("CRC-10")
    values_checksum = read_efficiency("CHECKSUM")

    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    
    # set height of bar
    # [crc,crc8,crc10,checksum]
    generator = []
    for i in range(3): generator.append([values_crc[i],values_crc8[i],values_crc10[i],0])

    generator_checksum = [0,0,0,values_checksum[0]]
    
    # Set position of bar on X axis
    br1 = np.arange(len(generator[0]))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, generator[0], color ='tab:red', width = barWidth,
            edgecolor ='grey', label ='$Gerador$ $g(x)$ 1')
    plt.bar(br2, generator[1], color ='tab:green', width = barWidth,
            edgecolor ='grey', label ='$Gerador$ $g(x)$ 2')
    plt.bar(br3, generator[2], color ='tab:blue', width = barWidth,
            edgecolor ='grey', label ='$Gerador$ $g(x)$ 3')
    plt.bar(br4, generator_checksum, color ='tab:gray', width = barWidth,
            edgecolor ='grey', label ='$Checksum$')
    
    # Adding Xticks
    plt.xlabel('$Modo$', fontsize = 15)
    plt.ylabel('$Eficiência$ (%)', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(generator[0]))],
            ['$CRC$', '$CRC-8$', '$CRC-10$', '$Checksum$'])
    
    plt.legend()
    plt.savefig('Figuras/plot.png')
    plt.show()

if __name__ == "__main__":
    plot()