class branchInstruction:

    def __init__(self, instructionValue):
        self.value = instructionValue
        self.opCode = (instructionValue>>8)
        self.offset = instructionValue&0xFF
        if(self.opCode == 1):
            self.mnemonic = "BR"
        elif(self.opCode == 2):
            self.mnemonic = "BNE"
        elif(self.opCode == 3):
            self.mnemonic = "BEQ"
        elif(self.opCode == 128):
            self.mnemonic = "BPL"
        elif(self.opCode == 129):
            self.mnemonic = "BMI"
        elif(self.opCode == 132):
            self.mnemonic = "BVC"
        elif(self.opCode == 133):
            self.mnemonic = "BVS"
        elif(self.opCode == 134):
            self.mnemonic = "BHIS/BCC"
        elif(self.opCode == 135):
            self.mnemonic = "BLO/BCS"
        elif(self.opCode == 4):
            self.mnemonic = "BGE"
        elif(self.opCode == 5):
            self.mnemonic = "BLT"
        elif(self.opCode == 6):
            self.mnemonic = "BGT"
        elif(self.opCode == 7):
            self.mnemonic = "BLE"
        elif(self.opCode == 130):
            self.mnemonic = "BHI"
        elif(self.opCode == 131):
            self.mnemonic = "BLOS"
        else:
            self.mnemonic = "ERROR"

    def printValue(self):
        print("Instruction value in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Instruction value in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def printInstructionData(self):
        print("Opcode: %d, Op: %s, Offset: %d " %(self.opCode, self.mnemonic, self.offset))

def test():
    instr1 = (0b00000011<<8) + 57   # beq, offset 57
    instr2 = (0b00000111<<8) + 101  # ble, offset 101

    i1 = branchInstruction(instr1)
    i2 = branchInstruction(instr2)

    i1.printInstructionData()
    i2.printInstructionData()
