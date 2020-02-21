import tkinter as tk
import time
from Maestro import Controller
WAIST = 0
MOTORS = 1
TURN = 2
HEADTURN = 3
HEADTILT = 4

class KeyControl():
    
    def __init__(self,win):
        self.root = win
        self.tango = Controller()
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.motors = 6000
        self.turn = 6000

        self.step = 200
        self.slowStep = 50
        self.fastStep = 400
        self.normalStep = 200

        self.stopSpeed = 6000

        self.sleepTime = .01
        
        self.currentMax = 7500
        self.currentMin = 4500
        
        self.normalMax = 7500
        self.normalMin = 4500
        
        self.slowMax = 6800
        self.slowMin = 5200
        
        self.fastMax = 8000
        self.fastMin = 2000

        self.leftKey = 113
        self.upKey = 116
        self.rightKey = 114
        self.downKey = 111
        self.spaceKey = 65
        self.qKey = 24
        self.wKey = 25
        self.eKey = 26
        self.rKey = 27
        self.aKey = 38
        self.sKey = 39
        self.dKey = 40
        self.zKey = 52
        self.xKey = 53
        self.cKey = 54

    def checkKey(self, key):
        ##print(key.keycode)
        if key.keycode == self.leftKey:
            self.goLeft()
        if key.keycode == self.upKey:
            self.goForward()
        if key.keycode == self.rightKey:
            self.goRight()
        if key.keycode == self.downKey:
            self.goReverse()
        if key.keycode == self.spaceKey:
            self.goStop()
        if key.keycode == self.qKey:
            self.bodyLeft()
        if key.keycode == self.wKey:
            self.bodyCenter()
        if key.keycode == self.eKey:
            self.bodyRight()
        if key.keycode == self.aKey:
            self.headLeft()
        if key.keycode == self.sKey:
            self.headCenter()
        if key.keycode == self.dKey:
            self.headRight()
        if key.keycode == self.zKey:
            self.tiltUp()
        if key.keycode == self.xKey:
            self.tiltCenter()
        if key.keycode == self.cKey:
            self.tiltDown()
        if key.keycode == self.rKey:
            self.changeSpeed()
        
##    def arrow(self, key):
##        print(key.keycode)
##        if key.keycode == 38:
##            self.motors += 200
##            if(self.motors > 7900):
##                self.motors = 7900
##            print(self.motors)

            #self.tango.setTarget(MOTORS, self.motors)


    def changeSpeed(self):
        self.goStop()
        if (self.currentMax == self.normalMax):
            self.currentMax = self.fastMax
            self.currentMin = self.fastMin
            ##print("Now in fast mode")

        elif (self.currentMax == self.fastMax):
            self.currentMax = self.slowMax
            self.currentMin = self.slowMin
            ##print("Now in slow mode")

        elif (self.currentMax == self.slowMax):
            self.currentMax = self.normalMax
            self.currentMin = self.normalMin
            ##print("Now in normal mode")

    def goLeft(self):
        self.turn += self.step
        if(self.turn < self.stopSpeed):
            self.turnStop()
        if (self.turn > self.currentMax):
            self.turn = self.currentMax
        self.tango.setTarget(TURN, self.turn)
        ##print("going left")
        
    def goForward(self):
        self.motors += self.step
        if(self.motors > self.currentMax):
            self.motors = self.currentMax
        self.tango.setTarget(MOTORS, self.motors)
        print("going forward: ", self.motors)

    def bodyLeft(self):
        self.body += self.fastStep
        if(self.body > self.fastMax):
            self.body = self.fastMax
        self.tango.setTarget(WAIST, self.body)

    def bodyRight(self):
        self.body -= self.fastStep
        if(self.body < self.fastMin):
            self.body = self.fastMin
        self.tango.setTarget(WAIST, self.body)

    def headRight(self):
        self.headTurn -= self.fastStep
        if(self.headTurn < self.fastMin):
            self.headTurn = self.fastMin
        self.tango.setTarget(HEADTURN, self.headTurn)

    def headLeft(self):
        self.headTurn += self.fastStep
        if(self.headTurn > self.fastMax):
            self.headTurn = self.fastMax
        self.tango.setTarget(HEADTURN, self.headTurn)

    def headCenter(self):
        self.headTurn = self.stopSpeed
        self.tango.setTarget(HEADTURN, self.headTurn)

    def tiltDown(self):
        self.headTilt -= self.fastStep
        if(self.headTilt < self.fastMin):
            self.headTilt = self.fastMin
        self.tango.setTarget(HEADTILT, self.headTilt)

    def tiltUp(self):
        self.headTilt += self.fastStep
        if(self.headTilt > self.fastMax):
            self.headTilt = self.fastMax
        self.tango.setTarget(HEADTILT, self.headTilt)

    def tiltCenter(self):
        self.headTilt = self.stopSpeed
        self.tango.setTarget(HEADTILT, self.headTilt)

    def bodyCenter(self):
        self.body = self.stopSpeed
        self.tango.setTarget(WAIST, self.stopSpeed)
        
    def goRight(self):
        self.turn -= self.step
        if (self.turn > self.stopSpeed):
            self.turnStop()
        if (self.turn < self.currentMin):
            self.turn = self.currentMin
        self.tango.setTarget(TURN, self.turn)
        ##print("going right")
        
    def goReverse(self):
        self.motors -= self.step
        if(self.motors < self.currentMin):
            self.motors = self.currentMin
        self.tango.setTarget(MOTORS, self.motors)
        print("going reverse: ", self.motors)

    def goStop(self):
        self.step = self.slowStep
        if(self.motors > self.stopSpeed):
            while self.motors > self.stopSpeed:
                self.goReverse()
                time.sleep(self.sleepTime)
        else:
            while self.motors < self.stopSpeed:
                self.goForward()
                time.sleep(self.sleepTime)
        self.step = self.normalStep
        self.tango.setTarget(MOTORS, self.stopSpeed)
        self.turnStop()

    def turnStop(self):
        self.turn = self.stopSpeed
        self.tango.setTarget(TURN, self.stopSpeed)
        
win = tk.Tk()
keys = KeyControl(win)
win.bind('<Up>', keys.checkKey)   #38
win.bind('<Down>', keys.checkKey) #40
win.bind('<Left>', keys.checkKey) #37
win.bind('<Right>', keys.checkKey)#39
win.bind('<space>', keys.checkKey)
win.bind('<q>', keys.checkKey)
win.bind('<w>', keys.checkKey)
win.bind('<e>', keys.checkKey)
win.bind('<r>', keys.checkKey)
win.bind('<a>', keys.checkKey)
win.bind('<d>', keys.checkKey)
win.bind('<s>', keys.checkKey)
win.bind('<z>', keys.checkKey)
win.bind('<x>', keys.checkKey)
win.bind('<c>', keys.checkKey)

win.mainloop()