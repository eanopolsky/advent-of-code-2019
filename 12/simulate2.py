#!/usr/bin/python3

from math import gcd

universe = []
with open("sanitized.txt","r") as f:
    for line in f:
        x,y,z = line.rstrip("\n").split(",")
        universe.append(int(x))
        universe.append(int(y))
        universe.append(int(z))
        universe.append(0) #x velocity
        universe.append(0) #y velocity
        universe.append(0) #z velocity

def applygravity(universe,axes=["x","y","z"]):
    if "x" in axes:
        for x in (0,6,12,18):
            for other in (0,6,12,18):
                if x != other and universe[x] != universe[other]:
                    universe[x+3] += (1 if universe[x] < universe[other] else -1)
    if "y" in axes:
        for y in (1,7,13,19):
            for other in (1,7,13,19):
                if y != other and universe[y] != universe[other]:
                    universe[y+3] += (1 if universe[y] < universe[other] else -1)
    if "z" in axes:
        for z in (2,8,14,20):
            for other in (2,8,14,20):
                if z != other and universe[z] != universe[other]:
                    universe[z+3] += (1 if universe[z] < universe[other] else -1)


def applyvelocity(universe,axes=["x","y","z"]):
    #for i in (0,1,2,6,7,8,12,13,14,18,19,20):
    #    universe[i] += universe[i+3]
    if "x" in axes:
        for i in (0,6,12,18):
            universe[i] += universe[i+3]
    if "y" in axes:
        for i in (1,7,13,19):
            universe[i] += universe[i+3]
    if "z" in axes:
        for i in (2,8,14,20):
            universe[i] += universe[i+3]

def findperiod(universe,axis):
    startuniverse = universe.copy()
    previousuniverses = set()
    iterations = 0
    while True:
        if tuple(universe) in previousuniverses:
            break
        previousuniverses.add(tuple(universe))
        applygravity(universe,axes=[axis])
        applyvelocity(universe,axes=[axis])
        iterations += 1
    secondoccurrenceiterations = iterations
    restartpoint = universe.copy()
    iterations = 0
    universe = startuniverse.copy()
    while True:
        if universe == restartpoint:
            break
        applygravity(universe,axes=[axis])
        applyvelocity(universe,axes=[axis])
        iterations += 1
    firstoccurrenceiterations = iterations
    #
    #It turns out this is always 0 for my first puzzle input, but it
    #didn't have to be. Assuming it's always 0 simplifies the code.
    #
    #print(firstoccurrenceiterations)
    return secondoccurrenceiterations

xperiod = findperiod(universe.copy(),"x")
yperiod = findperiod(universe.copy(),"y")
zperiod = findperiod(universe.copy(),"z")

totalperiod = int(xperiod * yperiod / gcd(xperiod,yperiod))
totalperiod = int(totalperiod * zperiod / gcd(totalperiod,zperiod))
print(totalperiod)

