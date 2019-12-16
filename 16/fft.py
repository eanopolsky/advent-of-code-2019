#!/usr/bin/python3

with open("testsignal2.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]

#print(signal) #works

basepattern = [0,1,0,-1]

def getpatternforelement(bp,elementnum,signallength):
    print("creating pattern for element {}".format(elementnum))
    # singlepattern = []
    # for val in bp:
    #     singlepattern.extend([val for i in range(elementnum)])
    # newpattern = singlepattern[1:]
    # while len(newpattern) < signallength:
    #     newpattern.extend(singlepattern)
    # return newpattern[0:signallength]
    pattern = []
    for i in range(signallength):
        bpindex = ((i+1)//elementnum) % 4
        pattern.append(bp[bpindex])
        #print("bpindex: {}, bp[bpindex]: {}".format(bpindex,bp[bpindex]))
    #input()
    return pattern

#print(getpatternforelement(basepattern,3,8)) #works
for phase in range(100):
    #print("phase {}".format(phase+1))
    #print("input signal: {}".format(signal))
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
    signal = nextsignal
    #print("new signal: {}".format(signal))
    #input()

print(signal[0:8])
