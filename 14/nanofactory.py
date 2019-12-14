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
        print(reaction)
        
