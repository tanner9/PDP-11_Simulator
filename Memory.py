
#FIXME think about adding simpler print functions like printWord(address) and printByte(address). Someone may want a simple statement 
#instead of all of the print statements currently in memoryRead. 

class Memory(object):
    
        mem = bytearray(65536)
        
        #FIXME Use a more descriptive function name like readFileIntoMemory
        def readFileIntoMemory(self, debug):
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
                        if(debug == True):
                            print(tempLine)       
            if(startAddressLine == ""):
                startingAddress = input('Enter the starting address: ')
            else:
                startingAddress = startAddressLine # FIXME This will always take the last line read as the starting address the way you have coded it. Instead use the startingAddressLine stored above. 
                            
        #FIXME order of bytes written is correct but comments are backwards. Data & 0xFF is lower byte, Data >> 8 is upper byte. 
        #FIXME Don't shift incoming address. Assume incoming address is 16 bits already. If some is using a word address it can be shifted before the call to memory.
        #FIXME Combine print statements. Something like "writing word x into mem[y]" and "Writing byte x into mem[y]"
        #FIXME Dont write octal and decimal in the print statements, they take up a lot of room. Python prints octal as 0oX and decimal as X so they can be distinguished easily. 
        def memoryWrite(self, memAddress, memWriteData, debug):
            if(debug == True):
                print('Memory Address referred \n', oct(memAddress))
                print('Word to be written into Memory \n', oct(memWriteData))
            address             = memAddress << 1               #calculate byte address
            self.mem[address]   = int(memWriteData & 0x00ff)    #lower 8 bits of 2 byte word
            self.mem[address+1]	= int((memWriteData >> 8) & 0x00ff)      #higher 8 bits of 2 byte word
            if(debug == True):
                print('First Byte Writen into Memory in Octal \n',oct(self.mem[address]))
                print('Second Byte Writen into Memory in Octal \n',oct(self.mem[address+1]))            
                print('First Byte Writen into Memory(Decimal) \n',self.mem[address])
                print('Second Byte Writen into Memory(Decimal) \n',self.mem[address+1])
                print('Address of First Byte Written in Octal \n',oct(address))
                print('Address of Second Byte Written in Octal \n',oct(address+1))

        def memoryRead(self, memAddress, debug):
            if(debug == True):
                print('Memory Address referred \n', oct(memAddress))
            address             = memAddress << 1
            LowerByte	 	= self.mem[address]
            HigherByte	        = self.mem[address+1]
            if(debug == True):
                print('First Byte Read \n',oct(self.mem[address]))
                print('Second Byte Read \n',oct(self.mem[address+1]))
                print('First Byte Read From Memory(Decimal) \n',self.mem[address])
                print('Second Byte Read From Memory(Decimal) \n',self.mem[address+1])
                print('Address of First Byte Read \n',oct(address))
                print('Address of Second Byte Read \n',oct(address+1))
            memReadData         = int((HigherByte << 8)|LowerByte) 
            if(debug == True):
                print('The data read is \n', oct(memReadData))
            return memReadData

        '''def memoryAccessPrint(self, memAddress):
            m 				= memoryview(bytes(memAddress))   #print word address
            mylist			= m.tolist()
            print (','.join(mylist))'''

#def main():
a = 655
b = 5623
debug = True
memInstance = Memory()
memInstance.readFileIntoMemory(debug)
memInstance.memoryWrite(a, b, debug)
memInstance.memoryRead(a, debug)
#main()
                            
                            
	
	

