class RegisterFile():
     
    def __init__(self,pc=0):
        global registers
        global reg
        global data
        global mode
        registers = {'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'R7':pc}
        r = input ('register number:' )
        reg = 'R'+str(r)
        print (reg)
        print (registers[reg])

    def readReg(self):
        r2 = input ('register number:' )
        reg = 'R'+str(r2)
        mode = int(input("addressing mode:"))
        if(mode == 2):
            if((reg == 'R0') or (reg == 'R1') or (reg == 'R2') or (reg == 'R3') or (reg == 'R4') or (reg == 'R5')):
                data = registers[reg]
                registers[reg] = (registers[reg])+1
                print( "register contents:",registers[reg])
                print("data read:", data)
            else:
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read",data)
        elif(mode == 3):
            if((reg == 'R0') or (reg == 'R1') or (reg == 'R2') or (reg == 'R3') or (reg == 'R4') or (reg == 'R5')):
                data = registers[reg]
                registers[reg] = registers[reg] + 2
                print( "register contents:",registers[reg])
                print("data read",data)
            else:
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read", data)
        elif(mode == 4):
            if((reg == 'R0') or (reg == 'R1') or (reg == 'R2') or (reg == 'R3') or (reg == 'R4') or (reg == 'R5')):
                registers[reg] = registers[reg] - 1
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read", data)
            else:
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read",data)
        elif(mode == 5):
            if((reg == 'R0') or (reg == 'R1') or (reg == 'R2') or (reg == 'R3') or (reg == 'R4') or (reg == 'R5')):
                registers[reg] = registers[reg] - 2
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read:", data)
            else:
                data = registers[reg]
                print( "register contents:",registers[reg])
                print("data read", data)
        else:
            data = registers[reg]
            print( "register contents:",registers[reg])
            print("data read", data)
        

    def writeReg(self):
        data = input ('the data input:')
        registers[reg] = data
        print(reg)
        print('the contents written into the register:',registers[reg])
        
    def printReg(self):
        r1 = input ('register number:' )
        reg = 'R'+str(r1)
        print ('the register contents are:',registers[reg])


x=RegisterFile()
x.readReg()
x.writeReg()
x.printReg()
