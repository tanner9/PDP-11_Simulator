class branchStage:

    def __init__(self, debug):
        self.debug = debug

    def checkBranch(self, op, cond):
        condition = []
        condition.append(int(cond[0])) # condition[0] = Z
        condition.append(int(cond[1])) # condition[1] = C
        condition.append(int(cond[2])) # condition[2] = V
        condition.append(int(cond[3])) # condition[3] = N
        
        if(op == "BR"):
            return True
        elif(op == "BNE"):
            return (condition[0] == 0)
        elif(op == "BEQ"):
            return (condition[0] == 0)
        elif(op == "BGE"):
            return ((condition[3] & condition[2]) == 0)
        elif(op == "BLT"):
            return (condition[3] & condition[2])
        elif(op == "BGT"):
            return (((condition[3] & condition[2]) or condition[0]) == 0)
        elif(op == "BLE"):
            return ((condition[3] & condition[2]) or condition[0])
        elif(op == "BPL"):
            return ((condition[3]) == 0)
        elif(op == "BMI"):
            return (condition[3])
        elif(op == "BHI"):
            return ((condition[1] or condition[0]) == 0)
        elif(op == "BLOS"):
            return (condition[1] or condition[0])
        elif(op == "BVC"):
            return (condition[2] == 0)
        elif(op == "BVS"):
            return (condition[2])
        elif(op == "BHIS/BCC"):
            return (condition[1] == 0)
        elif(op == "BLO/BCS"):
            return (condition[1])
        else:
            print("Unknown branch op passed")
            return False
