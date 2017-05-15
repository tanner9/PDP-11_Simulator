class RegisterFile():
     
    def __init__(self,pc=0):
       
        self.registers = {'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'R7':pc}
       
    def readReg(self, register, mode):
        
        self.reg = 'R'+str(register)
        
        if(mode == 2):
            if((self.reg == 'R0') or (self.reg == 'R1') or (self.reg == 'R2') or (self.reg == 'R3') or (self.reg == 'R4') or (self.reg == 'R5')):
                self.data = self.registers[self.reg]
                self.registers[self.reg] = (self.registers[self.reg])+1
                print( "register contents:",self.registers[self.reg])
                print("data read:", self.data)
            else:
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read",self.data)
        elif(mode == 3):
            if((self.reg == 'R0') or (self.reg == 'R1') or (self.reg == 'R2') or (self.reg == 'R3') or (self.reg == 'R4') or (self.reg == 'R5')):
                self.data = self.registers[self.reg]
                self.registers[self.reg] = (self.registers[self.reg]) + 2
                print( "register contents:",self.registers[self.reg])
                print("data read",self.data)
            else:
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read", self.data)
        elif(mode == 4):
            if((self.reg == 'R0') or (self.reg == 'R1') or (self.reg == 'R2') or (self.reg == 'R3') or (self.reg == 'R4') or (self.reg == 'R5')):
                self.registers[self.reg] = (self.registers[self.reg]) - 1
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read", self.data)
            else:
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read",self.data)
        elif(mode == 5):
            if((self.reg == 'R0') or (self.reg == 'R1') or (self.reg == 'R2') or (self.reg == 'R3') or (self.reg == 'R4') or (self.reg == 'R5')):
                self.registers[self.reg] = (self.registers[self.reg]) - 2
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read:", self.data)
            else:
                self.data = self.registers[self.reg]
                print( "register contents:",self.registers[self.reg])
                print("data read", self.data)
        else:
            self.data = self.registers[self.reg]
            print( "register contents:",self.registers[self.reg])
            print("data read", self.data)
        

    def writeReg(self,data):
        self.registers[self.reg] = data
        self.d_oct = oct(int(self.registers[self.reg]))
        print(self.d_oct)
        print('the contents written into the register:',self.d_oct)
        
    def printReg(self,register):
        self.reg = 'R'+str(register)
        print ('the register contents are:',oct(int(self.registers[self.reg])))


x=RegisterFile()
x.readReg(0, 2)
x.writeReg(23)
x.printReg(2)
