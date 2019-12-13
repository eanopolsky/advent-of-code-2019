#!/usr/bin/python3

with open("orbitmap.txt") as f:
    orbits = f.readlines()
orbits = [x.strip() for x in orbits]

celestialobjects = {}

for orbit in orbits:
    parent, child = orbit.split(")")
    if parent not in celestialobjects:
        celestialobjects[parent] = {"children":[child],
                                    "parent":"",
                                    "depth":"unknown"}
    else:
        celestialobjects[parent]["children"].append(child)
    if child in celestialobjects:
        celestialobjects[child]["parent"] = parent
    else:
        celestialobjects[child] = {"children":[],
                                   "parent": parent,
                                   "depth":"unknown"}

def getdepth(objname):
    #print("getting depth for {}".format(objname))
    if objname == "COM":
        return 0
    if celestialobjects[objname]["depth"] != "unknown":
        return celestialobjects[objname]["depth"]
    else:
        parentname = celestialobjects[objname]["parent"]
        return 1+getdepth(parentname)

for x in celestialobjects:
    #print(x,celestialobjects[x])
    celestialobjects[x]["depth"] = getdepth(x)

youparents = set()
obj="YOU"
while(True):
    obj = celestialobjects[obj]["parent"]
    youparents.add(obj)
    if obj == "COM":
        break

sanparents = set()
obj="SAN"
while(True):
    obj = celestialobjects[obj]["parent"]
    sanparents.add(obj)
    if obj == "COM":
        break

sharedparents = list(youparents & sanparents)
sharedparents.sort(key=lambda obj:celestialobjects[obj]["depth"],reverse=True)
bestparent = sharedparents[0]
transfers2bestparent = celestialobjects["YOU"]["depth"] - celestialobjects[bestparent]["depth"] - 1
transfers2santa = celestialobjects["SAN"]["depth"] - celestialobjects[bestparent]["depth"] - 1
print(transfers2bestparent + transfers2santa)
