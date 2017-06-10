from dataFetchStage import *
from decodeInstruction import *
from ALU import *
from branchStage import *
import argparse

parser = argparse.ArgumentParser(description="PDP-11 ISA Simulator")

parser.add_argument('-i', action="store", dest="inputFile", default="", help="Set input filename for object code")
parser.add_argument('-v', action="store_true", dest="verbose", default=False, help="Enable verbose mode")

args = parser.parse_args()

MASTER_DEBUG = True
MEM_DEBUG = False
DATA_FETCH_DEBUG = False
REGFILE_DEBUG = False
BRANCH_DEBUG = False
TOP_DEBUG = False
verbose = args.verbose

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
# initialize all stage
mem = Memory(MEM_DEBUG, args.inputFile)
mem.readFileIntoMemory()
mem.traceFileOpen()
regFile = RegisterFile(REGFILE_DEBUG)
regFile.writeReg(7, mem.getStartingAddress())
dataFetch = dataFetchStage(mem, regFile, DATA_FETCH_DEBUG)
decodeStage = decodeStage()
ALU = ALU
branchStage = branchStage(BRANCH_DEBUG)


# fetch and execute first instruction
debug = TOP_DEBUG
PC = regFile.readPC()
if(debug):
    print("Starting Address: %o" %PC)
if(debug):
    print("\nPC for current instruction =", PC)
IR = mem.memoryRead(PC, 2)
if(debug):
    print("IR =", IR)
decodedInstruction = decodeStage.decodeInstruction(IR)

if(verbose):
    print("\n")
    regFile.printRegFile()
    cond_code = ALU.get_condition(ALU)
    print("Condition code: N:%s Z:%s V:%s C:%s " %(cond_code[0], cond_code[1], cond_code[2], cond_code[3]))
if(debug | verbose):
    decodedInstruction.printInstructionData()

while(decodedInstruction.getMnemonic() != "HALT"): 
    if(debug):   
        print("Fetching operands for instruction")
    operands = dataFetch.fetchData(decodedInstruction)
    numOperands = operands[0]
    operand0 = toByteArray(operands[1])
    operand1 = toByteArray(operands[2])
    if(debug):
        print("Fetched operands: ", operand0, ", ", operand1)
    if(decodedInstruction.getMnemonic == "JMP"):
        if(debug):
            print("Jumping to address %o" %operand0)
        regFile.writeReg(7, operand0)
    elif(decodedInstruction.getType() != "branch"):
        op = decodedInstruction.getMnemonic()
        if(debug):
        	print("ALU operands: %s & %s; OP: %s" % (operand0, operand1, op))
        result = ALU.execute(ALU, op, operand0, operand1)
        if(debug):
            cond_code = ALU.get_condition(ALU)
            print("Condition code: N:%s Z:%s V:%s C:%s " %(cond_code[0], cond_code[1], cond_code[2], cond_code[3]))
        if(debug):
        	print("ALU result: %d" % (result))
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
        offset = twos_comp(offset, 8)
        condition = ALU.get_condition(ALU)
        branchTrue = branchStage.checkBranch(op, condition)
        if(branchTrue == True):
            PC = regFile.readReg(7, 0)
            target = PC + (2 * offset)
            if(debug):
            	print("Branching to target address: %d. Offset was %d" %(target, offset))
            regFile.writeReg(7, target)

    PC = regFile.readPC()
    if(debug):
        print("\nPC for current instruction =", PC)
    IR = mem.memoryRead(PC, 2)
    if(debug):
        print("IR =", IR)
    decodedInstruction = decodeStage.decodeInstruction(IR)

    if(verbose):
        print("\n")
        regFile.printRegFile()
        cond_code = ALU.get_condition(ALU)
        print("Condition code: N:%s Z:%s V:%s C:%s " %(cond_code[0], cond_code[1], cond_code[2], cond_code[3]))

    if(debug | verbose):
        decodedInstruction.printInstructionData()

if(debug):
    print("\nProgram has halted\n")

print("\nInstructions Executed: %d" %(mem.getInstructionCount()))
mem.memoryRead(0, 0)
mem.memoryRead(2, 0)
mem.memoryRead(4, 0)
