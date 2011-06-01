import subprocess, time
class ams:
    p = None
    def __init__(self, config):
        self.p = subprocess.Popen(["./AMSTracker -s -u 0.05"],stdout=subprocess.PIPE,shell=True)
        print self.p.stdout.readline()
    
    def read(self):
        data = self.p.stdout.readline()
        x = int(data[0:4])
        y = int(data[4:9])
        z = int(data[9:])
        values = [0,0,0,x,y,z,0]
        return values
