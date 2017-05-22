from RegisterFile import *
from Memory import *

class dataFetchStage:

	def __init__(self, mem, regFile, debug):
		self.mem = mem
		self.regFile = regFile
		self.debug = debug
		self.lastAddress = 0

	def fetchSingleData(self, reg, mode):
		if(mode == 0):
			data = self.regFile.readReg(reg, mode)
			self.lastAddress = reg
		else:
			if(mode == 1 or mode == 2 or mode == 4):
				effectiveAddress = self.regFile.readReg(reg, mode)
				data = self.mem.memoryRead(effectiveAddress)
			elif(mode == 3 or mode == 5):
				address = self.regFile.readReg(reg, mode)
				effectiveAddress = self.mem.memoryRead(address)
				data = self.mem.memoryRead(effectiveAddress)
			elif(mode == 6):
				regAddress = self.regFile.readReg(reg, mode)
				offset = self.getImmediate()
				offset = twos_comp(offset, 16)
				effectiveAddress = regAddress+offset
				data = self.mem.memoryRead(effectiveAddress)
			else:
				regAddress = self.regFile.readReg(reg, mode)
				offset = self.getImmediate()
				address = regAddress+offset
				effectiveAddress = self.mem.memoryRead(address)
				data = self.mem.memoryRead(effectiveAddress)

			self.lastAddress = effectiveAddress
			if(self.debug == True):
				print("Effective address: %d, data: %d" %(effectiveAddress, data))

		return data     

	def fetchData(self, instruction):
		data = []
		numOperands = instruction.getNumOperands()
		data.append(numOperands)
		if(numOperands == 2):
			if(self.debug == True):
				print("Fetching data for two operand instruction")
			reg = instruction.getReg()
			data.append(self.fetchSingleData(reg[0], reg[1]))
			data.append(self.fetchSingleData(reg[2], reg[3]))
		elif(numOperands == 1):
			if(self.debug == True):
				print("Fetching data for one operand instruction")
			reg = instruction.getReg()
			data.append(self.fetchSingleData(reg[0], reg[1]))
			data.append(0)
		else:
			if(self.debug == True):
				print("No data required for current instructions")
			data.append(0)
			data.append(0)

		return data

	def getImmediate(self):
		address = self.regFile.readPC()
		imm = self.mem.memoryRead(address)
		return imm

	def getLastAddress(self):
		if(self.debug == True):
			print("Fetched effective address: %d for write back" %(self.lastAddress))
		return self.lastAddress

def test():
	debug = False
	mem = Memory(debug)
	regFile = RegisterFile(debug)
	x = dataFetchStage(mem, regFile, debug)
	x.fetchSingleData(5, 2)
	x.fetchSingleData(5, 2)
	x.fetchSingleData(5, 4)
	x.fetchSingleData(5, 4)

def twos_comp(val, bits):
	if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val 