#!/usr/bin/python3

import threading
import intcodevm
from time import sleep

with open("myinput.txt","r") as f:
     memory = [int(x) for x in f.readline().split(",")]

exbotvm = intcodevm.intcodevm(memory=memory,name="explore-bot")
exbotvm.setinputmode("queue")
exbotvm.setoutputmode("null")
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

exbotthread = threading.Thread(group=None,target=exbotvm.run)
exbotthread.start()
while exbotvm.inputqueue.empty() == False:
     sleep(1)

#return manual control:
exbotvm.setoutputmode("printascii")
exbotvm.setinputmode("ascii")
exbotvm.queueinput(ord("\n")) #release exbot from blocking input queue read
