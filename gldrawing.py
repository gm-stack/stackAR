from OpenGL.GL import *
from OpenGL.GLU import *

def drawLine(x1,y1,x2,y2):
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_LINES)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()
    glEnable(GL_TEXTURE_2D)