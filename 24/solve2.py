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
    

def getneighborspaces(depth,loc):
    ns = [] #element: {"depth": depth, "loc": loc}
    #for points on the outside edges
    if loc[0] == 0:
        ns.append({"depth": depth - 1, "loc": (1,2)})
    if loc[0] == 4:
        ns.append({"depth": depth - 1, "loc": (3,2)})
    if loc[1] == 0:
        ns.append({"depth": depth - 1, "loc": (2,1)})
    if loc[1] == 4:
        ns.append({"depth": depth - 1, "loc": (2,3)})

    #for points on the inside edges:
    if loc == (2,1):
        for x in range(5):
            ns.append({"depth": depth + 1, "loc": (x,0)})
    if loc == (2,3):
        for x in range(5):
            ns.append({"depth": depth + 1, "loc": (x,4)})
    if loc == (1,2):
        for y in range(5):
            ns.append({"depth": depth + 1, "loc": (0,y)})
    if loc == (3,2):
        for y in range(5):
            ns.append({"depth": depth + 1, "loc": (4,y)})

    #neighbors at same depth
    samedepthoptions = [(loc[0]-1,loc[1]),
                        (loc[0]+1,loc[1]),
                        (loc[0],loc[1]-1),
                        (loc[0],loc[1]+1)]
    for locopt in samedepthoptions:
        if 0 <= locopt[0] <= 4 and 0 <= locopt[1] <= 4:
            ns.append({"depth": depth, "loc": locopt})
    return ns

def evolvegrids():
    newgrids = deepcopy(grids)
    for depth in grids:
        for loc in grids[depth]:
            ns = getneighborspaces(depth=depth,loc=loc)#stopped here

print(getneighborspaces(0,(1,2)))
# addgridsifnecessary()
# addgridsifnecessary()
# rendergrids()
# exit(1)




# def evolvemap(oldmap):
#     newmap = deepcopy(oldmap)
#     for loc in oldmap:
#         ns = getneighborspaces(loc)
#         nbugcount = 0
#         for n in ns:
#             try:
#                 if oldmap[n]["ch"] == "#":
#                     nbugcount += 1
#             except KeyError:
#                 pass #on map edge
#         if oldmap[loc]["ch"] == "#":
#             if nbugcount == 1:
#                 newmap[loc]["ch"] = "#" #unnecessary but clear
#             else:
#                 newmap[loc]["ch"] = "."
#         elif oldmap[loc]["ch"] == ".": 
#             if 1 <= nbugcount <= 2:
#                 newmap[loc]["ch"] = "#"
#         else:
#             pass #ignore newline spaces
#     return newmap
                
