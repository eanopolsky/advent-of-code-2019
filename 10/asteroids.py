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

vischecks = []
for a1 in asteroids:
    viscount = 0
    for a2 in (asteroids - set([a1])):
        if mutuallyvisible(asteroids,a1,a2):
            viscount += 1
    vischeck = {"asteroid": a1, "viscount": viscount}
    vischecks.append(vischeck)

vischecks.sort(key= lambda vischeck: vischeck["viscount"],reverse=True)
print(vischecks[0])
