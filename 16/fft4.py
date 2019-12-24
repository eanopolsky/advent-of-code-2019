#!/usr/bin/python3

with open("testsignal3.txt","r") as f:
    signal = [int(char) for char in f.readline().rstrip()]
#print(signal) #works

#part 2:
part2 = True
#messageoffset = signal[0:7]
messageoffset = signal[0]*1000000+signal[1]*100000+signal[2]*10000+signal[3]*1000+signal[4]*100+signal[5]*10+signal[6]
if part2:
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
        #when i == 0:
        #positive slices are 0:1, 4:5, 8:9, ...
        #negative slices are 2:3, 6:7, 10:11, ...
        #when i == 1:
        #positive slices are 1:3, 9:11, 17:19, ...
        #negative slices are 5:7, 13:15, 21:23, ...
        #when i == 2:
        #positive slices are 2:5, 14:17, 26:29, ...
        #negative slices are 8:11, 20:23, 32:35, ...
        #
        #regardless of i:
        #positive slices are 0(i+1)+i:2*i+1, 4(i+1)+i:4(i+1)+2*i+1, 8(i+1)+i:8(i+1)+2*i+1,... #ok
        #negative slices are 2(i+1)+0(i+1)+i:2(i+1)+2*i+1, 2*(i+1)+4(i+1)+i:2(i+1)+4(i+1)+2*i+1
        #positive slices start at n(i+1)+i where n is in 0,4,8,...
        #positive slices have a run length of i
        #negative slices start at 2(i+1)+n(i+1)+i where n in 0,4,8,...
        #negative slices have a run length of i
        if i % 10000 == 0:
            print(i)
        n = 0
        positivesum = 0
        while True:
            start = n*(i+1)+i
            if start > len(signal):
                break
            positivesum += sum(signal[start:start+i+1])
            n += 4
        n=0
        negativesum = 0
        while True: 
            start = 2*(i+1)+n*(i+1)+i
            if start > len(signal):
                break
            negativesum += sum(signal[start:start+i+1])
            n += 4
        finalvalue = abs(positivesum - negativesum) % 10
        nextsignal.append(finalvalue)

    #print("phase: {}".format(phase))
    #print("signal at beginning: {}".format(signal))
    #print("signal at end: {}".format(nextsignal))
    #input()
    signal = nextsignal

print(signal[messageoffset:messageoffset+8])
