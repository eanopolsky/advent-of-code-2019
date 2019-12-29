#!/usr/bin/python3

import intcodevm

with open("myinput.txt","r") as f:
     memory = [int(x) for x in f.readline().split(",")]

exbotvm = intcodevm.intcodevm(memory=memory,name="explore-bot")
exbotvm.setinputmode("ascii")
exbotvm.setoutputmode("printascii")
exbotvm.run()
