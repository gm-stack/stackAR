    #!/usr/bin/env python
import serial
import struct
import sys
import math

ser = serial.Serial("/dev/tty.usbserial-A8004wLd",115200)
ser.write("a")

def waitFor(ser,wantbyte):
    while True:
        byte = ord(ser.read(1))
        if (byte == wantbyte):
            return
        else:
            print "got %.2X" % byte

def hexdump(data):
    desc = "%i:" % len(data)
    for byte in data:
        desc += " " + ("%.2X" % ord(byte))
    print desc


while True:
    waitFor(ser,0xFF)
    data = ser.read(12)
    values = struct.unpack("<6h",data)
    waitFor(ser,0xFE)
    magX = values[0]
    magY = values[1]
    magZ = values[2]
    angle = math.atan2(magZ,magX) * (180/3.14159) + 90;
    if (angle < 0):
        angle = 360 + angle
    sys.stdout.write("\b"*36)
    sys.stdout.write("%4i %4i %4i  %4i %4i %4i  %4i" % (values[0], values[1], values[2], values[3], values[4], values[5],angle))
    sys.stdout.flush()
    
