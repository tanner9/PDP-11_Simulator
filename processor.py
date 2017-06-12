from dataFetchStage import *
from decodeInstruction import *
from ALU import *
from branchStage import *
import argparse

parser = argparse.ArgumentParser(description="PDP-11 ISA Simulator")

parser.add_argument('-i', action="store", dest="inputFile", default="", help="Set input filename for object code")
parser.add_argument('-v', action="store_true", dest="verbose", default=False, help="Enable verbose mode")
parser.add_argument('-s', action="store_true", dest="singleStep", default=False, help="Enable single step")

args = parser.parse_args()

MASTER_DEBUG = False
MEM_DEBUG = True
DATA_FETCH_DEBUG = True
REGFILE_DEBUG = True
BRANCH_DEBUG = False
TOP_DEBUG = True
verbose = args.verbose
singleStep = args.singleStep

def toByteArray(data):
    operand = bytearray(2)
    operand[1] = data & 0xFF
    operand[0] = (data >> 8) & 0xFF
    return operand

def sign_extend(data):
    sign_bit = data>>7 # bit 8 is signed bit
    mask = 0x8000 >> 7 # {1, 15'b0} sra 7 times. All right shifts in python are arithmetic
    if(sign_bit):
        return mask|data
    else:
        return data&0xFF


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
user_input = ""
while(decodedInstruction.getMnemonic() != "HALT"): 
    while(singleStep == True and user_input != 's'):
        user_input = input('\nEnter "s" to continue single stepping or "run" to execute the rest of the program: ')
        if(user_input == "run"):
            singleStep = False
    user_input = ""
    if(debug):   
        print("Fetching operands for instruction")
    if((decodedInstruction.getNumOperands() > 0) and decodedInstruction.getSize() == "byte"):
        isByte = True
    else:
        isByte = False
    operands = dataFetch.fetchData(decodedInstruction, isByte)
    numOperands = operands[0]
    operand0 = toByteArray(operands[1])
    operand1 = toByteArray(operands[2])
    if(debug):
        print("Fetched operands: ", operand0, ", ", operand1)
    if(decodedInstruction.getMnemonic() == "JMP"):
        data = int((operand0[0]<<16)+operand0[1]) # convert bytearray to int
        if(debug):
            print("Jumping to address %o" %data)
        regFile.writeReg(7, data)
    elif(decodedInstruction.getMnemonic() == "JSR"):
        reg = decodedInstruction.getOpCode() & 0x7 # Half operand stored in bottom 3 bits of opCode of single operand instruction
        regData = regFile.readReg(reg, 0) # Get contents of reg
        topStack = regFile.readReg(6, 4) #move top of stack
        mem.memoryWrite(topStack, regData) # push register data onto stack
        incrPC = regFile.readReg(7, 0) # Get PC
        regFile.writeReg(reg, incrPC) # Store incremented PC in register
        address = dataFetch.getLastAddress() # Effective address is address to jump to
        regFile.writeReg(7, address) # PC = operand0 passed through instruction
    elif(decodedInstruction.getMnemonic() == "RTS"):
        reg = decodedInstruction.getReg()[0] #returns reg and mode. Only reg is valid here
        NPC = regFile.readReg(reg, 0) # Get PC to return to
        regFile.writeReg(7, NPC) # PC = [Reg]
        stackpointer = regFile.readReg(6, 2) # Pop top of stack
        data = mem.memoryRead(stackpointer, 0)
        regFile.writeReg(reg, data) # Write value from top of stack into reg
    elif(decodedInstruction.getType() != "branch"):
        op = decodedInstruction.getMnemonic()
        if(debug):
        	print("ALU operands: %s & %s; OP: %s" % (operand0, operand1, op))
        if(isByte):
            ALUop = op+"B"
        else:
            ALUop = op
        result = ALU.execute(ALU, ALUop, operand0, operand1)
        if(isByte):
            result = result & 0xFF
        if(debug):
            cond_code = ALU.get_condition(ALU)
            print("Condition code: N:%s Z:%s V:%s C:%s " %(cond_code[0], cond_code[1], cond_code[2], cond_code[3]))
        if(debug):
        	print("ALU result: %d" % (result))
        writeBackAddress = dataFetch.getLastAddress()
        if(decodedInstruction.getNumOperands() > 0 and op != "CMP" and op != "BIT"):
            if(decodedInstruction.getDstMode() == 0):
                if(debug):
                    print("Writing back to regfile")
                if(op == "MOV"): # movb is the only byte instruction to write back to whole register
                    if(isByte):
                        result = sign_extend(result)#sign extend to fill word
                    isByte = False
                regFile.writeReg(writeBackAddress, result, isByte)
            else:
                if(debug):
                    print("Writing back to memory")
                if(isByte):
                    mem.memoryWriteByte(writeBackAddress, result)
                else:
                    mem.memoryWrite(writeBackAddress, result)
                
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
