#!/usr/bin/python3

import math

width = 25
height = 6

with open("dsn.txt") as f:
    pixelstring = f.readline().strip("\n")

numlayers = math.ceil(len(pixelstring) / (width*height))
layers = []
for i in range(numlayers):
    layer = {}
    for x in range(width):
        for y in range(height):
            layer[(x,y)] = int(pixelstring[width*height*i + width*y + x])
    layers.append(layer)

compositeimage = layers[0].copy()
for layer in layers:
    for x in range(width):
        for y in range(height):
            if compositeimage[(x,y)] == 2:
                compositeimage[(x,y)] = layer[(x,y)]

for y in range(height):
    for x in range(width):
        if compositeimage[(x,y)] == 0:
            print(" ",end="")
        elif compositeimage[(x,y)] == 1:
            print("#",end="")
        else:
            print("error")
            exit(1)
    print("")
