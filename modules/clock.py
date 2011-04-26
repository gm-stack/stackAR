import fontman
import datetime

def setup():
    pass

def draw():
    (x2,y2) = fontman.drawText(datetime.datetime.now().strftime("%S"),640,0,align=1,cache=True)
    (x2,y2) = fontman.drawText(datetime.datetime.now().strftime("%M"),x2,0,align=1,cache=True)
    (x2,y2) = fontman.drawText(datetime.datetime.now().strftime("%k"),x2,0,align=1,cache=True)