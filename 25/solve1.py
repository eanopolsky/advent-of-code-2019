#!/usr/bin/python3

import threading
import intcodevm
from time import sleep
from queue import Queue

with open("myinput.txt","r") as f:
     memory = [int(x) for x in f.readline().split(",")]


class chatbot:
     def __init__(self):
          self.receivedline = ""
          self.receivedlines = []
          self.intqueue = Queue()
          self.readyfornextcommand = False
          self.silencevm = False
     def receiveint(self, i):
          self.receivedline += chr(i)
          if chr(i) == "\n":
               self.receivedlines.append(self.receivedline)
               tmpline = self.receivedline
               self.receivedline = ""
               #allows chatbot to continue receiving characters
               #while responding to the last line
               self.gotline(tmpline)
     def gotline(self,newline): #hook for when we get a line from the vm
          if not self.silencevm:
               print(newline,end="")
          if newline == "Command?\n":
               self.readyfornextcommand = True
     def execcommand(self,command, silent = False):
          self.silencevm = silent
          if command[-1:] != "\n":
               command += "\n" #for convenience
          while self.readyfornextcommand == False:
               sleep(0.1) #could use tuning.
               #sleeping too long extends runtime.
               #sleeping too short steals cycles from the vm.
          self.readyfornextcommand = False
          for char in command:
               self.intqueue.put(ord(char))
          while self.readyfornextcommand == False:
               sleep(0.1) #don't return until command is processed

#create components and hook them up
exbotvm = intcodevm.intcodevm(memory=memory,name="explore-bot")
mychatbot = chatbot()
exbotvm.setinputfunc(mychatbot.intqueue.get)
exbotvm.setoutputfunc(mychatbot.receiveint)

exbotthread = threading.Thread(group=None,target=exbotvm.run)
exbotthread.start()

collectitemcmds = ["east","take sand",
                   "west", "south","take ornament",
                   "north", "west", "north", "take wreath",
                   "east", "take fixed point",
                   "west", "north", "north", "take spool of cat6",
                   "south", "south", "south", "south", "south",
                   "take candy cane",
                   "north", "east", "east", "east",
                   "take space law space brochure",
                   "south", "take fuel cell",
                   "south"]

for cmd in collectitemcmds:
     mychatbot.execcommand(cmd,silent=True)
print("exbot is at security checkpoint with all items")

items = ["space law space brochure",
         "fixed point",
         "candy cane",
         "sand",
         "ornament",
         "fuel cell",
         "spool of cat6",
         "wreath"]

dropallitemscmds = []
for item in items:
     dropallitemscmds.append("drop " + item)


from itertools import chain, combinations
def powerset(iterable):
     s = list(iterable)
     return chain.from_iterable(combinations(s,r) for r in range(len(s)+1))

for itemset in powerset(items):
     print("Trying to pass with {}.".format(itemset))
     for cmd in dropallitemscmds:
          mychatbot.execcommand(cmd,silent=True)
     for item in itemset:
          mychatbot.execcommand("take " + item,silent=True)
     mychatbot.execcommand("west")
     input("press enter to continue")
#print(len(list(powerset(items))) #prints 256: correct for 8 items

# def gomanual():
#      #return manual control:
#      exbotvm.setoutputmode("printascii")
#      exbotvm.setinputmode("ascii")
#      exbotvm.queueinput(ord("\n")) #release exbot from blocking input queue read
