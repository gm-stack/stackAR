import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

pygame.font.init()

font = pygame.font.Font(None, 24)

textim = {}         # maps from string to Surface
texturemap = {}     # maps from surface to GL texture ID
imagesize = {}      # maps from GL texture ID to w/h

DEBUG = False

def renderText(text,cache=True):
    if (cache):
        if not text in textim:
            if DEBUG: print "adding %s to cache" % text
            textim[text] = font.render(text,1,(0,255,255))
        return textim[text]
    else:
        return font.render(text,1,(0,255,255))

def texture2gl(image,cache=True):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    fstring = pygame.image.tostring(image,"RGBA",0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    w = image.get_width()
    h = image.get_height()
    if (cache):
        imagesize[texture] = (w,h)
        if DEBUG: print "cached"
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,fstring);
    return texture;

def glTexture(image,cache=True):
    if (cache):
        if image in texturemap:
            return texturemap[image]
        else:
            texturemap[image] = texture2gl(image)
            return texturemap[image]
    else:
        return texture2gl(image,cache=False);

def glRect(x,y,w,h,align=0):
    glBegin(GL_QUADS)
    if (align == 0): #top left
        glTexCoord2f(0,0); glVertex2f(x,y)
        glTexCoord2f(0,1); glVertex2f(x,y+h)
        glTexCoord2f(1,1); glVertex2f(x+w,y+h)
        glTexCoord2f(1,0); glVertex2f(x+w,y)
        glEnd()
        return (x+w,y+h)
    elif (align == 1): #top right
        glTexCoord2f(0,0); glVertex2f(x-w,y)
        glTexCoord2f(0,1); glVertex2f(x-w,y+h)
        glTexCoord2f(1,1); glVertex2f(x,y+h)
        glTexCoord2f(1,0); glVertex2f(x,y)
        glEnd()
        return (x-w,y+h)
    elif (align == 2): #bottom right
        glTexCoord2f(0,0); glVertex2f(x-w,y-h)
        glTexCoord2f(0,1); glVertex2f(x-w,y)
        glTexCoord2f(1,1); glVertex2f(x,y)
        glTexCoord2f(1,0); glVertex2f(x,y-h)
        glEnd()
        return (x-w,y-h)
    elif (align == 3): #bottom left
        glTexCoord2f(0,0); glVertex2f(x,y-h)
        glTexCoord2f(0,1); glVertex2f(x,y)
        glTexCoord2f(1,1); glVertex2f(x+w,y)
        glTexCoord2f(1,0); glVertex2f(x+w,y-h)
        glEnd()
        return (x-w,y+h)
    elif (align == 4): #top middle
        leftw = int(w/2)
        rightw = w - leftw # integer division does not guarantee (w/2)*2 == w
        glTexCoord2f(0,0); glVertex2f(x-leftw,  y)
        glTexCoord2f(0,1); glVertex2f(x-leftw,  y+h)
        glTexCoord2f(1,1); glVertex2f(x+rightw, y+h)
        glTexCoord2f(1,0); glVertex2f(x+rightw, y)
        glEnd()
        return (x-w,y+h)

def drawText(text,x,y,cache=True,align=0):
    if (cache):
        image = renderText(text,cache=True)
        texture = glTexture(image,cache=True)
        glBindTexture(GL_TEXTURE_2D,texture)
        w,h = imagesize[texture]
        x2,y2 = glRect(x,y,w,h,align=align)
        return (x2,y2)
    else:
        image = renderText(text,cache=cache)
        texture = glTexture(image,cache=cache)
        x2,y2 = glRect(x,y,image.get_width(),image.get_height(),align=align)
        glDeleteTextures(texture)
        return (x2,y2)
        # delete surface
    