#!/usr/bin/python3

debug = True
if debug:
    inputfile = "sample1.txt"
else:
    inputfile = "myinput.txt"

from asciifb import asciifb

myfb = asciifb()
with open(inputfile,"r") as f:
    for line in f:
        for char in line:
            myfb.receivechar(char)

mymap = myfb.getmap()
startloc = [coord for coord in mymap if mymap[coord]["ch"] == "@"][0]

def getneighbors(loc):
    neighbors = []
    neighbors.append((loc[0]-1,loc[1]))
    neighbors.append((loc[0]+1,loc[1]))
    neighbors.append((loc[0],loc[1]-1))
    neighbors.append((loc[0],loc[1]+1))
    return neighbors

def computedistances(themap,startloc,keyring):
    passable = []
    passable.append("@") #start location
    passable.extend([ch for ch in "abcdefghijklmnopqrstuvwxyz"]) #keys
    passable.append(".") #clear tunnels
    passable.extend([ch.upper() for ch in keyring]) #unlocked doors
    #print(passable) #correct
    themap[startloc]["dist"] = 0
    lastnumdists = 0
    numdists = 1
    while numdists > lastnumdists:
        lastnumdists = numdists
        for loc in themap:
            if "dist" in themap[loc]:
                #distance to this location already computed
                #makes sense to skip recomputation if map is simply connected.
                #may produce suboptimal routes if map is not simply connected.
                continue 
            if themap[loc]["ch"] not in passable:
                continue #location cannot be occupied
            ns = getneighbors(loc)
            ndists = []
            for n in ns:
                try:
                    ndist = themap[n]["dist"]
                    ndists.append(ndist)
                except KeyError:
                    pass

            if len(ndists) == 0:
                #no helpful neighbors
                continue
            else:
                themap[loc]["dist"] = min(ndists)+1
        numdists = len([l for l in themap if "dist" in themap[l]])

computedistances(themap=mymap,startloc=startloc,keyring=[])
    
print(mymap)
