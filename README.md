# I2C Protocol with Checksum and CRC
- Communication Systems course final project 2020.2
- Practical application of sending data with error detection methods (CRC and Checksum) between a Raspberry Pi 3 and an Arduino Uno, via I2C protocol
- Guilherme Araujo Machado do Nascimento (17105750) and Manoel Morais Lemos Neto (17204282)

## Libraries:
- PyQT5: $ pip3 install pyqt5 && sudo apt-get install python3-pyqt5 && sudo apt-get install pyqt5-dev-tools
- Scipy: $ sudo pip3 install scipy
- Matplotlib: $ pip3 install matplotlib
- Numpy: $ sudo pip3 install numpy
- PySerial: $ pip3 install pyserial
- Extras: $ sudo apt-get install libatlas-base-dev

## To generate the efficiency plot:
 - Run read_arduino.py file while sending data via Raspberry
 - Run efficiency.py file to save the calculated efficiency for that generator/mode
 - Repeat the process for all generators/modes
 - Run plot.py file to generate the efficiency plot
