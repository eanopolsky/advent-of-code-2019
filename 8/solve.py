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

zerocounts = []
for i in range(len(layers)):
    layer = layers[i]
    zerocount = 0
    for pixel in layer:
        if layer[pixel] == 0:
            zerocount += 1
    zerocounts.append({"layernum":i,"zerocount":zerocount})
zerocounts.sort(key=lambda z:z["zerocount"])
fewestzeroeslayer = zerocounts[0]["layernum"]
#print(fewestzeroeslayer)
numones = 0
numtwos = 0
for pixel in layers[fewestzeroeslayer]:
    if layers[fewestzeroeslayer][pixel] == 1:
        numones += 1
    if layers[fewestzeroeslayer][pixel] == 2:
        numtwos += 1
print(numones*numtwos)

