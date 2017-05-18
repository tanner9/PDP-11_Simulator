from dataFetchStage import *
from decodeInstruction import *
from ALU import *


MEM_DEBUG = True
DATA_FETCH_DEBUG = True

def toByteArray(data):
	operand = bytearray(2)
	operand[0] = data & 0xFF
	operand[1] = (data >> 8) & 0xFF
	return operand

startingAddress = 0

mem = Memory()
mem.readFileIntoMemory(MEM_DEBUG)
regFile = RegisterFile()
dataFetch = dataFetchStage(mem, regFile)
decodeStage = decodeStage()
ALU = ALU()

IR = regFile.readPC()
instruction = mem.memoryRead(IR, MEM_DEBUG)
decodedInstruction = decodeStage.decodeInstruction(instruction)
operands = dataFetch.fetchData(decodedInstruction, DATA_FETCH_DEBUG)
operand0 = toByteArray(operands[0])
operand1 = toByteArray(operands[1])
print("ALU operands: %s & %s; OP: %s" %(operand0, operand1, decodedInstruction.getMnemonic()))
result = ALU.execute(decodedInstruction.getMnemonic(),operand0, operand1)
print("ALU result: %d" %(result))
