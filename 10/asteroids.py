#!/usr/bin/python3


asteroids = []
with open("map.txt","r") as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                asteroids.append((x,y))

#print(asteroids)
