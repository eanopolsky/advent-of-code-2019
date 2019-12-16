#!/usr/bin/python3

with open("signal.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]

#print(signal) #works

basepattern = [0,1,0,-1]

def getpatternforelement(bp,elementnum,signallength):
    singlepattern = []
    for val in bp:
        singlepattern.extend([val for i in range(elementnum)])
    newpattern = singlepattern[1:]
    while len(newpattern) < signallength:
        newpattern.extend(singlepattern)
    return newpattern[0:signallength]

print(getpatternforelement(basepattern,3,8))
