#!/usr/bin/python3

import intcodevm

with open("myinput.txt") as f:
    memory = [int(x) for x in f.readline().split(",")]

springdroid = intcodevm.intcodevm(memory=memory,name="springdroid")
springdroid.setinputmode("queue")
springdroid.setoutputmode("printascii")
springscript = [ "NOT A T",
                 "OR T J",
                 "NOT B T",
                 "OR T J",
                 "NOT C T",
                 "OR T J",
                 "AND D J", #set J if there are gaps coming and D is hull
                 "NOT E T",
                 "NOT T T", #set T to E (space after landing)
                 "OR H T",  #T = droid can advance to E or jump to H
                 "AND T J",
                 "RUN"]
for line in springscript:
    for char in line:
        springdroid.queueinput(ord(char))
    springdroid.queueinput(ord("\n"))
springdroid.run()
