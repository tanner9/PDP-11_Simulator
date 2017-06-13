# RegisterFile.py
# Authors: Yoshita Nandamuri and Tanner Shephard
# Description: Implements the register file as a hash. Allows access via read and 
#              write functions. Registers can be accessed with either R0 or 0 
#              formats. The input is checked and formatted before being used to 
#              access the hash


class RegisterFile():
     
    def __init__(self, debug, pc=0):
        self.registers = {'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'R7':pc}
        self.debug = debug

       
    def readReg(self, register, mode, isByte=0): # isByte is used for byte operations using auto increment or decrement. Optionally given
        
        reg = self.sanitizeInput(register)
        if(self.debug):
            print("Before Read")
            self.printRegOct(reg)

        if(mode == 2 and reg != "R7" and reg != "R6"):
            data = self.registers[reg]
            if(isByte):
                self.registers[reg] = data+1
            else:
                self.registers[reg] = data+2
        elif(mode == 3 or mode == 2):
            data = self.registers[reg]
            self.registers[reg] = data + 2
        elif(mode == 4 and reg != "R6"):
            if(isByte):
                self.registers[reg] = (self.registers[reg]) - 1
            else:
                self.registers[reg] = (self.registers[reg]) - 2
            data = self.registers[reg]
        elif(mode == 5 or mode == 4):
            self.registers[reg] = (self.registers[reg]) - 2
            data = self.registers[reg]
        else:
            data = self.registers[reg]
        if(self.debug):
            print("Read reg with mode %d" %(mode))
            self.printRegOct(reg)
        return data

    def writeReg(self,register, data, isByte = 0):
        reg = self.sanitizeInput(register)
        if(isByte):
            self.registers[reg] = (self.registers[reg] & 0xFF00)+data
        else:
            self.registers[reg] = data
        if(self.debug):
            print("write reg")
            self.printRegOct(reg)
        
    def printRegDec(self,register):
        reg = self.sanitizeInput(register)
        print("%s: %d" %(reg, self.registers[reg]))

    def printRegOct(self,register):
        reg = self.sanitizeInput(register)
        print( "%s: %s" %(reg, oct(int(self.registers[reg]))))

    def readPC(self):
        PC = self.registers['R7']
        self.registers['R7'] = PC+2
        if(self.debug):
            print("Read and increment PC")
            self.printRegOct('R7')
        return PC

    def printRegFile(self):
        print("-------")
        for i in range (0,8):
            print("|", end="")
            reg = self.sanitizeInput(i)
            print("%s: %d" %(reg, self.registers[reg]), end="")
            print("|\n-------")

    def sanitizeInput(self, input):
        if(str(input)[0] == 'R'):
            return input
        else:
            return 'R'+str(input)



def test():
    x=RegisterFile()
    x.writeReg(0, 23)
    x.readReg(0, 0)
    x.writeReg(4, 53)
    x.readReg(4, 2)
    x.writeReg(6, 17)
    x.readReg(6, 4)
