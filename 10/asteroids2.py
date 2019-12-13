#!/usr/bin/python3

import cmath

asteroids = set()
with open("map.txt","r") as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                asteroids.add(complex(x,y)) #.real = x, .imag = y

def mutuallyvisible(aset,a1,a2):
    #a1 is the reference point
    iset = aset - set([a1]) - set([a2]) # interfering asteroids
    cansee = True #until something interferes
    r,phi = cmath.polar(a2-a1)
    for ia in iset:
        newr, newphi = cmath.polar(ia-a1)
        if newphi == phi and newr < r:
            cansee = False
            break
    return cansee

print("computing station location")
vischecks = []
for a1 in asteroids:
    viscount = 0
    for a2 in (asteroids - set([a1])):
        if mutuallyvisible(asteroids,a1,a2):
            viscount += 1
    vischeck = {"asteroid": a1, "viscount": viscount}
    vischecks.append(vischeck)

vischecks.sort(key= lambda vischeck: vischeck["viscount"],reverse=True)
station = vischecks[0]["asteroid"]
asteroids -= set([station])
print("station found at {}".format(station))
remainingtargets = list(asteroids)
# In the problem description, the laser starts pointing up and
# rotates clockwise. In normal polar coordinates this would be
# phi = pi/2, but because the positive y axis extends downward
# in this problem, it will be phi = 3pi/2. Also, clockwise
# rotation becomes counterclockwise rotation for the same
# reason. So, the laser rotation will increase phi (until it
# gets over 2pi and wraps back to 0).
#
#Might not need this:
#lasertargets.sort(key=lambda t: cmath.polar(t-station)[1])
vaporizedtargets = []
laserangle = cmath.polar(complex(0,-1))[1] #phi=3pi/2
while len(vaporizedtargets) < 200:
    possibletargets = list(filter(lambda t: cmath.polar(t-station)[1] == laserangle, remainingtargets))
    if len(possibletargets) == 0: #miss. advance the laser.
        higherangletargets = list(filter(lambda t: cmath.polar(t-station)[1] > laserangle,remainingtargets))
        if len(higherangletargets) == 0:
            laserangle=0
            continue
        else:
            higherangletargets.sort(key=lambda t:cmath.polar(t-station)[1])
            laserangle = cmath.polar(higherangletargets[0])[1]
            continue
    else: #hit. vaporize the closest one
        possibletargets.sort(key=lambda t:cmath.polar(t-station)[0])
        unluckyasteroid = possibletargets[0]
        vaporizedtargets.append(unluckyasteroid)
        remainingtargets.remove(unluckyasteroid)
        print("zapped {}, total: {}".format(unluckyasteroid,len(vaporizedtargets)))
        continue

print(vaporizedtargets[199])
