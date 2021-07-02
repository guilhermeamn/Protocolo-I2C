##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
"""
Grava a saída do Arduíno em um arquivo txt
"""
import serial
import sys

serial_port = '/dev/ttyACM0'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)
modes = ["CRC","CRC-8","CRC-10","CHECKSUM"]
name = ""

if len(sys.argv) < 2:
    print("Usage: python3 read_arduino.py [mode]")
    print("[CRC,CRC-8,CRC-10,CHECKSUM]")

else:
    if sys.argv[1] not in modes:
        print("Modo digitado não existe. Digite novamente.")
        print("Usage: python3 read_arduino.py [mode]")
        print("[CRC,CRC-8,CRC-10,CHECKSUM]")
    else:
        mode = sys.argv[1]
        write_to_file_path = "Output/output_{}.txt".format(mode)

        print("MODE = " + mode)

        output_file = open(write_to_file_path, "w")
        ser = serial.Serial(serial_port, baud_rate)
        while True:
            line = ser.readline()
            line = line.decode("utf-8") #ser.readline returns a binary, convert to string
            print(line)
            output_file.write(line)