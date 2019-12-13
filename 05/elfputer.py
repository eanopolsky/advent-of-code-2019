#!/usr/bin/python3

debug = False

class elfputer:
    #instructions
    decodemap = {1: {"name":"add","parameters":3},
                 2: {"name":"multiply","parameters":3},
                 3: {"name":"input","parameters":1},
                 4: {"name":"output","parameters":1},
                 5: {"name":"jump-if-true","parameters":2},
                 6: {"name":"jump-if-false","parameters":2},
                 7: {"name":"less than","parameters":3},
                 8: {"name":"equals","parameters":3},
                 99: {"name":"halt","parameters":0}}

    #parameter modes for instructions
    pmodemap = {0: "position",
                1: "immediate"}

    def __init__(self, memory):
        self.memory = memory
        self.registers = {"ip": 0}
        self.running = False

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
        #Doesn't make sense for this to be part of decode because it could be
        #affected during execution when jmp instructions are introduced.
        #instruction["nextip"] = ip + 1 + instruction["parametercount"]

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

    #dereferences a positional parameter if needed
    def __dereference(self,deci,paramnum):
        if deci["parametermodes"][paramnum] == "immediate":
            return deci["parameters"][paramnum]
        elif deci["parametermodes"][paramnum] == "position":
            return self.memory[deci["parameters"][paramnum]]
        else:
            print("unsupported parameter mode")
            exit(1)
    
    #executes a decoded instruction
    def __execute(self,deci):
        if deci["name"] == "add":
            summand1 = self.__dereference(deci,0)
            summand2 = self.__dereference(deci,1)
            self.memory[deci["parameters"][2]] = summand1 + summand2
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "multiply":
            multiplicand1 = self.__dereference(deci,0)
            multiplicand2 = self.__dereference(deci,1)
            self.memory[deci["parameters"][2]] = multiplicand1 * multiplicand2
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "input":
            self.memory[deci["parameters"][0]] = int(input("input: "))
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "output":
            print(str(self.__dereference(deci,0)))
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "jump-if-true":
            testvalue = self.__dereference(deci,0)
            if testvalue != 0:
                self.registers["ip"] = self.__dereference(deci,1)
            else:
                self.registers["ip"] += deci["size"]
        elif deci["name"] == "jump-if-false":
            testvalue = self.__dereference(deci,0)
            if testvalue == 0:
                self.registers["ip"] = self.__dereference(deci,1)
            else:
                self.registers["ip"] += deci["size"]
        elif deci["name"] == "less than":
            if self.__dereference(deci,0) < self.__dereference(deci,1):
                self.memory[deci["parameters"][2]] = 1
            else:
                self.memory[deci["parameters"][2]] = 0
            self.registers["ip"] += deci["size"]
        elif deci["name"] == "equals":
            if self.__dereference(deci,0) == self.__dereference(deci,1):
                self.memory[deci["parameters"][2]] = 1
            else:
                self.memory[deci["parameters"][2]] = 0
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
        
if __name__ == "__main__":
    memory = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,46,47,225,2,122,130,224,101,-1998,224,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1102,61,51,225,102,32,92,224,101,-800,224,224,4,224,1002,223,8,223,1001,224,1,224,1,223,224,223,1101,61,64,225,1001,118,25,224,101,-106,224,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,1102,33,25,225,1102,73,67,224,101,-4891,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,14,81,225,1102,17,74,225,1102,52,67,225,1101,94,27,225,101,71,39,224,101,-132,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,14,38,224,101,-1786,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1,65,126,224,1001,224,-128,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1101,81,40,224,1001,224,-121,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,7,226,226,224,102,2,223,223,1005,224,539,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,107,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,599,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,614,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
    e = elfputer(memory)
    e.run()
