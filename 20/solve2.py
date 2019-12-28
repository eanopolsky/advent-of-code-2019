#!/usr/bin/python3

from copy import deepcopy

#debug = False
#debug = True

inputfile = "sample1.txt"
#inputfile = "sample2.txt"
#inputfile = "myinput.txt"

from asciifb import asciifb

myfb = asciifb()
with open(inputfile,"r") as f:
    for line in f:
        for char in line:
            myfb.receivechar(char)
#myfb.render()

mymap = myfb.getmap()

#find dimensions of map
#and boundaries of inner ring/rectangle
width = 0
height = 0
for loc in mymap:
    if loc[0] > width:
        width = loc[0]
    if loc[1] > height:
        height = loc[1]
center = (int(width/2),int(height/2))
#print(center)
innerring = {}
x = center[0]
while True:
    if mymap[(x,center[1])]["ch"] == "." or mymap[(x,center[1])]["ch"] == "#":
        innerring["startx"] = x
        break
    else:
        x -= 1
x = center[0]
while True:
    if mymap[(x,center[1])]["ch"] == "." or mymap[(x,center[1])]["ch"] == "#":
        innerring["endx"] = x
        break
    else:
        x += 1
y = center[1]
while True:
    if mymap[(center[0],y)]["ch"] == "." or mymap[(center[0],y)]["ch"] == "#":
        innerring["starty"] = y
        break
    else:
        y -= 1
y = center[1]
while True:
    if mymap[(center[0],y)]["ch"] == "." or mymap[(center[0],y)]["ch"] == "#":
        innerring["endy"] = y
        break
    else:
        y += 1
#print(innerring)

# tag portal-adjacent spaces
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for loc in mymap:
    if mymap[loc]["ch"] == ".":
        portal = ""
        portaldir = ""
        if mymap[(loc[0]-1,loc[1])]["ch"] in letters:
            portal = mymap[(loc[0]-2,loc[1])]["ch"] + mymap[(loc[0]-1,loc[1])]["ch"]
        elif mymap[(loc[0]+1,loc[1])]["ch"] in letters:
            portal = mymap[(loc[0]+1,loc[1])]["ch"] + mymap[(loc[0]+2,loc[1])]["ch"]
        elif mymap[(loc[0],loc[1]-1)]["ch"] in letters:
            portal = mymap[(loc[0],loc[1]-2)]["ch"] + mymap[(loc[0],loc[1]-1)]["ch"]
        elif mymap[(loc[0],loc[1]+1)]["ch"] in letters:
            portal = mymap[(loc[0],loc[1]+1)]["ch"] + mymap[(loc[0],loc[1]+2)]["ch"]
        else:
            continue
        mymap[loc]["portal"] = portal
        if (innerring["startx"] <= loc[0] <= innerring["endx"] and
            innerring["starty"] <= loc[1] <= innerring["endy"]):
            mymap[loc]["portaldir"] = "in"
        else:
            mymap[loc]["portaldir"] = "out"

print(mymap)
exit(1)

originalmap = mymap
layers = []

portalnames = set()
for loc in mymap:
    if "portal" in mymap[loc]:
        portalnames.add(mymap[loc]["portal"])

def addlayer():
    newlayer = deepcopy(originalmap)
    layernum = len(layers)
    layers.append(newlayer)
    if layernum == 0:
        for loc in newlayer:
            if newlayer[loc]["portal"] == "AA":
                newlayer[loc]["start"] = True
            if newlayer[loc]["portal"] == "ZZ":
                newlayer[loc]["end"] = True
    else:
        prevlayer = layernum - 1
        #incomplete. needs portal linking between this
        #layer and previous layer
                

exit(1)
for loc in mymap:
    if "start" in mymap[loc]:
        startloc = loc
    if "end" in mymap[loc]:
        endloc = loc


for portalname in portalnames:
    connectedspaces = [loc for loc in mymap if "portal" in mymap[loc] and mymap[loc]["portal"] == portalname]
    if len(connectedspaces) != 2:
        print("error while finding linked spaces")
        exit(1)
    else:
        mymap[connectedspaces[0]]["portaldest"] = connectedspaces[1]
        mymap[connectedspaces[1]]["portaldest"] = connectedspaces[0]

# #shows links between spaces that have portals
# for loc in mymap:
#     if "portaldest" in mymap[loc]:
#         print("{} links to {}".format(loc,mymap[loc]["portaldest"]))

def getneighborspaces(loc):
    adjacent = []
    adjacent.append((loc[0]-1,loc[1]))
    adjacent.append((loc[0]+1,loc[1]))
    adjacent.append((loc[0],loc[1]-1))
    adjacent.append((loc[0],loc[1]+1))
    neighbors = []
    for space in adjacent:
        if mymap[space]["ch"] == ".":
            neighbors.append(space)
    if "portaldest" in mymap[loc]:
        neighbors.append(mymap[loc]["portaldest"])
    return neighbors

# def clearroutes(themap):
#     for loc in themap:
#         try:
#             del themap[loc]["dist"]
#         except KeyError:
#             pass
#         try:
#             del themap[loc]["barriers"]
#         except KeyError:
#             pass

def computedists(themap,startloc):
    themap[startloc]["dist"] = 0
    wavefront = [startloc]
    while len(wavefront) != 0:
        newwavefront = []
        for loc in wavefront:
            ns = getneighborspaces(loc) #returns only passable neighbors: ., portals
            for n in ns:
                if "dist" not in themap[n]:
                    themap[n]["dist"] = themap[loc]["dist"] + 1
                    newwavefront.append(n)
                    continue
                if themap[n]["dist"] > themap[loc]["dist"] + 1:
                    themap[n]["dist"] = themap[loc]["dist"] + 1
                    newwavefront.append(n)
                    continue
        wavefront = newwavefront

computedists(mymap,startloc)

print(mymap[endloc]["dist"])
