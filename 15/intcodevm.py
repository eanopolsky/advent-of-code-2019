#!/usr/bin/python3

from time import sleep
from queue import Queue
from itertools import permutations
import threading
import colorama

debug = False

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

class mvcontroller:
    mvcmds = [{"raw":1,"name":"north","shortcut":"n","dx":0,"dy":1},
             {"raw":2,"name":"south","shortcut":"s","dx":0,"dy":-1},
             {"raw":3,"name":"west","shortcut":"w","dx":-1,"dy":0},
             {"raw":4,"name":"east","shortcut":"e","dx":1,"dy":0}]
    scodes = [{"raw":0,"name":"wallhit","moveok":False},
              {"raw":1,"name":"floor","moveok":True},
              {"raw":2,"name":"oxygen","moveok":True}]
    def __init__(self,robotmemory):
        self.__myvm = intcodevm(memory=robotmemory,name="repairdroid")
        self.__myvm.setinputmode("queue") #.queueinput(val)
        self.__myvm.setoutputmode("queue") #.getoutput()
        self.__myvmthread = threading.Thread(group=None,target=self.__myvm.run)
        self.__myvmthread.start()
        self.__robot = {"x": 0, "y": 0}
        self.__areamap = [{"x":0,"y":0,"content":"."}]

    def __addtile(self, newtile):
        self.__areamap = [maptile for maptile in self.__areamap if
                          not (maptile["x"] == newtile["x"] and
                               maptile["y"] == newtile["y"])]
        self.__areamap.append(newtile)

    def render(self):
        minx = min([tile["x"] for tile in self.__areamap])
        maxx = max([tile["x"] for tile in self.__areamap])
        miny = min([tile["y"] for tile in self.__areamap])
        maxy = max([tile["y"] for tile in self.__areamap])
        for y in range(maxy,miny-1,-1):
            for x in range(minx,maxx+1):
                try:
                    tile = list(filter(lambda tile: tile["x"] == x and tile["y"] == y,self.__areamap))[0]
                    tilechar = tile["content"]
                except IndexError:
                    tilechar = " "
                #color
                if x == self.__robot["x"] and y == self.__robot["y"]:
                    print(colorama.Back.GREEN+tilechar+colorama.Style.RESET_ALL,end="")
                else:
                    print(tilechar,end="")
            print("")

    def processusercmd(self,cmd):
        try:
            mvcmd = [mvcmd for mvcmd in self.mvcmds if mvcmd["shortcut"] == cmd][0]
        except IndexError:
            print("invalid command shortcut")
            return
        self.__myvm.queueinput(mvcmd["raw"])
        rawstatus = self.__myvm.getoutput()
        status = [scode for scode in self.scodes if scode["raw"] == rawstatus][0]
        newx = self.__robot["x"] + mvcmd["dx"]
        newy = self.__robot["y"] + mvcmd["dy"]
        newmaptile = {"x": newx, "y": newy, "content": ""}
        if status["name"] == "wallhit":
            newmaptile["content"] = "#"
        elif status["name"] == "floor":
            newmaptile["content"] = "."
        elif status["name"] == "oxygen":
            newmaptile["content"] = "O"
        else:
            print("unsupported tile")
            exit(1)
        self.__addtile(newmaptile)
        if status["moveok"] == True:
            self.__robot["x"] = newx
            self.__robot["y"] = newy
        self.render()
        
if __name__ == "__main__":
    with open('program.txt') as f:
        memory = [int(x) for x in f.readline().split(",")]
    mymvcontroller = mvcontroller(memory)
    #mymvcontroller.render()
    while True:
        mymvcontroller.processusercmd(input())

