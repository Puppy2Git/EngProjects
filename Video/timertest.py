import time
class timer:
    def __init__(self,duration=0,start=False):
        self.start_time = time.time()
        self.active = start
        self.initduration = duration
        self.duration = self.initduration
    def pause_timer(self):
        self.duration = self.duration - (time.time() - self.start_time)
        self.active = False
    def start_timer(self):
        self.start_time = time.time()
        self.active = True
    def isDone(self):
        if (self.active == True):
            print (self.start_time + self.duration <= time.time())
            return (self.start_time + self.duration <= time.time())
        else:
            return False
    def reset_timer(self):
        self.duration = self.initduration
        self.active = False
    def hasStarted(self):
        return (self.duration == self.initduration & self.active == False)


lmao = timer(10,True)
lmao.isDone()
while (lmao.isDone() == False):
    x = 1
print("Done")