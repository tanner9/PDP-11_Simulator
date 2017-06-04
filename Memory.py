from decodeInstruction import *  # used for debug


class Memory(object):

    def __init__(self, debug):
        self.mem = bytearray(65536)
        self.debug = debug
        self.count = 0

    def readFileIntoMemory(self):
        decode = decodeStage()
        filename = "test.ascii"
        startAddressLine = ""
        pos = 0
        with open(filename) as fp:
            for line in fp:
                if(line[0] == '*'):
                    startAddressLine = line
                elif(line[0] == '@'):
                    pos = int(line[1:], 8)
                else:
                    tempLine = int(line[1:], 8)
                    self.mem[pos] = tempLine & 0xff
                    self.mem[pos + 1] = (tempLine >> 8) & 0xff
                    pos += 2
                    if(self.debug):
                        print(oct(pos - 2), ": ", line[1:])
                        decode.decodeInstruction(
                            tempLine).printInstructionData()
        if(startAddressLine == ""):
            self.startingAddress = int(input('Enter the starting address: ' ),8)
            if((self.startingAddress % 2)!=0):
                self.startingAddress = 0
            else:
                self.startingAddress = self.startingAddress
        else:
            self.startingAddress = startAddressLine

    def memoryWrite(self, address, memWriteData, typeOf):
        # lower 8 bits of 2 byte word
        self.mem[address] = int(memWriteData & 0x00ff)
        # higher 8 bits of 2 byte word
        self.mem[address + 1] = int((memWriteData >> 8) & 0x00ff)
        self.traceWrite(typeOf, address)
        if(self.debug):
            print("MemWrite to addr %s. Data = (%d)_10 = (%s)_8" %
                  (oct(address), memWriteData, oct(memWriteData)))

    def getStartingAddress(self):
        return self.startingAddress

    def memoryRead(self, address, typeOf):
        decode = decodeStage()
        if(self.debug):
            print("Attempting to read from address %d" % (address))
        LowerByte = self.mem[address]
        HigherByte = self.mem[address + 1]
        memReadData = int((HigherByte << 8) | LowerByte)
        self.traceWrite(typeOf, address)            
        instr = decode.decodeInstruction(memReadData)
        if(((instr.mnemonic != "ERROR") | (instr.mnemonic == "WAIT")) & (typeOf == 2)):
                    self.count += 1
                    if(inst.mnemonic == "HALT"):
                        print("Current Instructions Executed Count is %d" %(self.count))
        if(self.debug):
            print("MemRead from addr %s. Data = (%d)_10 = (%s)_8" %
                  (oct(address), memReadData, oct(memReadData)))
        return memReadData

    def traceWrite(self,typeOf,address):
            f       = open('ECE586_Trace','a')
            f.write('{} {:>18} \n'.format(typeOf, oct(address)))
            
    def traceFileOpen(self):                       
            x       = ' '
            f       = open('ECE586_Trace','w')
            text    = 'TYPE' +10*x + 'ADDRESS \n'
            f.write(text)

def test():
    a = 655
    b = 5623
    debug = True
    memInstance = Memory(debug)
    memInstance.readFileIntoMemory()
    memInstance.memoryWrite(a, b)
    memInstance.memoryRead(a)
    memInstance.traceWrite(4, 34)
