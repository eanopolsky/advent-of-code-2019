#!/usr/bin/python3

from asciifb import asciifb
from copy import deepcopy

inputfile = "myinput.txt"

myfb = asciifb()
myfb.load(inputfile)
mymap = myfb.getmap()

basemap = {}
for loc in mymap:
    ch = mymap[loc]["ch"]
    if ch == "#" or ch == ".":
        basemap[loc] = ch

basemap[(2,2)] = "?"
cleanmap = deepcopy(basemap)
for loc in cleanmap:
    if loc != (2,2):
        cleanmap[loc] = "."

grids = {} #depth: map dictionary
grids[0] = basemap

def addgridsifnecessary():
    depths = grids.keys()
    mindepth = min(depths)
    mindepthgrid = grids[mindepth]
    maxdepth = max(depths)
    maxdepthgrid = grids[maxdepth]

    needsmallerdepth = False
    for loc in mindepthgrid:
        if loc[0] == 0 or loc[0] == 4 or loc[1] == 0 or loc[1] == 4:
            if mindepthgrid[loc] == "#":
                needsmallerdepth = True
                break
    if needsmallerdepth:
        newgrid = deepcopy(cleanmap)
        grids[mindepth-1] = newgrid

    needlargerdepth = False
    for loc in [(2,1), (3,2), (2,3), (1,2)]:
        if maxdepthgrid[loc] == "#":
            needlargerdepth = True
            break
    if needlargerdepth:
        newgrid = deepcopy(cleanmap)
        grids[maxdepth+1] = newgrid

def rendergrids():
    depths = sorted(grids.keys())
    for depth in depths:
        print("Depth {}:".format(depth))
        for y in range(5):
            for x in range(5):
                print(grids[depth][(x,y)],end="")
            print("")
        print("")
    
addgridsifnecessary()
addgridsifnecessary()
rendergrids()
exit(1)

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
                
# myfb.render()
# myfb.setmap(evolvemap(mymap))
# myfb.render()

seenstates = set()
while True:
    seenstates.add(serializemap(mymap))
    mymap = evolvemap(mymap)
    if serializemap(mymap) in seenstates:
        print(calcbrating(mymap))
        break
