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

print("exbot is at security checkpoint with all items")

items = ["space law space brochure",
         "fixed point",
         "candy cane",
         "sand",
         "ornament",
         "fuel cell",
         "spool of cat6",
         "wreath"]

dropallitemscmds = ""
for item in items:
     dropallitemscmds += ("drop " + item + "\n")

from itertools import chain, combinations
def powerset(iterable):
     s = list(iterable)
     return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))

#print(len(list(powerset(items))) #prints 256: correct for 8 items

def gomanual():
     #return manual control:
     exbotvm.setoutputmode("printascii")
     exbotvm.setinputmode("ascii")
     exbotvm.queueinput(ord("\n")) #release exbot from blocking input queue read

exbotvm.setoutputmode("printascii")
# for char in "inv\n":
#      exbotvm.queueinput(ord(char))
# exit(1)

for itemset in powerset(items):
     #print(itemset)
     #exbotvm.setoutputmode("null")
     for char in dropallitemscmds:
          exbotvm.queueinput(ord(char))
     for item in itemset:
          takecmd = ("take " + item + "\n")
          for char in takecmd:
               exbotvm.queueinput(ord(char))
     exbotvm.setoutputmode("queue")
     for char in "west\n":
          exbotvm.queueinput(ord(char))
     while exbotvm.blockingoninputqueue == False:
          pass #wait for vm to process commands
     while True:
          print(chr(exbotvm.getoutput()),end="")
     break

gomanual()
