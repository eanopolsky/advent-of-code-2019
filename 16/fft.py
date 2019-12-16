#!/usr/bin/python3

with open("myinput.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]

#print(signal) #works

#rangelensignal = range(len(signal)) # this actually makes it run slower
for phase in range(100):
    #print("phase {}".format(phase+1))
    #print("input signal: {}".format(signal))
    nextsignal = []
    for i in range(len(signal)):
        # i   is the index in the signal array in this program
        # i+1 is the "position in the output list" in the language of
        #     the problem
        #print("i {}".format(i))
        positiveelements = [signal[j] for j in range(len(signal)) if (((j+1)//(i+1)) % 4) == 1]
        negativeelements = [signal[j] for j in range(len(signal)) if (((j+1)//(i+1)) % 4) == 3]
        #print("positiveelements: {}".format(positiveelements))
        #print("negativeelements: {}".format(negativeelements))
        esum = sum(positiveelements) - sum(negativeelements)
        esum = abs(esum) % 10
        #print("esum: {}".format(esum))
        nextsignal.append(esum)
    signal = nextsignal
    #print("new signal: {}".format(signal))
    #input()

print(signal[0:8])
