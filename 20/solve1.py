#!/usr/bin/python3

#debug = False
#debug = True

inputfile = "sample1.txt"
#inputfile = "myinput.txt"

from asciifb import asciifb

myfb = asciifb()
with open(inputfile,"r") as f:
    for line in f:
        for char in line:
            myfb.receivechar(char)
#myfb.render()

mymap = myfb.getmap()

# tag portal-adjacent spaces
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for loc in mymap:
    if mymap[loc]["ch"] == ".":
        portal = ""
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
        if portal == "AA":
            mymap[loc]["start"] = True
        elif portal == "ZZ":
            mymap[loc]["end"] = True
        else:
            mymap[loc]["portal"] = portal

# #portal tag check:
#
# for loc in mymap:
#     try:
#         print(mymap[loc]["portal"])
#     except KeyError:
#         pass
# exit(1)

for loc in mymap:
    if "start" in mymap[loc]:
        startloc = loc
    if "end" in mymap[loc]:
        endloc = loc

portalnames = set()
for loc in mymap:
    if "portal" in mymap[loc]:
        portalnames.add(mymap[loc]["portal"])

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
