#!/usr/bin/python3

debug = True
if debug:
    inputfile = "sample1.txt"
else:
    inputfile = "myinput.txt"

from asciifb import asciifb

myfb = asciifb()
with open(inputfile,"r") as f:
    for line in f:
        for char in line:
            myfb.receivechar(char)

myfb.render()
