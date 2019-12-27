#!/usr/bin/python3

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

def cleardistances(themap):
    for loc in themap:
        try:
            del themap[loc]["dist"]
        except KeyError:
            pass

keys = "abcdefghijklmnopqrstuvwxyz"

def computedistances(themap,startloc,keyring):
    passable = []
    passable.append("@") #start location
    passable.extend([ch for ch in keys]) #keys
    passable.append(".") #clear tunnels
    passable.extend([ch.upper() for ch in keyring]) #unlocked doors
    #print(passable) #correct
    themap[startloc]["dist"] = 0
    lastmaxdist = -1
    maxdist = 0
    while maxdist > lastmaxdist:
        lastmaxdist = maxdist
        newmaxdist = maxdist
        for loc in themap:
            if "dist" not in themap[loc] or themap[loc]["dist"] != maxdist:# 44% of time here
                continue #only consider the wavefront
            ns = getneighbors(loc)
            for n in ns:
                if "dist" in themap[n] or themap[n]["ch"] not in passable: # 24% of time here
                    continue
                else:
                    themap[n]["dist"] = themap[loc]["dist"] + 1
                    if themap[n]["dist"] > newmaxdist:
                        newmaxdist = themap[n]["dist"]
        maxdist = newmaxdist
                    

keyring = []
def getstepstocomplete(themap,startloc,keyring):
    computedistances(themap=themap,startloc=startloc,keyring=keyring) #works
    #cleardistances(mymap)
    destinations = [loc for loc in mymap
                    if "dist" in mymap[loc] #reachable
                    and mymap[loc]["ch"] in keys #consider only keys
                    and mymap[loc]["ch"] not in keyring ]#key we don't have
    # print(destinations)
    # for d in destinations:
    #     print(themap[d]["ch"])
    if len(destinations) == 0:
        #no more keys to collect
        return 0
    else:
        destdata = {}
        for d in destinations:
            destdata[d] = {"steps2dest": themap[d]["dist"]}
        for d in destinations:
            newkeyring = keyring.copy()
            newkeyring.append(themap[d]["ch"])
            cleardistances(themap)
            stepstocomplete = getstepstocomplete(themap,d,newkeyring)
            destdata[d]["stepsafterdest"] = stepstocomplete
        for d in destinations:
            destdata[d]["totalsteps"] = destdata[d]["steps2dest"] + \
                destdata[d]["stepsafterdest"]
        steptotals = [destdata[d]["totalsteps"] for d in destdata]
        return min(steptotals)

print(getstepstocomplete(themap=mymap,startloc=startloc,keyring=keyring))
