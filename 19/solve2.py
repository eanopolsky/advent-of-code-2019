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

xstartleft, xstartright = findedgesbruteforce(ystart)
xendleft, xendright = findedgesbruteforce(yend)

rightslopeapprox = (yend-ystart) / (xendright-xstartright)

def findrightsidesmart(y):
    xguess = int(y / rightslopeapprox)
    if testspace(xguess,y) == 0: #outside of beam. xguess too high.
        while True:
            xguess -= 1
            if testspace(xguess,y) == 1:
                return xguess
    else: #inside beam. xguess exactly right or too low.
        while True:
            if testspace(xguess+1,y) == 0:
                return xguess
            xguess += 1

#print(findrightsidesmart(200000))
def will100x100fitat(y):
    xright = findrightsidesmart(y)
    xleft = xright - 99 #100 spaces inclusive
    if xleft < 0: #common sense check
        return False
    if testspace(xleft,y) == 0: #100 space line won't fit
        return False
    if testspace(xleft,y+99) == 1:
        return True #diagonal opposite corner will fit
    else:
        return False

ylow = 100
yhigh = 10000
while True:
    ymid = int((ylow + yhigh)/2)
    if will100x100fitat(ymid):
        yhigh = ymid
    else:
        ylow = ymid
    if yhigh - ylow == 1:
        #print(yhigh)
        break
answer = (findrightsidesmart(yhigh)-99)*10000 + yhigh
print(answer)
