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

def compact(instructions):
    multiplier = 1
    offset = 0
    for instruction in instructions:
        if instruction[0] == "add":
            offset += instruction[1]
            offset %= decksize
        elif instruction[0] == "multiply":
            multiplier *= instruction[1]
            multiplier %= decksize
            offset *= instruction[1]
            offset %=  decksize
        else:
            print("invalid instruction: {}".format(instruction))
    newinstructions = []
    newinstructions.append(("multiply",multiplier))
    newinstructions.append(("add",offset))
    return newinstructions

#from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def revinstructions(instructions):
    newinstructions = instructions.copy()
    newinstructions.reverse()
    revinstructions = []
    for instruction in newinstructions:
        if instruction[0] == "add":
            offset = (instruction[1] * -1) % decksize
            revinstructions.append(("add",offset))
        elif instruction[0] == "multiply":
            multiplier = modinv(instruction[1] % decksize ,decksize)
            revinstructions.append(("multiply",multiplier))
        else:
            print("invalid instruction: {}".format(instruction))
            exit(1)
    return revinstructions
            
instructions = compact(instructions)
undo = compact(revinstructions(instructions)) # compact not needed, but fun

print("card starting in position {} ended up in position {}".format(startposition,shuffle(startposition,instructions)))
print("card ending up in position {} started in position {}".format(shuffle(startposition,instructions),shuffle(shuffle(startposition,instructions),undo)))

