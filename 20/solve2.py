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
    for loc in newlayer:
        newlayer[loc]["layer"] = layernum
    if layernum == 0:
        for loc in newlayer:
            try:
                if newlayer[loc]["portal"] == "AA":
                    newlayer[loc]["start"] = True
                if newlayer[loc]["portal"] == "ZZ":
                    newlayer[loc]["end"] = True
            except KeyError:
                pass
    else:
        prevlayernum = layernum -1
        prevlayer = layers[prevlayernum]
        for portalname in portalnames:
            if portalname == "AA" or portalname == "ZZ":
                continue
            for loc in newlayer:
                try:
                    if (newlayer[loc]["portal"] == portalname and
                        newlayer[loc]["portaldir"] == "out"):
                        newlayerportalloc = loc
                        break
                except KeyError:
                    continue
            for loc in prevlayer:
                try:
                    if (prevlayer[loc]["portal"] == portalname and
                        prevlayer[loc]["portaldir"] == "in"):
                        prevlayerportalloc = loc
                        break
                except KeyError:
                    continue
            #portaldest now includes a destination layer and location
            prevlayer[prevlayerportalloc]["portaldest"] = (layernum,
                                                           newlayerportalloc)
            newlayer[newlayerportalloc]["portaldest"] = (prevlayernum,
                                                         prevlayerportalloc)
addlayer()
# addlayer()
# for layernum in range(len(layers)):
#     for loc in layers[layernum]:
#         if "portal" in layers[layernum][loc]:
#             print(layernum,loc,layers[layernum][loc])
# exit(1)

for loc in layers[0]:
    if "start" in layers[0][loc]:
        startloc = (0,loc)
    if "end" in layers[0][loc]:
        endloc = (0,loc)

def linkportals():
    if (len(layers) == 1):
        return #no portals to link
    for portalname in portalnames:
        if portalname == "AA" or portalname == "ZZ":
            continue
        hlayernum = len(layers)-2
        hlayer = layers[hlayernum]
        llayernum = len(layers)-1
        llayer = layers[llayernum]
        hconnectedspace = [loc for loc in hlayer
                           if "portal" in hlayer[loc]
                           and hlayer[loc]["portal"] == portalname
                           and hlayer[loc]["portaldir"] == "in"][0]
        lconnectedspace = [loc for loc in llayer
                           if "portal" in llayer[loc]
                           and llayer[loc]["portal"] == portalname
                           and llayer[loc]["portaldir"] == "out"][0]
        #print(hconnectedspace,lconnectedspace)
        #exit(1)
        hlayer[hconnectedspace]["portaldest"] = (llayernum,lconnectedspace)
        llayer[lconnectedspace]["portaldest"] = (hlayernum,hconnectedspace)

addlayer()
linkportals()
exit(1)



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
