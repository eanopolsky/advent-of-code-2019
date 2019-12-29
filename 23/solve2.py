#!/usr/bin/python3

import intcodevm
import threading
from time import sleep

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

class natdevice:
     def __init__(self,myswitch):
          self.storedpacket = []
          self.lastpacket = []
          self.vswitchputpacket = myswitch.putpacket
          self.vms = []
     def receivepacket(self,packet):
          self.storedpacket = packet
     def maybedeliverpacket(self):
          hungryvms = [vm for vm in vms if vm.nic.packetqueue.empty()] #might not work because a vm with an empty queue might not be trying to read from it.
          if len(hungryvms) == len(vms) and len(self.storedpacket) == 2:
               self.vswitchputpacket([0].extend(self.storedpacket))
               try:
                    if self.storedpacket[1] == self.lastpacket[1]:
                         print("y value delivered twice: {}".format(self.storedpacket[1]))
                         exit(0)
               except IndexError:
                    pass #maybe no lastpacket yet
               self.lastpacket = self.storedpacket
     def deliverythread(self):
          while True:
               sleep(1)
               self.maybedeliverpacket()
               


myswitch = vswitch()
mynatdevice = natdevice(vswitch)
vms = []
mynatdevice.vms = vms
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

thread = threading.Thread(group=None,target=mynatdevice.deliverythread)
threads.append(thread)
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
