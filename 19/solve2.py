#!/usr/bin/python3

import intcodevm
import asciifb

with open("myinput.txt") as f:
    memory = [int(x) for x in f.readline().split(",")]

# beamfb = asciifb.asciifb()

# for y in range(50):
#     for x in range(50):
#         beamscanner = intcodevm.intcodevm(memory=memory,name="beamscanner")
#         beamscanner.setinputmode("queue")
#         beamscanner.queueinput(x)
#         beamscanner.queueinput(y)
#         beamscanner.setoutputmode("queue")
#         beamscanner.run()
#         if beamscanner.getoutput() == 1:
#             beamfb.setpixel(x,y,"#")
#         else:
#             beamfb.setpixel(x,y,".")
# beamfb.render()

def testspace(x,y):
    beamscanner = intcodevm.intcodevm(memory=memory,name="beamscanner")
    beamscanner.setinputmode("queue")
    beamscanner.queueinput(x)
    beamscanner.queueinput(y)
    beamscanner.setoutputmode("queue")
    beamscanner.run()
    return beamscanner.getoutput()

# estimate slope of beam edges:
ystart = 200
yend = ystart * 2

def findedgesbruteforce(y):
    #find left side of beam at ystart by brute force
    x = 0
    xleft = 0
    while True:
        if testspace(x,y) == 1:
            xleft = x
            break
        x += 1

    #find right side of beam at ystart by brute force
    x = xleft
    xright = 0
    while True:
        if testspace(x,y) == 0:
            xright = x-1
            break
        x += 1
    return xleft, xright

print(findedgesbruteforce(ystart))

        