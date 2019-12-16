#!/usr/bin/python3

with open("signal.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]

#print(signal)

basepattern = [0,1,0,-1]

def getpatternforelement(bp,element):
    pass
