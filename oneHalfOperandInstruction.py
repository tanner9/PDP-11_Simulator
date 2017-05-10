class oneHalfOperandInstruction:

    def __init__(self, instructionValue):
        self.value = instructionValue
        self.reg = (instructionValue>>6)&0x7
        self.opCode = (instructionValue>>9)&0x7f
        self.addr = instructionValue&0x7
        self.addrMode = (instructionValue>>3)&0x7

        if(self.opCode == 0o070):
            self.mnemonic = "MUL"
        elif(self.opCode == 0o071):
            self.mnemonic = "DIV"
        elif(self.opCode == 0o072):
            self.mnemonic = "ASH"
        elif(self.opCode == 0o073):
            self.mnemonic = "ASHC"
        elif(self.opCode == 0o074):
            self.mnemonic = "XOR"  
        else:
            self.mnemonic = "ERROR"

    def printValue(self):
        print("Instruction in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Instruction in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def printInstruction(self):
        print("%s %d, %d" %(self.mnemonic, self.reg, self.addr))

    def printInstructionData(self):
        print("Opcode: %d, Op: %s, Reg: %d, Addr: %d, Addr Mode: %d" %(self.opCode, self.mnemonic, self.reg, self.addr, self.addrMode))

def test():
    instr1 = 28994 # 070502 in octal mult reg 5, reg 2 mode 0
    instr2 = 29596 # 071634 in octal div reg 6, reg4 mode 3

    i1 = oneHalfOperandInstruction(instr1)
    i2 = oneHalfOperandInstruction(instr2)

    i1.printInstructionData()
    i2.printInstructionData()

