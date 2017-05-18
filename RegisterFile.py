class RegisterFile():
     
    def __init__(self, debug, pc=0):
        self.registers = {'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'R7':pc}
        self.debug = debug

       
    def readReg(self, register, mode):
        
        reg = self.sanitizeInput(register)

        print("Before Read")
        self.printRegDec(reg)

        if(mode == 2):
            data = self.registers[reg]
            self.registers[reg] = data+1
        elif(mode == 3):
            data = self.registers[reg]
            self.registers[reg] = data + 2
        elif(mode == 4):
            self.registers[reg] = (self.registers[reg]) - 1
            data = self.registers[reg]
        elif(mode == 5):
            self.registers[reg] = (self.registers[reg]) - 2
            data = self.registers[reg]
        else:
            data = self.registers[reg]
        print("Read reg with mode %d" %(mode))
        self.printRegDec(reg)
        return data

    def writeReg(self,register, data):
        reg = self.sanitizeInput(register)
        self.registers[reg] = data
        print("write reg")
        self.printRegDec(reg)
        
    def printRegDec(self,register):
        reg = self.sanitizeInput(register)
        print("%s: %d" %(reg, self.registers[reg]))

    def printRegOct(self,register):
        reg = self.sanitizeInput(register)
        print( "%s: %s" %(reg, oct(int(self.registers[reg]))))

    def readPC(self):
        PC = self.registers['R7']
        self.registers['R7'] = PC+2
        print("Read and increment PC")
        self.printRegDec('R7')
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
