#!/usr/bin/python3

from math import ceil

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
        reaction["P"]["num"] = int(reaction["P"]["num"])
        for reagent in reagents:
            reagentdict = {}
            reagentdict["num"], reagentdict["chem"] = reagent.split(" ")
            reagentdict["num"] = int(reagentdict["num"])
            reaction["Rs"].append(reagentdict)
        reactions.append(reaction)
        #print(reaction)

knownchems = [reaction["P"]["chem"] for reaction in reactions]
#print(knownchems)

needed = {}
for knownchem in knownchems:
    needed[knownchem] = 0 if knownchem != "FUEL" else 1
needed["ORE"] = 0
#print(needed)
storage = {}
for knownchem in knownchems:
    storage[knownchem] = 0
#print(storage)


def hashablestorage(storage):
    return tuple(sorted([key+str(storage[key]) for key in storage]))

storagestates = set()
storagestates.add(hashablestorage(storage))
fuelsynthesized = 0
while True:
    for target in needed:
        if target == "ORE":
            continue
        if needed[target] == 0:
            continue
        if needed[target] <= storage[target]:
            storage[target] -= needed[target]
            needed[target] = 0
            continue
        else:
            needed[target] -= storage[target]
            storage[target] = 0
        reaction = [reaction for reaction in reactions if reaction["P"]["chem"] == target][0] #only works when each chem is produced by a single recipe. Might change in part 2?
        #print(reaction)
        nreactions = ceil(needed[target] / reaction["P"]["num"])
        for reagent in reaction["Rs"]:
            needed[reagent["chem"]] += nreactions * reagent["num"]
        excessproduct = nreactions * reaction["P"]["num"] - needed[target]
        storage[target] += excessproduct
        needed[target] = 0
    #print(storage)
    #print(needed)
    if sum([needed[chem] for chem in needed if chem != "ORE"]) == 0:
        fuelsynthesized += 1
        if hashablestorage(storage) in storagestates:
            #finite state loop found
            break
        else:
            storagestates.add(hashablestorage(storage))
            needed["FUEL"] += 1

print(fuelsynthesized)
print(needed["ORE"])
