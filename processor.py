from dataFetchStage import *
from decodeInstruction import *
from ALU import *
from branchStage import *

MASTER_DEBUG = True
MEM_DEBUG = True
DATA_FETCH_DEBUG = True
REGFILE_DEBUG = True
BRANCH_DEBUG = True
TOP_DEBUG = True

def toByteArray(data):
	operand = bytearray(2)
	operand[1] = data & 0xFF
	operand[0] = (data >> 8) & 0xFF
	return operand

if(MASTER_DEBUG == False):
	MEM_DEBUG = False
	DATA_FETCH_DEBUG = False
	REGFILE_DEBUG = False
	BRANCH_DEBUG = False
	TOP_DEBUG = False

startingAddress = 0
#initialize all stage
mem = Memory(MEM_DEBUG)
mem.readFileIntoMemory()
regFile = RegisterFile(REGFILE_DEBUG)
regFile.writeReg(7, int(mem.getStartingAddress()))
dataFetch = dataFetchStage(mem, regFile, DATA_FETCH_DEBUG)
decodeStage = decodeStage()
ALU = ALU()
branchStage = branchStage(BRANCH_DEBUG)


#fetch and execute first instruction
debug = TOP_DEBUG
PC = regFile.readPC()
if(debug):
	print("PC for current instruction =",PC)
IR = mem.memoryRead(PC, 2)
if(debug):
	print("IR =",IR)
decodedInstruction = decodeStage.decodeInstruction(IR)

if(debug):
	print("Decoded Instruction: ",decodedInstruction.printInstructionData())
	print("Fetching operands for instruction")

while(decodedInstruction.getMnemonic() != "HALT"):
	operands = dataFetch.fetchData(decodedInstruction)
	numOperands = operands[0]
	operand0 = toByteArray(operands[1])
	operand1 = toByteArray(operands[2])
	if(debug):
		print("Fetched operands: ", operand0, ", ", operand1)
	if(decodedInstruction.getType() != "branch"):
		op = decodedInstruction.getMnemonic()
		print("ALU operands: %s & %s; OP: %s" %(operand0, operand1, op))
		result = ALU.execute(op,operand0, operand1)
		print("ALU result: %d" %(result))
		writeBackAddress = dataFetch.getLastAddress()
		if(decodedInstruction.getNumOperands() > 0 and op != "CMP" and op != "BIT"):
			if(decodedInstruction.getDstMode() == 0):
				regFile.writeReg(writeBackAddress, result)
				if(debug):
					print("Writing back to regfile")
			else:
				mem.memoryWrite(writeBackAddress, result)
				if(debug):
					print("Writing back to memory")
	else:
		op = decodedInstruction.getMnemonic()
		offset = decodedInstruction.getOffset()
		condition = ALU.get_condition()
		branchTrue = branchStage.checkBranch(op, condition)
		if(branchTrue == True):
			PC = regFile.readReg(7)
			regFile.writeReg(7, PC+offset)

	PC = regFile.readPC()
	if(debug):
		print("PC for current instruction =",PC)
	IR = mem.memoryRead(PC, 2)
	if(debug):
		print("IR =",IR)
	decodedInstruction = decodeStage.decodeInstruction(IR)

	if(debug):
		print("Decoded Instruction: ",decodedInstruction.printInstructionData())
		print("Fetching operands for instruction")



