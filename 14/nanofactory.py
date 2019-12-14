#!/usr/bin/python3

reactions = []
with open("input.txt") as f:
    for line in f:
        reaction = {"Rs": [], "P": {}}
        reagents, product = line.split("=>")
        reagents = reagents.strip().split(", ")
        product = product.strip()
        #print("'{}'".format(reagents))
        #print("'{}'".format(product))
        reaction["P"]["num"], reaction["P"]["chem"] = product.split(" ")
        for reagent in reagents:
            reagentdict = {}
            reagentdict["num"], reagentdict["chem"] = reagent.split(" ")
            reaction["Rs"].append(reagentdict)
        reactions.append(reaction)
        #print(reaction)

knownchems = [reaction["P"]["chem"] for reaction in reactions]
#print(knownchems)

oreused = 0
desiredchems = {}
for knownchem in knownchems:
    desiredchems[knownchem] = 0 if knownchem != "FUEL" else 1
#print(desiredchems)
storedchems = {}
for knownchem in knownchems:
    storedchems[knownchem] = 0
#print(storedchems)

