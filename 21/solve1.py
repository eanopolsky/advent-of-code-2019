#!/usr/bin/python3

import intcodevm

with open("myinput.txt") as f:
    memory = [int(x) for x in f.readline().split(",")]

springdroid = intcodevm.intcodevm(memory=memory,name="springdroid")

