from dataFetchStage import *
from decodeInstruction import *

mem = Memory()
regFile = RegisterFile()
dataFetch = dataFetchStage(mem, regFile)
decode = decodeStage()

instr1 = 24576 # 060000 in octal add r0, r0
instr2 = 24705 # 060201 in octal add r1, r2
instr3 = 60089 # 165271 in octal sub r1 mode 7, r2 mode 5

i1 = decode.decodeInstruction(instr1)
i2 = decode.decodeInstruction(instr2)
i3 = decode.decodeInstruction(instr3)

i1.printInstructionData()
i2.printInstructionData()
i3.printInstructionData()

data = dataFetch.fetchData(i3, True)
print(data)

instr1 = 0o000332  # swab reg 2, mode 3
instr2 = 0o105060  # CLR byte reg 0, mode 6

i1 = oneOperandInstruction(instr1)
i2 = oneOperandInstruction(instr2)

i1.printInstructionData()
i2.printInstructionData()

data = dataFetch.fetchData(i1, False)
print(data)

regFile.printRegFile()
regFile.readPC()
regFile.printRegFile()
