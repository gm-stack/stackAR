import serial
import math
import struct

class sensorboard:
    ser = None
    def __init__(self, config):
        ser = serial.Serial(config.get('device','devnode'),config.getint('device','baudrate'))
        ser.write("a")
    
    def waitFor(ser,wantbyte):
        while True:
            byte = ord(ser.read(1))
            if (byte == wantbyte):
                return
            else:
                vprint("got %.2X" % byte)
    
    def read(self):
        waitFor(ser,0xFF)
        data = self.ser.read(12)
        values = struct.unpack("<6h",data)
        waitFor(ser,0xFE)
        magX = values[0]
        magY = values[1]
        magZ = values[2]
        angle = math.atan2(magZ,magX) * (180/3.14159) + 90;
        if (angle < 0):
            angle = 360 + angle
        values += [angle]
        return values
