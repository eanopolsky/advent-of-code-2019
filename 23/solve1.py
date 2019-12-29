#!/usr/bin/python3

import intcodevm
import threading

with open("myinput.txt","r") as f:
     memory = [int(x) for x in f.readline().split(",")]

class vswitch:
    def __init__(self):
        self.routingtable = {} #{netaddress: packet_queue_function}
    def putpacket(self,packet):
        print("vswitch got packet: {}".format(packet))
        destaddress = packet[0]
        if destaddress == 255:
            print(packet[2])
            exit(0)
        else:
            self.routingtable[destaddress](packet[1:])
    def register(self,netaddress,packetqueue):
        self.routingtable[netaddress] = packetqueue

myswitch = vswitch()
vms = []
for i in range(50):
    newvm = intcodevm.intcodevm(memory=memory,
                                name="node{}".format(i),
                                netaddress=i)
    newvm.setinputmode("network")
    newvm.setoutputmode("network")
    myswitch.register(netaddress=i,packetqueue=newvm.nic.packetqueue.put)
    newvm.nic.sendpacket = myswitch.putpacket
    vms.append(newvm)

threads = []
for vm in vms:
    thread = threading.Thread(group=None,target=vm.run)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
