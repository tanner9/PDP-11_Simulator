# branchStage.py
# Author: Tanner Shephard
# Description: Takes in condition codes and determines for the given operation
#              if the branch should be taken or not

class branchStage:

    def __init__(self, debug):
        self.debug = debug

    def checkBranch(self, op, cond):
        condition = []
        condition.append(int(cond[1])) # condition[0] = Z
        condition.append(int(cond[3])) # condition[1] = C
        condition.append(int(cond[2])) # condition[2] = V
        condition.append(int(cond[0])) # condition[3] = N
        
        if(op == "BR"):
            return True
        elif(op == "BNE"):
            return (condition[0] == 0) # Z=0
        elif(op == "BEQ"):
            return (condition[0] == 1) # Z=1
        elif(op == "BGE"):
            return (condition[3] == condition[2]) # N xor V = 0
        elif(op == "BLT"):
            return (condition[3] != condition[2]) # N xor V = 1
        elif(op == "BGT"):
            return (((condition[3] != condition[2]) or condition[0]) == 0) # (N xor V) or Z = 0
        elif(op == "BLE"):
            return ((condition[3] != condition[2]) or condition[0]) #(N xor V) or Z = 1
        elif(op == "BPL"):
            return ((condition[3]) == 0) # N = 0
        elif(op == "BMI"):
            return (condition[3]) # N =1
        elif(op == "BHI"):
            return ((condition[1] or condition[0]) == 0) # C or Z = 0
        elif(op == "BLOS"):
            return (condition[1] or condition[0]) # C or Z = 1
        elif(op == "BVC"):
            return (condition[2] == 0) # V = 0
        elif(op == "BVS"):
            return (condition[2]) # V = 1
        elif(op == "BHIS/BCC"):
            return (condition[1] == 0) # C = 0
        elif(op == "BLO/BCS"):
            return (condition[1]) # C = 1
        else:
            print("Unknown branch op passed")
            return False
