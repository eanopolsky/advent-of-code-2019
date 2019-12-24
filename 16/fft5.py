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
lensignal = len(signal)

#rangelensignal = range(len(signal)) # this actually makes it run slower
for phase in range(100):
#for phase in range(1):
    print("computing phase {}".format(phase+1))
    #print("input signal: {}".format(signal))
    sum2end = signal.copy()
    for i in range(len(signal)-1,0,-1):
        sum2end[i-1] += sum2end[i]
    nextsignal = []
    for i in range(len(signal)):
        #regardless of i:
        #positive slices are 0(i+1)+i:2*i+1, 4(i+1)+i:4(i+1)+2*i+1, 8(i+1)+i:8(i+1)+2*i+1,... #ok
        #negative slices are 2(i+1)+0(i+1)+i:2(i+1)+2*i+1, 2*(i+1)+4(i+1)+i:2(i+1)+4(i+1)+2*i+1
        #positive slices start at n(i+1)+i where n is in 0,4,8,...
        #positive slices have a run length of i
        #negative slices start at 2(i+1)+n(i+1)+i where n in 0,4,8,...
        #negative slices have a run length of i
        #if i % 10000 == 0:
        #    print(i)
        # if i == 0: #doesn't help much
        #     positivesum = sum(signal[0::4])
        #     negativesum = sum(signal[2::4])
        #     nextsignal.append(abs(positivesum - negativesum) % 10)
        #     continue
        n = 0
        positivesum = 0
        while True:
            start = n*(i+1)+i #7%
            if start >= lensignal:
                break
            #positivesum += sum(signal[start:start+i+1])
            oneafterend = start + i + 1 #5%
            if oneafterend <= (lensignal-1):
                positivesum += (sum2end[start] - sum2end[oneafterend]) #16%
            else:
                positivesum += sum2end[start]
            n += 4
        n=0
        negativesum = 0
        while True: 
            #start = 2*(i+1)+n*(i+1)+i
            start = (2+n)*(i+1)+i
            if start >= lensignal:
                break
            #negativesum += sum(signal[start:start+i+1])
            oneafterend = start + i + 1 #4%
            if oneafterend <= (lensignal-1):
                negativesum += (sum2end[start] - sum2end[start+i+1]) #19%
            else:
                negativesum += sum2end[start]
            n += 4
        finalvalue = abs(positivesum - negativesum) % 10
        nextsignal.append(finalvalue)

    #print("phase: {}".format(phase))
    #print("signal at beginning: {}".format(signal))
    #print("signal at end: {}".format(nextsignal))
    #input()
    signal = nextsignal

print(signal[messageoffset:messageoffset+8])
