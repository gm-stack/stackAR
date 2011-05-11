import fontman
import thread
import socket
import gldrawing

degreespixel = 0
pixeldegree = 0

accel = [0,0,0]
mag = [0,0,0,0]
magaverage = []
average_len = 50

def accthread():
    print "start accthread"
    global accel
    global mag
    global magaverage
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",49154))
    fs = s.makefile()
    while True:
        line1 = fs.readline()[:-1].split(" ")
        mag1 = int(line1[6])
        magaverage.append(mag1)
        if len(magaverage) > average_len:
            magaverage.pop(0)
        total = 0
        for i in magaverage:
            total += i
        mag[3] = total / len(magaverage)
        #mag = [int(line[0]),int(line[1]),int(line[2]),int(line[6])]
        #accel = [int(line[3]),int(line[4]),int(line[5])]

def setup(config):    
    global degreespixel
    global pixeldegree
    thread.start_new_thread(accthread,())
    degreespixel = float(config.getint("camera","horfov")) / float(config.getint("StackAR","display_width"))
    pixeldegree = 1/degreespixel
    print "%f degrees/pixel, %f pixels/degree" % (degreespixel, pixeldegree)

def degwrap(deg):
    if (deg > 360):
        deg -= 360
    elif (deg < 0):
        deg += 360
    return deg

def draw():
    deg = mag[3]
    
    fontman.drawText("%i deg" % deg,320,30,align=4,cache=True)
    
    degoffset = deg % 10
    nearest = deg - degoffset
    pixoffset = degoffset * pixeldegree    
    #gldrawing.drawLine(320-pixoffset,20,320-pixoffset,30)
    tendeg = 10 * pixeldegree
    for i in range(-4,4):
        gldrawing.drawLine((320-pixoffset)+(i*tendeg),20,(320-pixoffset)+(i*tendeg),30)
    