#!/usr/bin/python3

with open("myinput.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]
#print(signal) #works

#part 2:
part2 = False
if part2:
    messageoffset = signal[0:7]
    realsignal = []
    for i in range(10000):
        realsignal.extend(signal)
    signal = realsignal


#rangelensignal = range(len(signal)) # this actually makes it run slower
for phase in range(100):
    #print("phase {}".format(phase+1))
    #print("input signal: {}".format(signal))
    nextsignal = []
    for i in range(len(signal)):
        # i   is the index in the signal array in this program
        # i+1 is the "position in the output list" in the language of
        #     the problem
        #
        # build an nextsignal backwards
        #if i % 10000 == 0:
        #print("i: {}".format(i))
        if i == 0:
            #last element of the signal never changes
            nextsignal.append(signal[len(signal)-1]) 
        elif i < (len(signal)/2):
            #no need to account for negative numbers before % 10
            #because all summands are positive
            nextvalue = (nextsignal[i-1] + signal[len(signal)-1-i]) % 10
            nextsignal.append(nextvalue)
        else:
            i = len(signal)-1-i #try the old logic for now
            positiveelements = [signal[j] for j in range(len(signal)) if (((j+1)//(i+1)) % 4) == 1]
            negativeelements = [signal[j] for j in range(len(signal)) if (((j+1)//(i+1)) % 4) == 3]
            esum = sum(positiveelements) - sum(negativeelements)
            esum = abs(esum) % 10
            nextsignal.append(esum)
    nextsignal.reverse() #account for list built backwards
    signal = nextsignal
    #print("new signal: {}".format(signal))
    #input()

print(signal[0:8])
