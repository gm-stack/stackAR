import fontman
import thread
testmode = False
try:
    import gps
except:
    testmode = True
    print "no GPS found"

lat = 0
lon = 0
alt = 0
speed = 0
status = 0

session = None

def gpsthread():
    global session
    global lat
    global lon
    global alt
    global speed
    global status
    
    if not testmode:
        session = gps.gps(host="127.0.0.1",port=2947)
        session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
        for report in session:
            status = 0
            if ("lat" in report) and ("lon" in report):
                lat = report["lat"]
                lon = report["lon"]
                status = 1
            if "alt" in report:
                alt = report["alt"]
                status = 2
    else:
        lat = 34.929
        lon = 138.601
        alt = 100
        speed = 0
        status = 3

def setup(config):
    global testmode
    
    thread.start_new_thread(gpsthread,())

def draw():
    if (status == 0):
        fontman.drawText("No GPS fix",0,480,align=3,cache=True)
    elif (status == 1):
        fontman.drawText("2D %f %f" % (lat,lon),0,480,align=3,cache=True)
    elif (status == 2):
        fontman.drawText("3D %f %f %.1f" % (lat,lon,alt),0,480,align=3,cache=True)
    elif (status == 3):
        fontman.drawText("GPS Testmode: No GPS",0,480,align=3,cache=True)