class oneOperandInstruction:

    def __init__(self, instructionValue):
        self.value = instructionValue
        self.mode = (instructionValue>>3)&0x7
        self.reg = instructionValue&0o7
        self.opCode = (instructionValue>>6)&0x1ff
        if(self.opCode == 3 or self.opCode == 67):
            self.size = "word"
        else:
            if(instructionValue>>15):
                self.size = "byte"
            else:
                self.size = "word"

        if(self.opCode == 0o50):
            self.mnemonic = "CLR"
        elif(self.opCode == 0o52):
            self.mnemonic = "INC"
        elif(self.opCode == 0o53):
            self.mnemonic = "DEC"
        elif(self.opCode == 0o55):
            self.mnemonic = "ADC"
        elif(self.opCode == 0o56):
            self.mnemonic = "SBC"
        elif(self.opCode == 0o57):
            self.mnemonic = "TST"
        elif(self.opCode == 0o54):
            self.mnemonic = "NEG"
        elif(self.opCode == 0o51):
            self.mnemonic = "COM"
        elif(self.opCode == 0o60):
            self.mnemonic = "ROR"
        elif(self.opCode == 0o61):
            self.mnemonic = "ROL"
        elif(self.opCode == 0o62):
            self.mnemonic = "ASR"
        elif(self.opCode == 0o63):
            self.mnemonic = "ASL"
        elif(self.opCode == 0o3):
            self.mnemonic = "SWAB"
        elif(self.opCode == 0o67):
            self.mnemonic = "SoT"  
        else:
            self.mnemonic = "ERROR"

    def printValue(self):
        print("Instruction in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Instruction in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def printInstruction(self):
        print("%s %d" %(self.mnemonic, self.reg))

    def printInstructionData(self):
        x = 'W' if (self.size == "word") else 'B'
        print("Opcode: %d, Op: %s, Reg: %d, Mode: %d, Type: %s " %(self.opCode, self.mnemonic, self.reg, self.mode, x))

def test():
    instr1 = 0o000332  # swab reg 2, mode 3
    instr2 = 0o105060  # CLR byte reg 0, mode 6

    i1 = oneOperandInstruction(instr1)
    i2 = oneOperandInstruction(instr2)

    i1.printInstructionData()
    i2.printInstructionData()