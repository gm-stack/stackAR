#!/usr/bin/env python
import serial
import struct
import sys
import math
import ConfigParser
import logging
import socket
import thread

config = ConfigParser.ConfigParser()
config.read("read_sensorboard.conf")

ser = serial.Serial(config.get('device','devnode'),config.getint('device','baudrate'))
ser.write("a")

verbose = (config.getint('app','verbose') == 1)
debug = (config.getint('app','debug') == 1)

def vprint(msg):
    if (verbose):
        print msg


def waitFor(ser,wantbyte):
    while True:
        byte = ord(ser.read(1))
        if (byte == wantbyte):
            return
        else:
            vprint("got %.2X" % byte)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((config.get('net','bind'), config.getint('net','port')))
serversocket.listen(50)

connections = []

def connthread(serversocket):
    global connections
    while 1:
        conn, addr = serversocket.accept()
        if (verbose):
            print "connection from %s" % addr[0]
        connections.append(conn)

thread.start_new_thread(connthread,(serversocket,))

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
    for conn in connections:
        try:
            conn.send("%i %i %i %i %i %i %i\n" % (values[0], values[1], values[2], values[3], values[4], values[5],angle))
        except:
            connections.remove(conn)
    if (debug):
        sys.stdout.write("\b"*36)
        sys.stdout.write("%4i %4i %4i  %4i %4i %4i  %4i" % (values[0], values[1], values[2], values[3], values[4], values[5],angle))
        sys.stdout.flush()
    
