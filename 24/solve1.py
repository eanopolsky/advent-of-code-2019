#!/usr/bin/python3

from asciifb import asciifb
from copy import deepcopy

inputfile = "myinput.txt"
inputfile = "sample1.txt"


myfb = asciifb()
myfb.load(inputfile)
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

def getneighborspaces(loc):
    adjacent = []
    adjacent.append((loc[0]-1,loc[1]))
    adjacent.append((loc[0]+1,loc[1]))
    adjacent.append((loc[0],loc[1]-1))
    adjacent.append((loc[0],loc[1]+1))
    return adjacent


def evolvemap(oldmap):
    newmap = deepcopy(oldmap)
    for loc in oldmap:
        ns = getneighborspaces(loc)
        nbugcount = 0
        for n in ns:
            try:
                if oldmap[n]["ch"] == "#":
                    nbugcount += 1
            except KeyError:
                pass #on map edge
        if oldmap[loc]["ch"] == "#":
            if nbugcount == 1:
                newmap[loc]["ch"] = "#" #unnecessary but clear
            else:
                newmap[loc]["ch"] = "."
        elif oldmap[loc]["ch"] == ".": 
            if 1 <= nbugcount <= 2:
                newmap[loc]["ch"] = "#"
        else:
            pass #ignore newline spaces
    return newmap
                
myfb.render()
myfb.setmap(evolvemap(mymap))
myfb.render()
