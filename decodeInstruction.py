# decodeInstruction.py
# Author: Tanner Shephard and Manasvi Prasad
# Description: Takes in raw instruction value. Decodes type of instruction then passes data into 
#              the appropriate class to be further decoded

from twoOperandInstruction import *
from nopInstruction import *
from oneOperandInstruction import *
from branchInstruction import *
from zeroOperandInstruction import *

class decodeStage:

	def decodeInstruction(self,instructionValue):
		if((instructionValue>>12) == 0x7):
			instruction = nopInstruction()
		elif((((instructionValue>>11)&0xf) == 0x1) or ((instructionValue>>6) == 3) or ((instructionValue>>6) == 67) or ((instructionValue>>3) == 16) or ((instructionValue>>6) == 1)):
			instruction = oneOperandInstruction(instructionValue)
		elif((instructionValue>>8) == 0):
			instruction = zeroOperandInstruction(instructionValue)
		elif(((instructionValue>>11)&0xf) == 0):
			instruction = branchInstruction(instructionValue)
		else:
			instruction = twoOperandInstruction(instructionValue)

		return instruction
	
	def instructionCount(self,decodeInstr):
                instructionsList = []
                instructionsList.append(decodeInstr.mnemonic)
                total_count = len(instructionsList)
                print("Instruction Count is %d" %(total_count))
                print("The Executed Instructions are %s" %(instructionsList))
		
	def printInstruction(self):
		self.printInstructionData()

def test():
	x = decodeStage()
	#two operand instructions
	instr1 = 24576 # 060000 in octal add r0, r0
	instr2 = 24705 # 060201 in octal add r1, r2
	instr3 = 60089 # 165271 in octal sub r1 mode 7, r2 mode 5

	i1 = x.decodeInstruction(instr1)
	i2 = x.decodeInstruction(instr2)
	i3 = x.decodeInstruction(instr3)

	i1.printInstructionData()
	i2.printInstructionData()
	i3.printInstructionData()

	#One and a half operand instructions
	instr1 = 28994 # 070502 in octal mult reg 5, reg 2 mode 0
	instr2 = 29596 # 071634 in octal div reg 6, reg4 mode 3

	i1 = x.decodeInstruction(instr1)
	i2 = x.decodeInstruction(instr2)

	i1.printInstructionData()
	i2.printInstructionData()

    #One Operand Instructions
	instr1 = 0o000332  # swab reg 2, mode 3
	instr2 = 0o105060  # CLR byte reg 0, mode 6

	i1 = x.decodeInstruction(instr1)
	i2 = x.decodeInstruction(instr2)

	i1.printInstructionData()
	i2.printInstructionData()

    #Branch instructions
	instr1 = (0b00000011<<8) + 57   # beq, offset 57
	instr2 = (0b00000111<<8) + 101  # ble, offset 101

	i1 = x.decodeInstruction(instr1)
	i2 = x.decodeInstruction(instr2)

	i1.printInstructionData()
	i2.printInstructionData()

	#zero operand instruction
	instr1 = 0 # 000000 in octal HALT
	instr2 = 1 # 000001 in octal WAIT
	instr3 = 5 # 000005 in octal RESET

	i1 = x.decodeInstruction(instr1)
	i2 = x.decodeInstruction(instr2)
	i3 = x.decodeInstruction(instr3)

	i1.printInstructionData()
	i2.printInstructionData()
	i3.printInstructionData()

