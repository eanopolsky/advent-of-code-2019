#!/usr/bin/python3

class asciifb:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.screenmap = {} #element = (0,0): "#"
    def receiveint(self, n):
        if type(n) != type(int()):
            print("wrong type passed to receiveint")
            exit(1)
        try:
            self.screenmap[(self.x,self.y)]["ch"] = chr(n)
        except KeyError:
            self.screenmap[(self.x,self.y)] = {}
            self.screenmap[(self.x,self.y)]["ch"] = chr(n)
        if n == 10:
            self.y += 1
            self.x = 0
            return
        self.x += 1
    def receivechar(self, ch):
        if type(ch) != type("") or len(ch) != 1:
            print("wrong type passed to receivechar")
            exit(1)
        self.receiveint(ord(ch))
    def setpixel(self,x,y,v):
        if type(v) != type(""):
            print("invalid character type: {}".format(type(v)))
            exit(1)
        self.screenmap[(x,y)] = {}
        self.screenmap[(x,y)]["ch"] = v
    def getmap(self):
        return self.screenmap
    def render(self):
        rx = 0
        ry = 0
        while True: #iterate over lines
            while True: #iterate over line
                try:
                    print(self.screenmap[(rx,ry)]["ch"],end="")
                except KeyError:
                    if self.screenmap[(rx-1,ry)]["ch"] != "\n":
                        #line is not newline-terminated
                        print("") #render line properly
                    break
                rx += 1
            ry += 1
            rx = 0
            if (rx,ry) not in self.screenmap:
                break
