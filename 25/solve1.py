#!/usr/bin/python3

import intcodevm

with open("myinput.txt","r") as f:
     memory = [int(x) for x in f.readline().split(",")]

exbotvm = intcodevm.intcodevm(memory=memory,name="explore-bot")
exbotvm.setinputmode("queue")
exbotvm.setoutputmode("printascii")
collectitemcmds = """east
take sand
west
south
take ornament
north
west
north
take wreath
east
take fixed point
west
north
north
take spool of cat6
south
south
south
south
south
take candy cane
north
east
east
east
take space law space brochure
south
take fuel cell
south
inv
"""
for char in collectitemcmds:
     exbotvm.queueinput(ord(char))

exbotvm.run()
#exbotvm.setinputmode("ascii")
