#!/usr/bin/python3

import intcodevm

with open('myinput.txt') as f:
    memory = [int(x) for x in f.readline().split(",")]
myvm = intcodevm.intcodevm(memory = memory, name = "ascii")
myfb = intcodevm.asciifb()
myvm.setoutputfunc(myfb.receiveint)
myvm.run()
myfb.render()

alignparams = []
for pixelcoords in myfb.screenmap:
    if myfb.screenmap[pixelcoords] != "#":
        #not an intersection
        continue
    neighbors = [(pixelcoords[0]-1,pixelcoords[1]),
                 (pixelcoords[0]+1,pixelcoords[1]),
                 (pixelcoords[0],pixelcoords[1]-1),
                 (pixelcoords[0],pixelcoords[1]+1)]
    try:
        nscaff = [n for n in neighbors if myfb.screenmap[n] == "#"]
        if len(nscaff) == 4:
            alignparam = pixelcoords[0]*pixelcoords[1]
            alignparams.append(alignparam)
        else:
            continue
    except KeyError:
        #this pixel is on the edge of the screen
        continue

print(sum(alignparams))
