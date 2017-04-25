#FIXME: use memory class instead of bytearray
filename = "test.ascii"
startingAddress = -1
mem = bytearray(64000)
pos = 0
with open(filename) as fp:
    for line in fp:
        if(line[0] == '*'):
            startingAdress = line[1:]
        elif(line[0] == '@'):
            pos = int(line[1:], 8)
        else:
            tempLine = int(line[1:], 8)
            mem[pos] = tempLine&0xff
            mem[pos+1] = (tempLine>>8)&0xff
            pos += 2
            

if(startingAddress == -1):
    startingAddress = input('Enter the starting address: ')

# Uncomment following lines to test memory contents 
#for i in range(0,58):
#    print(mem[i])


