from dataFetchStage import *
from decodeInstruction import *
from ALU import *


MEM_DEBUG = True
DATA_FETCH_DEBUG = True
REGFILE_DEBUG = True

def toByteArray(data):
	operand = bytearray(2)
	operand[0] = data & 0xFF
	operand[1] = (data >> 8) & 0xFF
	return operand

startingAddress = 0
#initialize all stage
mem = Memory(MEM_DEBUG)
mem.readFileIntoMemory()
regFile = RegisterFile(REGFILE_DEBUG)
dataFetch = dataFetchStage(mem, regFile, DATA_FETCH_DEBUG)
decodeStage = decodeStage()
ALU = ALU()


#fetch and execute first instruction
IR = regFile.readPC()
instruction = mem.memoryRead(IR)
decodedInstruction = decodeStage.decodeInstruction(instruction)
operands = dataFetch.fetchData(decodedInstruction)
operand0 = toByteArray(operands[0])
operand1 = toByteArray(operands[1])
print("ALU operands: %s & %s; OP: %s" %(operand0, operand1, decodedInstruction.getMnemonic()))
result = ALU.execute(decodedInstruction.getMnemonic(),operand0, operand1)
print("ALU result: %d" %(result))
