#!/usr/bin/python3

debug = False
#debug = True

#inputfile = "sample1b.txt"
inputfile = "sample2b.txt"
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

#Because the map is simply connected, the keys that are required to
#reach any given destination fall into two sets:
# * The set of keys necessary to reach the destination starting from @.
# * The set of keys that the player must already have based on their
#   current location.
# To continue, we need two directories of information:
# 1. The number of steps from each key (or @) to each other key.
# 2. The keys needed to get from @ to each key.

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
    routestartchars = set(["@"]).union(vault["accessiblekeys"])

    #find all routes within vault
    routes = []
    for routestartloc in mymap:
        if routestartloc not in vault["accessiblelocations"]:
            continue
        if mymap[routestartloc]["ch"] not in routestartchars:
            continue
        computeroutes(mymap,routestartloc)
        for routeendloc in mymap:
            if mymap[routeendloc]["ch"] not in vault["accessiblekeys"]:
                continue
            if routeendloc == routestartloc:
                continue
            route = {"startch": mymap[routestartloc]["ch"],
                     "endch": mymap[routeendloc]["ch"],
                     "barriers": mymap[routeendloc]["barriers"],
                     "steps": mymap[routeendloc]["dist"]}
            routes.append(route)
        clearroutes(mymap)
    vault["routes"] = routes
    #store graph edge cost for this vault in steps directory:
    stepsdir = {} #"fromlocation": {"tolocation1": 20, "loc2": 33, ...
    for routestartchar in routestartchars:
        stepsdir[routestartchar] = {}
        for routeendchar in vault["accessiblekeys"]:
            if routestartchar == routeendchar:
                continue
            stepsdir[routestartchar][routeendchar] = {}
    for route in vault["routes"]:
        stepsdir[route["startch"]][route["endch"]] = route["steps"]
    vault["stepsdir"] = stepsdir
    keysneededtoaccess = {} #"a": set('b','c'), "b": set("x","y"), ...
    for route in vault["routes"]:
        if route["startch"] != "@":
            continue
        keysneeded = set([barrier.lower() for barrier in route["barriers"]])
        keysneededtoaccess[route["endch"]] = keysneeded
    vault["keysneededtoaccess"] = keysneededtoaccess

# for vault in vaults:
#     print(vault)



pathcache = {}
#entries:
# tuple(fromch,set(keyring)): numsteps

# fromchs is now a list the same length as vaults.
#
# Each element of fromchs is a character referencing the current location
# of the robot in that vault. For example, if fromchs[2] == "v", then the
# robot in vaults[2] is at key "v".
#
# keyring is a shared keyring among all robots
def getstepstocomplete(fromchs,keyring):
    #pathcachekey = tuple([fromch, tuple(sorted(list(keyring)))])
    if debug:
        print("")
        print("Robot locations: {}. Shared keyring: {}".format(fromchs, keyring))
    # if pathcachekey in pathcache:
    #     return pathcache[pathcachekey]
    if len(keyring) == len(keys):
        # pathcache[pathcachekey] = 0
        return 0
    neededkeys = keys - keyring
    #destopts now contains tuples of the form (vaultnum, key)
    # For example, the tuple (1, "c") would mean that we have the option
    # to dispatch the robot in vaults[1] to key "c".
    destopts = []
    for neededkey in neededkeys:
        for i in range(len(vaults)):
            vault = vaults[i]
            try:
                if vault["keysneededtoaccess"][neededkey].issubset(keyring):
                    destopt = {"vaultnum": i,
                               "destkey": neededkey}
                    destopts.append(destopt)
            except KeyError:
                #neededkey not available in vault i
                pass
    if debug:
        print("available next steps: {}".format(destopts))
        input("press enter to continue")

    destoptsteps = []
    for destopt in destopts:
        newkeyring = keyring.copy()
        newkeyring.add(destopt["destkey"])
        newrobotchs = fromchs.copy()
        newrobotchs[destopt["vaultnum"]] = destopt["destkey"]
        stepsafterdestopt = getstepstocomplete(newrobotchs,newkeyring)
        #not updated to support multiple robots yet:
        #destoptstep = stepsdir[fromch][destopt] + stepsafterroute
        stepstodestopt = vaults[destopt["vaultnum"]]["stepsdir"][fromchs[destopt["vaultnum"]]][destopt["destkey"]]
        destoptstep = stepstodestopt + stepsafterdestopt
        destoptsteps.append(destoptstep)        

    # pathcache[pathcachekey] = min(destoptsteps)
    return min(destoptsteps)
        
print(getstepstocomplete(fromchs=["@" for vault in vaults],keyring=set()))

