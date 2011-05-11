#!/usr/bin/python

import sys
import cv
import pygame
import time
import thread
import fontman
import datetime
import time

from OpenGL.GL import *
from OpenGL.GLU import *

import ConfigParser

config = ConfigParser.ConfigParser()
config.read("StackAR.conf")

screen_width = config.getint("StackAR","display_width")
screen_height = config.getint("StackAR","display_height")

cameranum = config.getint("camera","cameraNum")

pygame.init()
pygame.display.init()
pygame.display.set_mode((screen_width, screen_height),pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0,screen_width,screen_height,0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

capture = cv.CaptureFromCAM(cameranum)

cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH, screen_width)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,screen_height)

def glRect(x,y,w,h):
    glBegin(GL_QUADS)
    glTexCoord2f(0,0); glVertex2f(x,y)
    glTexCoord2f(0,1); glVertex2f(x,y+h)
    glTexCoord2f(1,1); glVertex2f(x+w,y+h)
    glTexCoord2f(1,0); glVertex2f(x+w,y)
    glEnd()

def createTextureFromCam(texture):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    fstring = frame.tostring()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,screen_width,screen_height,0,GL_BGR,GL_UNSIGNED_BYTE,fstring);
    return texture;

def evLoop():
    while 1:
        event = pygame.event.wait()

thread.start_new_thread(evLoop,())

#modules = {}
#for module in config.get("modules","load").split(","):
#modules[module] = __import__(module,fromlist=["modules"])
#print modules

import modules.clock
import modules.gpsloc
import modules.sensors

modules = {"clock": modules.clock, "gpsloc": modules.gpsloc, "sensors": modules.sensors}

for mod in modules:
    print mod
    modules[mod].setup(config)

sttime = time.time()

while 1:
    frame = cv.QueryFrame(capture)
    texture = createTextureFromCam(frame)
    glBindTexture(GL_TEXTURE_2D,texture)
    glRect(0,0,screen_width,screen_height)
    glDeleteTextures(texture)
    
    fontman.drawText("StackAR 0.01 pre-alpha rc 0",0,0)
    
    for mod in modules:
        modules[mod].draw()
    
    currtime = time.time()
    timediff = currtime - sttime
    sttime = currtime
    fps = 1/timediff
    fontman.drawText("%.1f fps" % fps,screen_width,screen_height,align=2)
    
    pygame.display.flip()