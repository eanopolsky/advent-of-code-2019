#!/usr/bin/python3

import intcodevm

with open('myinput.txt') as f:
    memory = [int(x) for x in f.readline().split(",")]
memory[0] = 2 #part 2
myvm = intcodevm.intcodevm(memory = memory, name = "ascii")
myfb = intcodevm.asciifb()
#myvm.setoutputfunc(myfb.receiveint)
myvm.setinputmode("queue")
#myvm.queueinput(n)

mainpattern = "A,B,A,B,A,C,B,C,A,C\n"
pA = "L,10,L,12,R,6\n"
pB = "R,10,L,4,L,4,L,12\n"
pC = "L,10,R,10,R,6,L,4\n"
cvf = "n\n"
inputs = [mainpattern, pA, pB, pC, cvf]
for inp in inputs:
    for i in range(len(inp)):
        print("queueing input: {}".format(ord(inp[i])))
        myvm.queueinput(ord(inp[i]))
myvm.run()
myfb.render()
