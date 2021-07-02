# Bibliotecas necessárias:
- PyQT5: $ pip3 install pyqt5 && sudo apt-get install python3-pyqt5 && sudo apt-get install pyqt5-dev-tools
- Scipy: $ sudo pip3 install scipy
- Matplotlib: $ pip3 install matplotlib
- Numpy: $ sudo pip3 install numpy
- PySerial: $ pip3 install pyserial
- Extras: $ sudo apt-get install libatlas-base-dev

# Para gerar o gráfico de eficiência:
 - Executar o arquivo read_arduino.py enquanto envia os dados pelo Raspberry
 - Executar o arquivo efficiency.py para salvar a eficiência calculada para aquele gerador/modo
 - Repetir o processo para todos os geradores/modos
 - Executar o arquivo plot.py para gerar o gráfico