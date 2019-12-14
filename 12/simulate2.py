#!/usr/bin/python3

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



def applygravity(universe):
    for x in (0,6,12,18):
        for other in (0,6,12,18):
            if x != other and universe[x] != universe[other]:
                universe[x+3] += (1 if universe[x] < universe[other] else -1)
    for y in (1,7,13,19):
        for other in (1,7,13,19):
            if y != other and universe[y] != universe[other]:
                universe[y+3] += (1 if universe[y] < universe[other] else -1)
    for z in (2,8,14,20):
        for other in (2,8,14,20):
            if z != other and universe[z] != universe[other]:
                universe[z+3] += (1 if universe[z] < universe[other] else -1)


def applyvelocity(universe):
    for i in (0,1,2,6,7,8,12,13,14,18,19,20):
        universe[i] += universe[i+3]

#if tuple(universe) in previousuniverses

previousuniverses = set()
iterations = 0

while True:
    if tuple(universe) in previousuniverses:
        print(iterations)
        break
    if iterations % 100000 == 0:
        print(iterations)
        previousuniverses.add(tuple(universe)) #useful for approximating
    applygravity(universe)
    applyvelocity(universe)
    iterations += 1

