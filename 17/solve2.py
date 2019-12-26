#!/usr/bin/python3

import intcodevm

with open('myinput.txt') as f:
    memory = [int(x) for x in f.readline().split(",")]
myvm = intcodevm.intcodevm(memory = memory, name = "ascii")
myfb = intcodevm.asciifb()
myvm.setoutputfunc(myfb.receiveint)
myvm.run()
myfb.render()

for pc in myfb.screenmap:
    ch = myfb.screenmap[pc]
    if ch in ["^","v","<",">"]:
        rloc = pc
        rdir = ch
        break

movelist = []
while True:
    fspace = (0,0)
    fchar = ""
    lspace = (0,0)
    lchar = ""
    rspace = (0,0)
    rchar = ""
    if rdir == "^":
        fspace = (rloc[0],rloc[1]-1)
        lspace = (rloc[0]-1,rloc[1])
        rspace = (rloc[0]+1,rloc[1])
    elif rdir == "<":
        fspace = (rloc[0]-1,rloc[1])
        lspace = (rloc[0],rloc[1]+1)
        rspace = (rloc[0],rloc[1]-1)
    elif rdir == ">":
        fspace = (rloc[0]+1,rloc[1])
        lspace = (rloc[0],rloc[1]-1)
        rspace = (rloc[0],rloc[1]+1)
    elif rdir == "v":
        fspace = (rloc[0],rloc[1]+1)
        lspace = (rloc[0]+1,rloc[1])
        rspace = (rloc[0]-1,rloc[1])
    else:
        print("invalid robot direction")
        exit(1)
    try:
        fchar = myfb.screenmap[fspace]
    except KeyError:
        fchar = "."
    try:
        lchar = myfb.screenmap[lspace]
    except KeyError:
        lchar = "."
    try:
        rchar = myfb.screenmap[rspace]
    except KeyError:
        rchar = "."
    if fchar == "#":
        nextmove = 1
    elif lchar == "#":
        nextmove = "L"
    elif rchar == "#":
        nextmove = "R"
    else:
        #robot has nowhere to go but back
        break
    movelist.append(nextmove)
    if nextmove == "R":
        if rdir == "^":
            rdir = ">"
        elif rdir == ">":
            rdir = "v"
        elif rdir == "v":
            rdir = "<"
        elif rdir == "<":
            rdir = "^"
        else:
            print("invalid robot direction")
            exit(1)
    if nextmove == "L":
        if rdir == "^":
            rdir = "<"
        elif rdir == "<":
            rdir = "v"
        elif rdir == "v":
            rdir = ">"
        elif rdir == ">":
            rdir = "^"
        else:
            print("invalid robot direction")
            exit(1)
    if nextmove == 1:
        if rdir == "^":
            rloc = (rloc[0],rloc[1]-1)
        elif rdir == ">":
            rloc = (rloc[0]+1,rloc[1])
        elif rdir == "v":
            rloc = (rloc[0],rloc[1]+1)
        elif rdir == "<":
            rloc = (rloc[0]-1,rloc[1])
        else:
            print("invalid robot direction")
            exit(1)

i = 0
while True:
    try:
        if type(movelist[i]) == type(movelist[i+1]) == type(int()):
            movelist[i] += movelist[i+1]
            del movelist[i+1]
            continue
    except IndexError:
        break
    i += 1
print(movelist)
