#!/usr/bin/env python
import serial
import struct
import sys

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
    sys.stdout.write("\b"*30)
    sys.stdout.write("%4i %4i %4i  %4i %4i %4i" % values)
    sys.stdout.flush()
    
