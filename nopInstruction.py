# nopInstruction.py
# Author: Tanner Shephard
# Description: Class for nop instruction. May not be used in final design

class nopInstruction:

    def __init__(self):
        self.mnemonic = "NOP"
        self.numOperands = -1
        self.type = "nop"

    def getReg(self):
        x = []
        return x

    def getNumOperands(self):
        return self.numOperands

    def printValue(self):
        print("Instruction in decimal: %s" %(self.value))

    def printValueOct(self):
        print("Instruction in octal: %s" %(oct(self.value)))

    def printMnemonic(self):
        print(self.mnemonic)

    def getMnemonic(self):
        return self.mnemonic

    def getType(self):
        return self.type

    def printInstruction(self):
        print("%s" %(self.mnemonic))

    def printInstructionData(self):
        print("NOP")

