#!/usr/bin/python3

#TODO: implement iomanager and hypervisor

from time import sleep
from queue import Queue
from itertools import permutations
import threading

debug = False

class iomanager:
    def __init__(self):
        # Contains dictionaries representing VMs.
        # {"name": name of VM,
        #  "inputqueue": VM's input queue
        #  "outputqueue": VM's output queue}
        registeredVMs = []
        # Contains dictionaries representing io distributors.
        # Each distributor has one input and one or more outputs.
        # The input must be a VM's output queue. The outputs may
        # be either another VM's input queue or the special stdout
        # queue. Each time an object (normally an integer) appears
        # in an io distributor's input queue, a copy is put into
        # each output queue.
        # 
        iodistributors = []

class memorymanager:
    def __init__(self,initcontents):
        self.memdict = {}
        self.load(initcontents)
    def load(self,newmem):
        if type(newmem) != type(list()):
            print("memorymanager may only be initialized with a list")
            exit(1)
        for i in range(len(newmem)):
            self.memdict[i] = newmem[i]
    def __readsingle(self,i):
        try:
            return self.memdict[i]
        except KeyError:
            return 0
    def __getitem__(self,key):
        if type(key) == type(int()):
            return self.__readsingle(key)
        elif type(key) == type(slice(1)):
            if key.step != None:
                print("memory slicing with steps not supported")
                exit(1)
            return [self.__readsingle(i) for i in range(key.start,key.stop)]
        else:
            print("unsupported memory index type: {}".format(type(index)))
            exit(1)
    def __setitem__(self,key,value):
        self.memdict[key] = value

class intcodevm:
    #instructions
    decodemap = {1: {"name":"add","parameters":3},
                 2: {"name":"multiply","parameters":3},
                 3: {"name":"input","parameters":1},
                 4: {"name":"output","parameters":1},
                 5: {"name":"jump-if-true","parameters":2},
                 6: {"name":"jump-if-false","parameters":2},
                 7: {"name":"less than","parameters":3},
                 8: {"name":"equals","parameters":3},
                 9: {"name":"adj-relbase","parameters":1},
                 99: {"name":"halt","parameters":0}}

    #parameter modes for instructions
    pmodemap = {0: "position",
                1: "immediate",
                2: "relative"}

    def __init__(self, memory, name):
        self.name = name
        self.memory = memorymanager(memory)
        self.registers = {"ip": 0,
                          "relbase": 0 }
        self.running = False
        self.inputqueue = Queue()
        self.getinput = input
        self.outputqueue = Queue()
        self.output = print
        self.disassemble = False
        self.disassembled = []

    def setdisassemble(self,newval):
        self.disassemble = newval

    def showdisassembled(self):
        pass
        
    def setinputfunc(self,func):
        self.getinput = func
        
    def setinputmode(self,mode):
        if mode == "stdin":
            self.getinput = input
        elif mode == "queue":
            self.getinput = self.inputqueue.get
        else:
            print("unsupported input mode")
            exit(1)

    def queueinput(self,value):
        self.inputqueue.put(value)
            
    def setoutputfunc(self,func):
        self.output = func

    def setoutputmode(self,mode):
        if mode == "print":
            self.output = print
        elif mode == "queue":
            self.output = self.outputqueue.put

    def getoutput(self):
        return self.outputqueue.get()

    def __decode(self,ip):
        #low two digits are the instruction
        rawinstruction = self.memory[ip] % 100 
        if rawinstruction not in self.decodemap:
            print("invalid opcode {} at address {}".format(rawinstruction,ip))
            exit(1)
            
        instruction = {}
        instruction["name"] = self.decodemap[rawinstruction]["name"]
        instruction["parametercount"] = self.decodemap[rawinstruction]["parameters"]
        instruction["parameters"] = self.memory[ip+1:ip+1+instruction["parametercount"]]
        instruction["size"] = instruction["parametercount"]+1

        parametermodes = {}
        parameters = {}
        for i in range(instruction["parametercount"]):
            modebit = (self.memory[ip] // (10 ** (2+i))) % 10
            if modebit not in self.pmodemap:
                print("invalid parameter mode {} found in instruction {} at address {}".format(modebit,self.memory[ip],ip))
                exit(1)
            parametermodes[i] = self.pmodemap[modebit]
            # Fails because not all parameters are for reading.
            # Pointers must be dereferenced during execution.
            #if parametermodes[i] == "position":
            #    parameters[i] = self.memory[self.memory[ip+1+i]]
            #elif parametermodes[i] == "immediate":
            #    parameters[i] = self.memory[ip+1+i]
            #else:
            #    print("unsupported parameter mode")
            #    exit(1)
            parameters[i] =  self.memory[ip+1+i]
        instruction["parametermodes"] = parametermodes
        instruction["parameters"] = parameters
        if debug:
            print("Decoded {} to {}".format(self.memory[ip:ip+instruction["size"]],instruction))
        return instruction

    #fetches from a parameter, taking parameter modes into account
    def __fetchparam(self,deci,paramnum):
        if deci["parametermodes"][paramnum] == "immediate":
            return deci["parameters"][paramnum]
        elif deci["parametermodes"][paramnum] == "position":
            return self.memory[deci["parameters"][paramnum]]
        elif deci["parametermodes"][paramnum] == "relative":
            return self.memory[deci["parameters"][paramnum]+self.registers["relbase"]]
        else:
            print("fetch from unsupported parameter mode")
            exit(1)

    #stores to a parameter, taking parameter modes into account
    def __storeparam(self,deci,paramnum,value):
        if deci["parametermodes"][paramnum] == "immediate":
            print("invalid operation: cannot store to parameter in immediate mode")
            exit(1)
        elif deci["parametermodes"][paramnum] == "position":
            self.memory[deci["parameters"][paramnum]] = value
            return
        elif deci["parametermodes"][paramnum] == "relative":
            self.memory[deci["parameters"][paramnum]+self.registers["relbase"]] = value
            return
        else:
            print("store to unsupported parameter mode")
            exit(1)
    
    #executes a decoded instruction
    def __execute(self,deci):
        if self.disassemble:
            instruction = {"deci": deci, "ip": self.registers["ip"]}
            self.disassembled.append(instruction)
        if deci["name"] == "add":
            summand1 = self.__fetchparam(deci,0)
            summand2 = self.__fetchparam(deci,1)
            self.__storeparam(deci,2,summand1 + summand2)
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "multiply":
            multiplicand1 = self.__fetchparam(deci,0)
            multiplicand2 = self.__fetchparam(deci,1)
            self.__storeparam(deci,2,multiplicand1 * multiplicand2)
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "input":
            self.__storeparam(deci,0,int(self.getinput()))
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "output":
            self.output(self.__fetchparam(deci,0))
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "jump-if-true":
            testvalue = self.__fetchparam(deci,0)
            if testvalue != 0:
                self.registers["ip"] = self.__fetchparam(deci,1)
            else:
                self.registers["ip"] += deci["size"]
        elif deci["name"] == "jump-if-false":
            testvalue = self.__fetchparam(deci,0)
            if testvalue == 0:
                self.registers["ip"] = self.__fetchparam(deci,1)
            else:
                self.registers["ip"] += deci["size"]
        elif deci["name"] == "less than":
            if self.__fetchparam(deci,0) < self.__fetchparam(deci,1):
                self.__storeparam(deci,2,1)
            else:
                self.__storeparam(deci,2,0)
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "equals":
            if self.__fetchparam(deci,0) == self.__fetchparam(deci,1):
                self.__storeparam(deci,2,1)
            else:
                self.__storeparam(deci,2,0)
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "adj-relbase":
            self.registers["relbase"] += self.__fetchparam(deci,0)
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "halt":
            self.running = False
        else:
            print("execution of instruction '{}' not supported".format(deci["name"]))
            exit(1)
    
    def run(self):
        self.running = True
        while(self.running):
            deci = self.__decode(self.registers["ip"])
            self.__execute(deci)


class screen:
    tiletypes = [{"index": 0, "name": "empty", "render": " "},
                 {"index": 1, "name": "wall", "render": "#"},
                 {"index": 2, "name": "block", "render": "%"},
                 {"index": 3, "name": "hpaddle", "render": "-"},
                 {"index": 4, "name": "ball", "render": "@"}]
    emptytile = {"x": 0, "y": 0, "tiletype": {}}

    def __init__(self):
        self.__tilesonscreen = []
        self.__currenttile = self.emptytile.copy()
        self.__nextinput = "x"
        self.__segmentdisplay = 0

    def __addtile(self,newtile):
        self.__tilesonscreen = [ tile for tile in self.__tilesonscreen if
                                 not (tile["x"] == newtile["x"] and
                                      tile["y"] == newtile["y"]) ]
        # replacedtile = [tile for tile in self.__tilesonscreen if
        #                 tile["x"] == newtile["x"] and
        #                 tile["y"] == newtile["y"]]
        # if len(replacedtile) > 1:
        #     print("screen error")
        #     exit(1)
        # self.__tilesonscreen.remove(replacedtile)
        self.__tilesonscreen.append(newtile)

    def receivefromvm(self,i):
        if self.__nextinput == "x":
            self.__currenttile["x"] = i
            self.__nextinput = "y"
        elif self.__nextinput == "y":
            self.__currenttile["y"] = i
            self.__nextinput = "tile"
        elif self.__nextinput == "tile":
            #print("received tile at x={},y={}".format(self.__currenttile["x"], self.__currenttile["y"]))
            if self.__currenttile["x"] == -1 and self.__currenttile["y"] == 0:
                self.__segmentdisplay = i
                #self.render()
            else:
                self.__currenttile["tiletype"] = self.tiletypes[i]
                #self.__tilesonscreen.append(self.__currenttile)
                self.__addtile(self.__currenttile)
                #self.render()
            self.__currenttile = self.emptytile.copy()
            self.__nextinput = "x"
        else:
            print("error receiving tile from vm")
            exit(1)

    def render(self):
        minx = min([tile["x"] for tile in self.__tilesonscreen])
        maxx = max([tile["x"] for tile in self.__tilesonscreen])
        miny = min([tile["y"] for tile in self.__tilesonscreen])
        maxy = max([tile["y"] for tile in self.__tilesonscreen])
        if len(self.__tilesonscreen) < 20*44:
            print("incomplete screen")
            return
        print("Score: {}".format(self.__segmentdisplay))
        for y in range(miny,maxy+1):
            for x in range(minx,maxx+1):
                try:
                    tile = list(filter(lambda tile: tile["x"] == x and tile["y"] == y,self.__tilesonscreen))[0]
                    tilechar = tile["tiletype"]["render"]
                except IndexError:
                    tilechar = " "
                print(tilechar,end="")
            print("")
    def countblocks(self):
        return len(list(filter(lambda tile: tile["tiletype"]["name"] == "block",self.__tilesonscreen)))

    def getballx(self):
        for tile in self.__tilesonscreen:
            if tile["tiletype"]["name"] == "ball":
                return tile["x"]
    def getpaddlex(self):
        for tile in self.__tilesonscreen:
            if tile["tiletype"]["name"] == "hpaddle":
                return tile["x"]

def autojoystick():
    #myscreen.render()
    #sleep(1)
    if myscreen.getballx() == myscreen.getpaddlex():
        return 0
    else:
        return -1 if myscreen.getballx() < myscreen.getpaddlex() else 1

if __name__ == "__main__":
    with open('program.txt') as f:
        memory = [int(x) for x in f.readline().split(",")]
    #insert quarters:
    memory[0] = 2
    myvm = intcodevm(memory=memory,name="elfout")
    myscreen = screen()
    myvm.setoutputfunc(myscreen.receivefromvm)
    myvm.setinputfunc(autojoystick)
    myvm.setdisassemble(True)
    vmthread = threading.Thread(group=None, target=myvm.run)
    vmthread.start()
    vmthread.join()
    myscreen.render()
