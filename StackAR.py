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

pygame.init()
pygame.display.init()
pygame.display.set_mode((640, 480),pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0,640,480,0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

capture = cv.CaptureFromCAM(-1)

cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,480)

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
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,640,480,0,GL_BGR,GL_UNSIGNED_BYTE,fstring);
    return texture;

def evLoop():
    while 1:
        event = pygame.event.wait()

thread.start_new_thread(evLoop,())

import modules.clock
import modules.gpsloc

mods = [modules.clock,modules.gpsloc]
for mod in mods:
    mod.setup()

sttime = time.time()

while 1:
    frame = cv.QueryFrame(capture)
    texture = createTextureFromCam(frame)
    glBindTexture(GL_TEXTURE_2D,texture)
    glRect(0,0,640,480)
    glDeleteTextures(texture)
    
    fontman.drawText("StackAR 0.01 pre-alpha rc 0",0,0)
    
    for mod in mods:
        mod.draw()
    
    currtime = time.time()
    timediff = currtime - sttime
    sttime = currtime
    fps = 1/timediff
    fontman.drawText("%.1f fps" % fps,640,480,align=2)
    
    pygame.display.flip()