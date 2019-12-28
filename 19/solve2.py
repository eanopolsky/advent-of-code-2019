#!/usr/bin/python3

import intcodevm
import asciifb

with open("myinput.txt") as f:
    memory = [int(x) for x in f.readline().split(",")]

beamfb = asciifb.asciifb()

affectedpoints = 0
for y in range(50):
    for x in range(50):
        beamscanner = intcodevm.intcodevm(memory=memory,name="beamscanner")
        beamscanner.setinputmode("queue")
        beamscanner.queueinput(x)
        beamscanner.queueinput(y)
        beamscanner.setoutputmode("queue")
        beamscanner.run()
        if beamscanner.getoutput() == 1:
            beamfb.setpixel(x,y,"#")
        else:
            beamfb.setpixel(x,y,".")
beamfb.render()
