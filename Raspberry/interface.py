#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Raspberry Pi Master for Arduino Slave
# Connects to Arduino via I2C

import sys
import random
import unicodedata
import datetime
import os
import math
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
#from smbus import SMBus
import CRC
import Checksum
from time import sleep

#addr = 0x8 # bus address
#bus = SMBus(1) # indicates /dev/i2c-1

class Application(QWidget):
    def __init__(self, parent=None):
        super(Application,self).__init__()
        self.setWindowTitle("Interface de Comunicação")

        #------------atributos-----------#
        self.bits = 0
        self.active_erro = False
        self.active_erro_checksum = False
        self.qtd_erro = 0
        self.original_codeword = []
        self.codeword_plot = []
        self.crc_modes = ["CRC","CRC-8","CRC-10"]
        self.mode = "CRC"

        #------------------fonte-------------------#
        self.main_font = QtGui.QFont('Times',11, QtGui.QFont.Bold)
        self.secundary_font = QtGui.QFont('Times',12, QtGui.QFont.Bold)
        self.button_color = 'QPushButton {background-color: #365F73;}'

        self.Interface()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.formGroupBox1)
        self.setLayout(self.layout)

    def Interface(self):
        self.formGroupBox1 = QtWidgets.QGroupBox()

        #--------------layout--------------------#
        layout = QtWidgets.QHBoxLayout()

        #-------------------tabs--------------------#
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.CRCTabUI(), "CRC")
        self.tabs.addTab(self.ChecksumTabUI(), "Checksum")
        self.tabs.currentChanged.connect(self.tabsIndex)
        layout.addWidget(self.tabs)

        self.formGroupBox1.setLayout(layout)
        
    def CRCTabUI(self):
        crcTab = QtWidgets.QWidget()

        #--------------layouts--------------#
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(20,20,20,20)

        #--------------separator------------#
        separator = QtWidgets.QFrame()
        separator.setStyleSheet("background-color: #365F73")
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        separatorVertical = QtWidgets.QFrame()
        separatorVertical.setStyleSheet("background-color: #365F73")
        separatorVertical.setFrameShape(QtWidgets.QFrame.VLine)
        separatorVertical.setFrameShadow(QtWidgets.QFrame.Sunken)

        #----------------entrada------------------#
        self.entrada_crc = QtWidgets.QLineEdit()
        self.entrada_crc.setAlignment(QtCore.Qt.AlignLeft)
        self.entrada_crc.setStyleSheet('QLineEdit { background-color: gray; color: black}')
        label = QtWidgets.QLabel("Bits de entrada")
        label.setFont(self.main_font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.entrada_crc, 0, 1, 1, 2)
        
        #--------------gerador--------------#
        self.gerador = QtWidgets.QLineEdit()
        self.gerador.setStyleSheet('QLineEdit { background-color: gray; color: black}')
        self.gerador_label = QtWidgets.QLabel("Gerador g(x)")
        self.gerador_label.setFont(self.main_font)
        self.gerador_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.gerador_label, 1, 0)
        layout.addWidget(self.gerador, 1, 1, 1, 2)

        #------------enviar--------------#
        buttonEnviar = QtWidgets.QPushButton("Enviar")
        buttonEnviar.setStyleSheet(self.button_color)
        buttonEnviar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(buttonEnviar, 2, 1)
        buttonEnviar.clicked.connect(self.send)

        #------------combobox-------------#
        cb = QtWidgets.QComboBox()
        cb.addItems(["CRC","CRC-8","CRC-10"])
        cb.currentIndexChanged.connect(self.combo)
        layout.addWidget(cb, 0, 3)

        layout.addWidget(separator, 3, 0, 1, 5) # horizontal separator
        layout.addWidget(separatorVertical, 4, 1, 5, 1) # vertical separator

        #--------------análises-------------#
        analysis_title = QtWidgets.QLabel("ANÁLISE ESTATÍSTICA")
        analysis_title.setFont(self.secundary_font)
        analysis_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(analysis_title, 4, 0)

        #----------------simular------------------#
        buttonSimular = QtWidgets.QPushButton("Simular")
        buttonSimular.setStyleSheet(self.button_color)
        layout.addWidget(buttonSimular, 5, 0)
        buttonSimular.clicked.connect(self.automatizado)

        #---------simulação de análise de erros------------#
        buttonSimulacao = QtWidgets.QPushButton("Inserir ruído")
        buttonSimulacao.setStyleSheet(self.button_color)
        layout.addWidget(buttonSimulacao, 6, 0)
        buttonSimulacao.clicked.connect(self.simulacao)
        
        #------------opções de erro--------------#
        self.erro_crc = QtWidgets.QLineEdit()
        self.erro_crc.setPlaceholderText("Quantidade de erros")
        self.erro_crc.setStyleSheet('QLineEdit { background-color: gray; color: black}')
        layout.addWidget(self.erro_crc, 7, 0)
        self.erro_crc.setHidden(True)
        
        self.buttonSaveError_crc = QtWidgets.QPushButton("Salvar")
        self.buttonSaveError_crc.setStyleSheet(self.button_color)
        layout.addWidget(self.buttonSaveError_crc, 8, 0)
        self.buttonSaveError_crc.clicked.connect(self.saveError)
        self.buttonSaveError_crc.setHidden(True)
        
        #--------------gráficos-------------#
        plot_title = QtWidgets.QLabel("GRÁFICOS")
        plot_title.setFont(self.secundary_font)
        plot_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(plot_title, 4, 2)

        # codificador
        buttonCodificador = QtWidgets.QPushButton("Codificador")
        buttonCodificador.setStyleSheet(self.button_color)
        buttonCodificador.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(buttonCodificador, 5, 2, 2, 1)
        buttonCodificador.clicked.connect(self.codificador)
        
        # decodificador
        buttonDecodificador = QtWidgets.QPushButton("Decodificador")
        buttonDecodificador.setStyleSheet(self.button_color)
        buttonDecodificador.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        layout.addWidget(buttonDecodificador, 7, 2, 2, 1)
        buttonDecodificador.clicked.connect(self.decodificador)

        crcTab.setLayout(layout)
        return crcTab

    def ChecksumTabUI(self):
        checksumTab = QtWidgets.QWidget()

        #--------------layouts--------------#
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(20,20,20,20)

        #--------------separator------------#
        separator = QtWidgets.QFrame()
        separator.setStyleSheet("background-color: #365F73")
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        separatorVertical = QtWidgets.QFrame()
        separatorVertical.setStyleSheet("background-color: #365F73")
        separatorVertical.setFrameShape(QtWidgets.QFrame.VLine)
        separatorVertical.setFrameShadow(QtWidgets.QFrame.Sunken)

        #----------------entrada------------------#
        self.entrada_checksum = QtWidgets.QLineEdit()
        self.entrada_checksum.setAlignment(QtCore.Qt.AlignLeft)
        self.entrada_checksum.setStyleSheet('QLineEdit { background-color: gray; color: black}')
        label = QtWidgets.QLabel("Pacote de entrada")
        label.setFont(self.main_font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.entrada_checksum, 0, 1, 1, 2)

        #------------enviar--------------#
        buttonEnviar = QtWidgets.QPushButton("Enviar")
        buttonEnviar.setStyleSheet(self.button_color)
        buttonEnviar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(buttonEnviar, 2, 1)
        buttonEnviar.clicked.connect(self.send)

        layout.addWidget(separator, 3, 0, 1, 5) # horizontal separator

        #--------------análises-------------#
        analysis_title = QtWidgets.QLabel("ANÁLISE ESTATÍSTICA")
        analysis_title.setFont(self.secundary_font)
        #analysis_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(analysis_title, 4, 0)

        #----------------simular------------------#
        buttonSimular = QtWidgets.QPushButton("Simular")
        buttonSimular.setStyleSheet(self.button_color)
        layout.addWidget(buttonSimular, 5, 0)
        buttonSimular.clicked.connect(self.automatizado)

        #---------simulação de análise de erros------------#
        self.buttonSimulacaoChecksum = QtWidgets.QPushButton("Inserir ruído")
        self.buttonSimulacaoChecksum.setStyleSheet(self.button_color)
        self.buttonSimulacaoChecksum.setCheckable(True) # toggle button
        layout.addWidget(self.buttonSimulacaoChecksum, 6, 0)
        self.buttonSimulacaoChecksum.clicked.connect(self.simulacao)

        checksumTab.setLayout(layout)
        return checksumTab

    def tabsIndex(self):
        if self.tabs.currentIndex() == 0: self.mode = "CRC"
        elif self.tabs.currentIndex() == 1: self.mode = "Checksum"

    def automatizado(self):
        print("Simulação automática")
        if self.mode in self.crc_modes:
            message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,'Aviso','Esta simulação gera 100 datawords aleatórios. 50% deles utiliza 2 erros injetados. Os outros 50% sem erro.')
        elif self.mode == "Checksum":
            message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,'Aviso','Esta simulação gera 100 pacotes aleatórios. 50% deles utiliza erros injetados. Os outros 50% sem erro.')
        message.exec_()
        g_x = ""
        number_iterations = 100
        if self.mode in self.crc_modes:
            if(self.gerador.text() == ""): QtWidgets.QMessageBox.warning(self, 'Error', 'Entre com o gerador g(x)')
            else: g_x = str(self.gerador.text())
        for i in range(number_iterations):
            if self.mode in self.crc_modes and g_x != "":
                codeword = CRC.simulation(i,g_x,self.mode)
                codeword_array = [int(x) for x in codeword] # converte pra array de int
                codeword_with_g_x = [int(x) for x in g_x]
                codeword_with_g_x.insert(0,9) # pra indicar pro receptor que aqui começa o g(x)
                codeword_array += codeword_with_g_x
                #bus.write_i2c_block_data(addr,0,codeword_array) # envia pro arduino com offset 0
                sleep(1) # precisa dar sleep, se não a comunicação falha
                print("\n")
            elif self.mode == "Checksum":
                pack = Checksum.simulation(i)
                #bus.write_i2c_block_data(addr,1,pack) # envia pro arduino com offset 1
                sleep(1) # precisa dar sleep, se não a comunicação falha
                print("\n")
        self.gerador.clear()
        print("-----------------Simulação encerrada---------------------\n")
                
    def combo(self,i):
        self.mode = "CRC"
        if i == 0: self.gerador.setText("")
        elif i == 1: 
            self.gerador.setText("100000111")
            self.mode = "CRC-8"
        elif i == 2: 
            self.gerador.setText("1100011011")
            self.mode = "CRC-10"

    def save(self):
        retorno = 0 # retorna 0 se erro

        try:
            self.entry_crc = str(self.entrada_crc.text()) # pega string de entrada
            self.bits = retorno = [int(x) for x in self.entry_crc] # converte str pra array de int
            print("Bits de entrada: ", self.bits)
        except ValueError: # entrada não numérica ou vazia
            QtWidgets.QMessageBox.warning(self, 'Error', 'Entrada inválida! Digite novamente.')
        
        self.entrada_crc.clear() # limpa a entrada
        return retorno

    def save_checksum(self):
        retorno = 0 # retorna 0 se erro

        self.entry_checksum = str(self.entrada_checksum.text()) # pega string de entrada
        print("Pacote de entrada: ", self.entry_checksum)

        if len(self.entry_checksum) == 0: QtWidgets.QMessageBox.warning(self, 'Error', 'Entrada inválida! Digite novamente.')
        else: retorno = 1
        
        self.entrada_checksum.clear() # limpa a entrada
        return retorno

    def send(self):
        if self.mode in self.crc_modes and self.save(): # se entrada válida e CRC
            print("\n-----------------MODE = {}----------------".format(self.mode))
            g_x = str(self.gerador.text())
            codeword, original = CRC.encoder(self.entry_crc,g_x,self.qtd_erro)
            codeword_array = [int(x) for x in codeword] # converte pra array de int
            self.original_codeword = [int(x) for x in original] # pra plotar o codeword original
            self.codeword_plot = [int(x) for x in codeword] # pra plotar o codeword
            codeword_with_g_x = [int(x) for x in g_x]
            codeword_with_g_x.insert(0,9) # pra indicar pro receptor que aqui começa o g(x)
            codeword_array += codeword_with_g_x
            #bus.write_i2c_block_data(addr,0,codeword_array) # envia pro arduino com offset 0
            self.gerador.clear()
            print("------------------------------------------------\n")
        elif self.mode == "Checksum" and self.save_checksum(): # se entrada válida e Checksum
            print("\n-----------------MODE = {}----------------".format(self.mode))
            in_list = self.entry_checksum.split()
            if len(in_list) < 5: QtWidgets.QMessageBox.warning(self, 'Error', 'Entrada inválida! Pacote menor que 5.')
            else:
                somatorio = Checksum.calculate_sum(in_list)
                checksum = Checksum.emissor(somatorio,4,self.active_erro_checksum)
                in_list.append(checksum) # adiciona o checksum no array pra enviar
                #bus.write_i2c_block_data(addr,1,in_list) # envia pro arduino com offset 1
            print("------------------------------------------------\n")

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

        if len(self.original_codeword) != 0: self.plot(self.original_codeword,"Codificador","Codeword gerada")
        else: QtWidgets.QMessageBox.warning(self, 'Error', 'Primeiro digite a entrada e pressione Enviar.')
            
    def decodificador(self):
        print("Decodificador")
        
        if len(self.codeword_plot) != 0: self.plot(self.codeword_plot,"Decodificador","Codeword recebida")
        else: QtWidgets.QMessageBox.warning(self, 'Error', 'Primeiro digite a entrada e pressione Enviar.')

    def simulacao(self):
        print("Inserir ruído")
        if self.mode in self.crc_modes:
            if self.active_erro: 
                self.erro_crc.setHidden(True)
                self.buttonSaveError_crc.setHidden(True)
                self.active_erro = False
                self.qtd_erro = 0
            else: 
                self.erro_crc.setHidden(False)
                self.buttonSaveError_crc.setHidden(False)
                self.active_erro = True
        elif self.mode == "Checksum":
            if self.buttonSimulacaoChecksum.isChecked():
                self.buttonSimulacaoChecksum.setStyleSheet("background-color : lightblue")
                self.active_erro_checksum = True
            else:
                self.buttonSimulacaoChecksum.setStyleSheet(self.button_color)
                self.active_erro_checksum = False
            
    def saveError(self):
        if self.erro_crc.text() != "": self.qtd_erro = int(self.erro_crc.text())
        print("Quantidade de erros escolhida: ", self.qtd_erro)
        
def dark_theme(app):
    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dark_theme(app)

    window = Application()
    window.resize(600,400)

    window.show()

    sys.exit(app.exec_())
