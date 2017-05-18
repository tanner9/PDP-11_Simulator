from RegisterFile import *
from Memory import *

class dataFetchStage:

	def __init__(self, mem, regFile):
		self.mem = mem
		self.regFile = regFile

	def fetchSingleData(self, reg, mode, debug):
		if(mode == 0):
			data = self.regFile.readReg(reg, mode)
		else:
			if(mode == 1 or mode == 2 or mode == 4):
				effectiveAddress = self.regFile.readReg(reg, mode)
				data = self.mem.memoryRead(effectiveAddress, debug)
			elif(mode == 3 or mode == 5):
				address = self.regFile.readReg(reg, mode)
				effectiveAddress = self.mem.memoryRead(address, debug)
				data = self.mem.memoryRead(effectiveAddress, debug)
			elif(mode == 6):
				regAddress = self.regFile.readReg(reg, mode)
				offset = self.getImmediate(debug)
				effectiveAddress = regAddress+offset
				data = self.mem.memoryRead(effectiveAddress, debug)
			else:
				regAddress = self.regFile.readReg(reg, mode)
				offset = self.getImmediate(debug)
				address = regAddress+offset
				effectiveAddress = self.mem.memoryRead(address, debug)
				data = self.mem.memoryRead(effectiveAddress, debug)

			if(debug == True):
				print("Effective address: %d, data: %d" %(effectiveAddress, data))

		return data

	def fetchData(self, instruction, debug):
		data = []
		numOperands = instruction.getNumOperands()
		if(numOperands == 2):
			if(debug == True):
				print("Fetching data for two operand instruction")
			reg = instruction.getReg()
			data.append(self.fetchSingleData(reg[0], reg[1], debug))
			data.append(self.fetchSingleData(reg[2], reg[3], debug))
		elif(numOperands == 1):
			if(debug == True):
				print("Fetching data for one operand instruction")
			reg = instruction.getReg()
			data.append(self.fetchSingleData(reg[0], reg[1], debug))
			data.append(0)
		else:
			if(debug == True):
				print("No data required for current instructions")
			data.append(0)
			data.append(0)

		return data

	def getImmediate(self, debug):
		address = self.regFile.readPC()
		imm = self.mem.memoryRead(address, debug)
		return imm

def test():
	mem = Memory()
	regFile = RegisterFile()
	x = dataFetchStage(mem, regFile)
	x.fetchSingleData(5, 2, False)
	x.fetchSingleData(5, 2, False)
	x.fetchSingleData(5, 4, False)
	x.fetchSingleData(5, 4, False)
