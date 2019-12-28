#!/usr/bin/python3

debug = False
#debug = True

inputfile = "sample1b.txt"
#inputfile = "myinput2.txt"

from asciifb import asciifb

myfb = asciifb()
with open(inputfile,"r") as f:
    for line in f:
        for char in line:
            myfb.receivechar(char)

mymap = myfb.getmap()
# multiple robot start locations
robotstartlocs = [coord for coord in mymap if mymap[coord]["ch"] == "@"]

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
keys = set(keys)
doors = set([key.upper() for key in keys])

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



vaults = []
for robotstartloc in robotstartlocs:
    vault = {}
    vault["robotstartloc"] = robotstartloc
    vaults.append(vault)
# print(vaults)
# exit(1)

for vault in vaults:
    keyspresent = set()
    computeroutes(mymap,vault["robotstartloc"])
    vault["accessiblelocations"] = set()
    vault["accessiblekeys"] = set()
    for loc in mymap:
        if "dist" in mymap[loc]:
            vault["accessiblelocations"].add(loc)
            if mymap[loc]["ch"] in keys:
                vault["accessiblekeys"].add(mymap[loc]["ch"])
    clearroutes(mymap)
    startchars = set(["@"])

print(vaults)
exit(1)
    
    


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

#Because the map is simply connected, the keys that are required to
#reach any given destination fall into two sets:
# * The set of keys necessary to reach the destination starting from @.
# * The set of keys that the player must already have based on their
#   current location.
# To continue, we need two directories of information:
# 1. The number of steps from each key (or @) to each other key.
# 2. The keys needed to get from @ to each key.

stepsdir = {} #"fromlocation": {"tolocation1": 20, "loc2": 33, ...
for routestartchar in routestartchars:
    stepsdir[routestartchar] = {}
    for routeendchar in keys:
        if routestartchar == routeendchar:
            continue
        stepsdir[routestartchar][routeendchar] = {}
for route in routes:
    stepsdir[route["startch"]][route["endch"]] = route["steps"]

keysneededtoaccess = {} #"a": set('b','c'), "b": set("x","y"), ...
for route in routes:
    if route["startch"] != "@":
        continue
    keysneeded = set([barrier.lower() for barrier in route["barriers"]])
    keysneededtoaccess[route["endch"]] = keysneeded

# for start in stepsdir:
#     print("{}: {}".format(start,stepsdir[start]))
# for key in keysneededtoaccess:
#     print("{}: {}".format(key,keysneededtoaccess[key]))
# exit(1)

pathcache = {}
#entries:
# tuple(fromch,set(keyring)): numsteps

def getstepstocomplete(fromch,keyring):
    pathcachekey = tuple([fromch, tuple(sorted(list(keyring)))])
    if debug:
        print("")
        print("now at {}. Keyring: {}".format(fromch, keyring))
    if pathcachekey in pathcache:
        return pathcache[pathcachekey]
    if len(keyring) == len(keys):
        pathcache[pathcachekey] = 0
        return 0
    neededkeys = keys - keyring
    destopts = []
    for neededkey in neededkeys:
        if keysneededtoaccess[neededkey].issubset(keyring):
            destopts.append(neededkey)
    if debug:
        print("available next steps: {}".format(destopts))
        input("press enter to continue")
    destoptsteps = []
    for destopt in destopts:
        newkeyring = keyring.copy()
        newkeyring.add(destopt)
        stepsafterroute = getstepstocomplete(destopt,newkeyring)
        destoptstep = stepsdir[fromch][destopt] + stepsafterroute
        destoptsteps.append(destoptstep)
    pathcache[pathcachekey] = min(destoptsteps)
    return min(destoptsteps)
        
print(getstepstocomplete("@",set()))

