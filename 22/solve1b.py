#!/usr/bin/python3

#inputfile = "sample1.txt"
inputfile = "myinput.txt"
decksize = 10007 #10007 is prime. 
startposition = 2019

instructions = []
with open(inputfile,"r") as f:
    for line in f:
        line = line.rstrip("\n")
        if line == "deal into new stack":
            instructions.append(("multiply",-1))
            instructions.append(("add",-1))
        elif line[0:4] == "cut ":
            instructions.append(("add",-1*int(line[4:])))
        elif line[0:20] == "deal with increment ":
            instructions.append(("multiply",int(line[20:])))
        else:
            print("invalid line: {}".format(line))
            exit(1)

# for instruction in instructions:
#     print(instruction)
# exit(1)

endposition = startposition

def shuffle(startposition,instructions):
    pos = startposition
    for instruction in instructions:
        if instruction[0] == "add":
            pos += instruction[1]
        elif instruction[0] == "multiply":
            pos *= instruction[1]
        else:
            print("invalid instruction: {}".format(instruction))
        pos %= decksize
    return pos
    
print("card starting in position {} ended up in position {}".format(startposition,shuffle(startposition,instructions)))

