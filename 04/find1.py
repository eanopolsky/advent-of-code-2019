#!/usr/bin/python

import re

prog = re.compile(r'.*(.)\1')

def checkpossible(i):
    if prog.match(str(i)) == None:
        return False
    istr = str(i)
    if not (int(istr[0]) <= int(istr[1]) <= int(istr[2]) <= int(istr[3]) <= int(istr[4]) <= int(istr[5])):
        return False
    return True

count = 0
for i in range(245318, 765747+1):
    if checkpossible(i):
        count += 1
        #print(i)

print(count)
