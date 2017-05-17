class zeroOperandInstruction:

    def __init__(self, instructionValue):
        self.value = instructionValue
        self.numOperands = 0
        self.opCode = instructionValue
        if(self.opCode == 0):
            self.mnemonic = "HALT"
        elif(self.opCode == 1):
            self.mnemonic = "WAIT"
        elif(self.opCode == 5):
            self.mnemonic = "RESET"
        elif(self.opCode == 0o240):
            self.mnemonic = "NOP"
        else:
            self.mnemonic = "ERROR"

    def printValue(self):
        print("Opcode value in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Opcode value in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def getNumOperands(self):
        return self.numOperands

    def printInstructionData(self):
        print("Opcode: %d, Op: %s" %(self.opCode, self.mnemonic))

def test():
    instr1 = 0 # 000000 in octal HALT
    instr2 = 1 # 000001 in octal WAIT
    instr3 = 5 # 000005 in octal RESET

    i1 = zeroOperandInstruction(instr1)
    i2 = zeroOperandInstruction(instr2)
    i3 = zeroOperandInstruction(instr3)

    i1.printInstructionData()
    i2.printInstructionData()
    i3.printInstructionData()
