#!/usr/bin/python3

from asciifb import asciifb

inputfile = "myinput.txt"
inputfile = "sample1.txt"


myfb = asciifb()
myfb.load(inputfile)
myfb.render()
mymap = myfb.getmap()

def serializemap(themap):
    x = 0
    y = 0
    serial = []
    while True:
        try:
            ch = themap[(x,y)]["ch"]
            if ch == "#" or ch == ".":
                serial.append(ch)
            x += 1
            continue
        except KeyError:
            if x == 0:
                break
            else:
                x = 0
                y += 1
    #print(tuple(serial))
    return tuple(serial)

def calcbrating(themap):
    serialmap = serializemap(themap)
    brating = 0
    for i in range(len(serialmap)):
        if serialmap[i] == "#":
            brating += 2 ** i
    return brating

print(calcbrating(mymap))
