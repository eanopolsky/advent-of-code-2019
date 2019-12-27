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

def cleardistances(themap):
    for loc in themap:
        try:
            del themap[loc]["dist"]
        except KeyError:
            pass
        try:
            del themap[loc]["barriers"]
        except KeyError:
            pass

keys = "abcdefghijklmnopqrstuvwxyz"
doors = keys.upper()

# need to build a route map:
#
# from: starting location (either @ or a key)
# to: ending location (always a key)
# barriers: list of doors traversed on the way
# steps: step count for route

def computeroutes(themap,startloc):
    themap[startloc]["dist"] = 0
    themap[startloc]["barriers"] = []
    wavefront = [startloc]
    while len(wavefront) != 0:
        newwavefront = []
        for loc in wavefront:
            ns = getneighbors(loc)
            for n in ns:
                if "dist" in themap[n]:
                    continue
                ch = themap[n]["ch"]
                if ch == "#":
                    continue
                else:
                    themap[n]["dist"] = themap[loc]["dist"] + 1
                    themap[n]["barriers"] = themap[loc]["barriers"].copy()
                    if ch in doors:
                        themap[n]["barriers"].append(ch)
                    newwavefront.append(n)
        wavefront = newwavefront

computeroutes(mymap,startloc)

for loc in mymap:
    print("{}: {}".format(loc,mymap[loc]))
