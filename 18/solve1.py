#!/usr/bin/python3

#debug = False
debug = True
if debug:
    inputfile = "sample3.txt"
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

def clearroutes(themap):
    for loc in themap:
        try:
            del themap[loc]["dist"]
        except KeyError:
            pass
        try:
            del themap[loc]["barriers"]
        except KeyError:
            pass


keys = []
for loc in mymap:
    if 97 <= ord(mymap[loc]["ch"]) <= 122: #lower case letters
        keys.append(mymap[loc]["ch"])
#keys = "abcdefghijklmnopqrstuvwxyz"
doors = [key.upper() for key in keys]
routestartchars = keys.copy()
routestartchars.append("@")

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

#find all possible routes
routes = []
for routestartloc in mymap:
    if mymap[routestartloc]["ch"] not in routestartchars:
        continue
    computeroutes(mymap,routestartloc)
    for routeendloc in mymap:
        if mymap[routeendloc]["ch"] not in keys:
            continue
        if routeendloc == routestartloc:
            continue
        route = {"startch": mymap[routestartloc]["ch"],
                 "endch": mymap[routeendloc]["ch"],
                 "barriers": mymap[routeendloc]["barriers"],
                 "steps": mymap[routeendloc]["dist"]}
        routes.append(route)
    clearroutes(mymap)

#reorganize route data for better performance
newroutes = {}
for routestartchar in routestartchars:
    newroutes[routestartchar] = {}
    for routeendchar in keys:
        if routestartchar != routeendchar:
            newroutes[routestartchar][routeendchar] = {}
for oldroute in routes:
    newroutes[oldroute["startch"]][oldroute["endch"]]["barriers"] = set(oldroute["barriers"])
    newroutes[oldroute["startch"]][oldroute["endch"]]["steps"] = oldroute["steps"]

# for route in newroutes:
#     print("{}: {}".format(route,newroutes[route]))

def getstepstocomplete(fromch,passabledoors):
    if len(passabledoors) == len(keys): 
        return 0
    neededkeys = set(doors) - passabledoors #26% of time
    neededkeys = [neededkey.lower() for neededkey in neededkeys] #10% of time
    destopts = []
    for neededkey in neededkeys:
        if newroutes[fromch][neededkey]["barriers"].issubset(passabledoors):#10%
            destopts.append(neededkey)

    destoptsteps = []
    for destopt in destopts:
        newpassabledoors = passabledoors.copy()
        newpassabledoors.add(destopt.upper())
        stepsafterroute = getstepstocomplete(destopt,newpassabledoors)
        destoptstep = newroutes[fromch][destopt]["steps"] + stepsafterroute
        destoptsteps.append(destoptstep)
    return min(destoptsteps) #5.6%
        
print(getstepstocomplete("@",set()))

