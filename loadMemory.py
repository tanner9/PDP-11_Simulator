#FIXME: use memory class instead of bytearray
filename = "test.ascii"
startAddressLine = ""
mem = bytearray(64000)
pos = 0
with open(filename) as fp:
    for line in fp:
        if(line[0] == '*'):
            startAddressLine = line
        elif(line[0] == '@'):
            pos = int(line[1:], 8)
        else:
            tempLine = int(line[1:], 8)
            mem[pos] = tempLine&0xff
            mem[pos+1] = (tempLine>>8)&0xff
            pos += 2
            

if(startAddressLine == ""):
    startingAddress = input('Enter the starting address: ')
else:
    startingAddress = line[1:]

# Uncomment following lines to test memory contents 
#for i in range(0,58):
#    print(mem[i])


