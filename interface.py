import sys
import random
import unicodedata
import datetime
import os
import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

class Application(QWidget):
    def __init__(self, parent=None):
        super(Application,self).__init__()
        self.setWindowTitle("Interface de Comunicação")

        self.bits = 0
        self.Interface()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.formGroupBox1)
        self.setLayout(self.layout)

    def Interface(self):
        self.formGroupBox1 = QtWidgets.QGroupBox()

        #--------------layouts--------------------#
        layout = QtWidgets.QHBoxLayout()
        self.layout1 = QtWidgets.QFormLayout()
        self.layout2 = QtWidgets.QFormLayout()
        layout.addLayout(self.layout1)
        layout.addLayout(self.layout2)
        layout.addStretch()

        #----------------entrada------------------#
        self.entrada = QtWidgets.QLineEdit()

        self.layout1.addRow(QtWidgets.QLabel("Bits de entrada"), self.entrada)

        #------------enviar--------------#
        buttonEnviar = QtWidgets.QPushButton("Enviar")
        self.layout1.addRow(buttonEnviar)
        buttonEnviar.clicked.connect(self.send)

        #------------codificador--------------#
        buttonCodificador = QtWidgets.QPushButton("Codificador")
        self.layout2.addRow(buttonCodificador)
        buttonCodificador.clicked.connect(self.codificador)

        #------------decodificador------------#
        buttonDecodificador = QtWidgets.QPushButton("Decodificador")
        self.layout2.addRow(buttonDecodificador)
        buttonDecodificador.clicked.connect(self.decodificador)

        self.formGroupBox1.setLayout(layout)

    def save(self):
        retorno = 0 # retorna 0 se erro

        try:
            entry = str(self.entrada.text()) # pega string de entrada
            self.bits = retorno = [int(x) for x in entry] # converte str pra array de int
            print("Bits de entrada: ", self.bits)
        except ValueError: # entrada não numérica
            QtWidgets.QMessageBox.warning(self, 'Error', 'Entrada inválida ou digite novamente')
        
        self.entrada.clear() # limpa a entrada
        return retorno

    def send(self):
        if self.save(): # se entrada válida
            print("enviar")

    def plot(self, array, name, type):
        y = array # bits
        y.insert(0,0) # ajuste pro plot, insere um 0 na primeira posição do array

        x = [i for i in range(len(y))] # posicoes no tempo, a cada 1 seg, tamanho de acordo com a entrada y

        plt.step(x,y,'r',label=type)
        plt.title("${}$".format(name))
        plt.xlabel('$Tempo$')
        plt.ylabel('$Amplitude$')
        plt.grid(True, which='both')
        plt.legend(frameon=False)
        plt.xlim(0,len(x) - 1)
        plt.ylim(-1.5,1.5)
        plt.show()

    def codificador(self):
        print("Codificador")

        if self.save(): # se entrada válida
            self.plot(self.bits,"Codificador","Sinal de Entrada")

    def decodificador(self):
        print("Decodificador")

        if self.save(): # se entrada válida
            output = NRZBipolar(self.bits)
            self.plot(output,"Decodificador","NRZ Bipolar")

def NRZBipolar(input):
    output = []
    ant = -1

    for bit in input:
        if bit == 0:
            output.append(0)
        elif bit == 1:
            output.append(ant * (-1))
            ant *= (-1)

    return output

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Application()
    window.resize(600,400)

    window.show()

    sys.exit(app.exec_())