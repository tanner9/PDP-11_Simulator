# twoOperandInstruction.py
# Author: Tanner Shephard
# Description: Decodes and holds data for any double operand instruction. Value 
#              is given as a number and then all relevant variables are written 
#              via shifts and masks


class twoOperandInstruction:

    def __init__(self,instructionValue):
        self.value = instructionValue
        self.numOperands = 2
        self.type = "twoOperand"
        self.dstMode = (instructionValue>>3)&0x7
        self.dstReg = instructionValue&0x7
        self.srcMode = (instructionValue>>9)&0x7
        self.srcReg = (instructionValue>>6)&0x7
        self.opCode = (instructionValue>>12)&0x7
        if(self.opCode == 6 or self.opCode == 14):
            self.size = "word"
        else:
            if(instructionValue>>15):
                self.size = "byte"
            else:
                self.size = "word"

        if(self.opCode == 1):
            self.mnemonic = "MOV"
        elif(self.opCode == 6):
            self.mnemonic = "ADD"
        elif(self.opCode == 0o16):
            self.mnemonic = "SUB"
        elif(self.opCode == 2):
            self.mnemonic = "CMP"
        elif(self.opCode == 5):
            self.mnemonic = "BIS"
        elif(self.opCode == 4):
            self.mnemonic = "BIC"
        elif(self.opCode == 3):
            self.mnemonic = "BIT" 
        else:
            self.mnemonic = "ERROR"

    def printValue(self):
        print("Instruction in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Instruction in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def getMnemonic(self):
        return self.mnemonic

    def getDstMode(self):
        return self.dstMode

    def getReg(self):
        x = []
        x.append(self.srcReg)
        x.append(self.srcMode)
        x.append(self.dstReg)
        x.append(self.dstMode)
        return x

    def getNumOperands(self):
        return self.numOperands

    def getType(self):
        return self.type

    def getSize(self):
        return self.size

    def printInstruction(self):
        print("%s %d, %d" %(self.mnemonic, self.dstReg, self.srcReg))

    def printInstructionData(self):
        x = 'W' if (self.size == "word") else 'B'
        print("Opcode: %d, Op: %s, Src Reg: %d, Mode: %d, Dst Reg: %d, Mode: %d, Type: %s " %(self.opCode, self.mnemonic, self.srcReg, self.srcMode, self.dstReg, self.dstMode, x))


def test():
    instr1 = 24576 # 060000 in octal add r0, r0
    instr2 = 24705 # 060201 in octal add r1, r2
    instr3 = 60089 # 165271 in octal sub r1 mode 7, r2 mode 5

    i1 = twoOperandInstruction(instr1)
    i2 = twoOperandInstruction(instr2)
    i3 = twoOperandInstruction(instr3)

    i1.printInstructionData()
    i2.printInstructionData()
    i3.printInstructionData()
