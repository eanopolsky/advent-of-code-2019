#!/usr/bin/python3

#inputfile = "sample1.txt"
inputfile = "myinput.txt"
decksize = 10007 #10007 is prime. 

instructions = []
with open(inputfile,"r") as f:
    for line in f:
        line = line.rstrip("\n")
        if line == "deal into new stack":
            #instructions.append(("reverse",0))
            instructions.append(("multiply",decksize-1))
            instructions.append(("subtract",1))
        elif line[0:4] == "cut ":
            instructions.append(("subtract",int(line[4:])))
        elif line[0:20] == "deal with increment ":
            instructions.append(("multiply",int(line[20:])))
        else:
            print("invalid line: {}".format(line))
            exit(1)

# for instruction in instructions:
#     print(instruction)
# exit(1)


position = 2019
for instruction in instructions:
    if instruction[0] == "reverse":
        position = (decksize - 1) - position
    elif instruction[0] == "subtract":
        position = position - instruction[1]
        position = position % decksize
    elif instruction[0] == "multiply":
        position = position * instruction[1]
        position = position % decksize
    else:
        print("invalid instruction: {}".format(instruction))

print(position)
