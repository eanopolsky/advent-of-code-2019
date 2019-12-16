#!/usr/bin/python3

basepattern = [0,1,0,-1]

with open("testsignal3.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]

offset = signal[0:7] #works
largesignal = []
for i in range(10000):
    largesignal.extend(signal)
signal = largesignal

# caching patterns for day 2 won't work because it would take
# too much memory (~len(largesignal) ** 2 bytes)
def getpatternforelement(bp,elementnum,signallength):
    singlepattern = []
    for val in bp:
        singlepattern.extend([val for i in range(elementnum)])
    newpattern = singlepattern[1:]
    while len(newpattern) < signallength:
        newpattern.extend(singlepattern)
    return newpattern[0:signallength]

#profiling results:
#100% of time in getnextsignal
#~67% of time in sum += signal[j]*pattern[j]
#~20% of time in for j in range(len(signal)):
#~12% of time in pattern = getpatternforelement(basepattern,i+1,len(signal))
def getnextsignal(signal):
    nextsignal = []
    for i in range(len(signal)):
        #print("i {}".format(i))
        pattern = getpatternforelement(basepattern,i+1,len(signal))
        #print("pattern: {}".format(pattern))
        sum = 0
        for j in range(len(signal)):
            #print("j {}".format(j))
            sum += signal[j]*pattern[j]
        sum = abs(sum) % 10
        nextsignal.append(sum)
    return nextsignal

for phase in range(100):
    #print("phase {}".format(phase+1))
    #print("input signal: {}".format(signal))
    signal = getnextsignal(signal)
    #print("new signal: {}".format(signal))
    #input()

print(signal[0:8])
