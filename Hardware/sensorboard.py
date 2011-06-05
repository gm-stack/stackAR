import serial
import math
import struct

class sensorboard:
    ser = None
    def __init__(self, config):
        self.ser = serial.Serial(config.get('device','devnode'),config.getint('device','baudrate'))
        self.ser.write("a")
    
    def waitFor(self,seri,wantbyte):
        while True:
            byte = ord(self.ser.read(1))
            if (byte == wantbyte):
                return
            else:
                print("got %.2X" % byte)
    
    def read(self):
        self.waitFor(self.ser,0xFF)
        data = self.ser.read(18)
        values = struct.unpack("<9h",data)
        self.waitFor(self.ser,0xFE)
        magX = values[0]
        magY = values[1]
        magZ = values[2]
        angle = math.atan2(magZ,magX) * (180/3.14159) + 90;
        if (angle < 0):
            angle = 360 + angle
        values += (angle,)
        return values
