class branchStage:

	def __init__(self, debug):
		self.debug = debug

	def checkBranch(self, op, condition):
		if(op == "BR"):
			return True
		elif(op == "BNE"):
			return (condition[0] == '0')
		elif(op == "BEQ"):
			return (condition[0] == '1')
		elif(op == "BGE"):
			return (condition[3] == condition[2])
		elif(op == "BLT"):
			return (condition[3] != condition[2])
		elif(op == "BGT"):
			return (((condition[3] != condition[2]) or condition[0]) == False)
		elif(op == "BLE"):
			return (((condition[3] != condition[2]) or condition[0]) == True)
		elif(op == "BPL"):
			return ((condition[3]) == False)
		elif(op == "BMI"):
			return (condition[3])
		elif(op == "BHI"):
			return ((condition[1] or condition[0]) == False)
		elif(op == "BLOS"):
			return ((condition[1] or condition[0]) == True)
		elif(op == "BVC"):
			return (condition[2] == False)
		elif(op == "BVS"):
			return (condition[2])
		elif(op == "BHIS/BCC"):
			return (condition[1] == False)
		elif(op == "BLO/BCS"):
			return (condition[1])
		else:
			print("Unknown branch op passed")
			return False

