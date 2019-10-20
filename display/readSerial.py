import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

ser = serial.Serial('/dev/ttyUSB0', 9600)

def readSerial():
    line = ser.readline()
    if(line):
        print(line)

def endSerial():
    ser.close()