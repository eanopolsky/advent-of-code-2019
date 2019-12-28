#!/usr/bin/python3

import intcodevm

with open("myinput.txt") as f:
    memory = [int(x) for x in f.readline().split(",")]

springdroid = intcodevm.intcodevm(memory=memory,name="springdroid")
springdroid.setinputmode("queue")
springdroid.setoutputmode("printascii")
springscript = """NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""
for char in springscript:
    springdroid.queueinput(ord(char))
springdroid.run()
