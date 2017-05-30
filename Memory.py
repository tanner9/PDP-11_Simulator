from decodeInstruction import * # used for debug

#FIXME think about adding simpler print functions like printWord(address) and printByte(address). Someone may want a simple statement 
#instead of all of the print statements currently in memoryRead. 

class Memory(object):
    
        def __init__(self, debug):
            self.mem = bytearray(65536)
            self.debug = debug
            x       = ' '
            f       = open('ECE586_Trace','w')
            text    = 'TYPE' +10*x + 'ADDRESS \n'
            f.write(text)
        
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
                        pos 	    	= int(line[1:], 8)
                    else:
                        tempLine 		= int(line[1:], 8)
                        self.mem[pos] 	= tempLine&0xff
                        self.mem[pos+1]	= (tempLine>>8)&0xff
                        pos        += 2
                        if(self.debug == True):
                            print(pos-2, ": ", line[1:])
                            decode.decodeInstruction(tempLine).printInstructionData()   
            if(startAddressLine == ""):
                self.startingAddress = input('Enter the starting address: ')
            else:
                self.startingAddress = startAddressLine 

 
        #FIXME Don't shift incoming address. Assume incoming address is 16 bits already. If some is using a word address it can be shifted before the call to memory.
        #FIXME Combine print statements. Something like "writing word x into mem[y]" and "Writing byte x into mem[y]"
        #FIXME Dont write octal and decimal in the print statements, they take up a lot of room. Python prints octal as 0oX and decimal as X so they can be distinguished easily. 
        def memoryWrite(self, address, memWriteData):
            self.mem[address]   = int(memWriteData & 0x00ff)    #lower 8 bits of 2 byte word
            self.mem[address+1]	= int((memWriteData >> 8) & 0x00ff)      #higher 8 bits of 2 byte word
            self.traceWrite(1, address)
            if(self.debug == True):
                print("MemWrite to addr %s. Data = (%d)_10 = (%s)_8" %(address, memWriteData, oct(memWriteData)))

        def getStartingAddress(self):
            return self.startingAddress

        def memoryRead(self, address, typeOf):
            if(self.debug):
                print("Attempting to read from address %d" %(address))
            LowerByte	 	= self.mem[address]
            HigherByte	    = self.mem[address+1]
            memReadData     = int((HigherByte << 8)|LowerByte) 
            self.traceWrite(typeOf, address)
            if(self.debug == True):
                print("MemRead from addr %s. Data = (%d)_10 = (%s)_8" %(address, memReadData, oct(memReadData)))
            return memReadData
        
        def traceWrite(self,typeOf,address):
            f       = open('ECE586_Trace','a')
            f.write('{} {:>18} \n'.format(typeOf, oct(address)))

def test():
    a = 655
    b = 5623
    debug = True
    memInstance = Memory(debug) 
    memInstance.readFileIntoMemory()
    memInstance.memoryWrite(a, b)
    memInstance.memoryRead(a)
    memInstance.traceWrite(4,34)

                    

