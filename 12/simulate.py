#!/usr/bin/python3

moons = []
with open("sanitized.txt","r") as f:
    for line in f:
        x,y,z = line.rstrip("\n").split(",")
        moon = {"pos": {},
                "vel": {"x": 0,
                        "y": 0,
                        "z": 0}}
        moon["pos"]["x"] = int(x)
        moon["pos"]["y"] = int(y)
        moon["pos"]["z"] = int(z)
        moons.append(moon)

def applygravity(m1,m2):
    for axis in ["x","y","z"]:
        if m1["pos"][axis] < m2["pos"][axis]:
            m1["vel"][axis] += 1
            m2["vel"][axis] -= 1
        elif m1["pos"][axis] > m2["pos"][axis]:
            m2["vel"][axis] += 1
            m1["vel"][axis] -= 1
        else: #moons are at equal positions on this axis
            pass

def applyvelocity(moon):
    for axis in ["x","y","z"]:
        moon["pos"][axis] += moon["vel"][axis]

def showmoons():
    for moon in moons:
        print(moon)
    print("")

def getenergy(moon):
    axes = ["x","y","z"]
    posenergy = sum([moon["pos"][axis] for axis in axes])
    velenergy = sum([moon["vel"][axis] for axis in axes])
    return posenergy * velenergy
    
for step in range(1000):
    for i in range(len(moons)-1): #index of first moon
        for j in range(i+1,len(moons)):
            applygravity(moons[i],moons[j])
    for moon in moons:
        applyvelocity(moon)

print(sum([getenergy(moon) for moon in moons]))
    
