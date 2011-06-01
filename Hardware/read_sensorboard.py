#!/usr/bin/env python
import sys
import ConfigParser
import socket
import thread

config = ConfigParser.ConfigParser()
config.read("read_sensorboard.conf")

devtype = config.get('device','devtype')
device = None

if (devtype == "sensorboard"):
    import sensorboard
    device = sensorboard.sensorboard(config)
elif (devtype == "ams"):
    import ams
    device = ams.ams(config)


verbose = (config.getint('app','verbose') == 1)
debug = (config.getint('app','debug') == 1)

def vprint(msg):
    if (verbose):
        print msg

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
    values = device.read()
    for conn in connections:
        try:
            conn.send("%i %i %i %i %i %i %i\n" % (values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
        except:
            connections.remove(conn)
    if (debug):
        sys.stdout.write("\b"*36)
        sys.stdout.write("%4i %4i %4i  %4i %4i %4i  %4i" % (values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
        sys.stdout.flush()
    
