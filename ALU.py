

import math
from bitarray import bitarray
    
# Use these for bit position
_N = 8
_Z = 4
_V = 2
_C = 1

_BYTE_MASK = 0x00FF
_WORD_MASK = 0xFFFF
_HIGH_ORDER_BIT_WORD = 0x8000
_HIGH_ORDER_BIT_BYTE = 0x80
_LOW_ORDER_BIT = 0x01

class ALU:
    
    __condition_zer = False
    __condition_neg = False
    __condition_ove = False
    __condition_car = False
    __condition_code = 0

    # The next are for testing. They will be replaced by input.
    elements = [5, 23]
    elements2 = [0, 0]
    
    primary = bytearray(elements)
    secondary = bytearray(elements2) 
    # These are the word size version of the byte arrays in stings
    string = "{:08b}".format(primary[1]) + "{:08b}".format(primary[0])
    string2 = "{:08b}".format(secondary[1]) + "{:08b}".format(secondary[0])
    # These are the one byte version of the byte arrays in strings
    stringb = "{:08b}".format(primary[0])
    string2b = "{:08b}".format(secondary[1])
    # The word sized bit arrays
    first = bitarray(string, endian='big')
    second = bitarray(string2, endian='big')
    # The byte sized bit array
    firstb = bitarray(stringb, endian='big')
    secondb = bitarray(string2b, endian='big')

    word_integer = primary[0]*256 + primary[1]
    byte_integer = primary[1]
    
    word_integer_second = secondary[0]*256 + secondary[1]
    byte_integer_second = secondary[1]

    mod = 0
    
    def execute(self, mnemonic, operand1, operand2 = secondary, modifier = 0):
        
        self.mod = modifier

        self.word_integer = operand1[0]*256 + operand1[1]
        self.byte_integer = operand1[1]
    
        self.word_integer_second = operand2[0]*256 + operand2[1]
        self.byte_integer_second = operand2[1]
        

        # Single operand instructions
        if mnemonic is 'dec':
            self.__dec(self)
        elif mnemonic is 'clr':
            self.__clr(self)
        elif mnemonic is 'inc':
            self.__inc(self)
        elif mnemonic is 'neg':
            self.__neg(self)
        elif mnemonic is 'tst':
            self.__tst(self)
        elif mnemonic is 'com':
            self.__com(self)
        elif mnemonic is 'asr':
            self.__asr(self)
        elif mnemonic is 'asl':
            self.__asl(self)
        elif mnemonic is 'adc':
            self.__adc(self)
        elif mnemonic is 'sbc':
            self.__sbc(self)
        elif mnemonic is 'rol':
            self.__rol(self)
        elif mnemonic is 'ror':
            self.__ror(self)
        elif mnemonic is 'swab':
            self.word_integer = primary[1]*16 + primary[0] # Just re-initialized on reverse order

        # From here on out I have to re-initialize since the functions will only use the last byte

        elif mnemonic is 'decb':
            self.__decb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'clrb':
            self.__clrb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'incb':
            self.__incb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'negb':
            self.__negb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'tstb':
            self.__tstb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'comb':
            self.__comb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'asrb':
            self.__asrb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'aslb':
            self.__aslb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'adcb':
            self.__adcb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'sbcb':
            self.__sbcb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'rolb':
            self.__rolb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'rorb':
            self.__rorb(self)
            self.word_integer = primary[0]*16 + byte_integer

        # Double operand instructions

        elif mnemonic is 'add':
            self.__add(self)
        elif mnemonic is 'sub':
            self.__sub(self)
        elif mnemonic is 'cmp':
            self.__cmp(self)
        elif mnemonic is 'bis':
            self.__bis(self)
        elif mnemonic is 'bit':
            self.__bit(self)
        elif mnemonic is 'bic':
            self.__bic(self)

        # From here on out I have to re-initialize word_integer, since the functions will only use the last byte
      
        elif mnemonic is 'cmpb':
            self.__cmpb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'bisb':
            self.__bisb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'bitb':
            self.__bitb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnemonic is 'bicb':
            self.__bicb(self)
            self.word_integer = primary[0]*16 + byte_integer

        # The final section is for Condition code operators
        elif mnemonic is 'clc':
            self.__clc(self)
        elif mnemonic is 'clv':
            self.__clv(self)
        elif mnemonic is 'clz':
            self.__clz(self)
        elif mnemonic is 'cln':
            self.__cln(self)
        elif mnemonic is 'sec':
            self.__sec(self)
        elif mnemonic is 'sev':
            self.__sev(self)
        elif mnemonic is 'sez':
            self.__sez(self)
        elif mnemonic is 'sen':
            self.__sen(self)

        return self.word_integer
      
        # End of the execute() function

    # Condition output variable is generated by this function
    def get_condition(self):
        self.__condition_code = 0
        if self.__condition_neg:
            self.__condition_code += _N
        if(self.__condition_ove):
            self.__condition_code += _V
        if(self.__condition_car):
            self.__condition_code += _C
        if(self.__condition_zer):
            self.__condition_code += _Z
        return "{:04b}".format(self.__condition_code)
        
    # From here on out I am defining all of the assembly code instruction functions

    def __clr(self):
        self.first.setall(False)
        self.word_integer = 0
        
        self.__condition_zer  = True
        self.__condition_neg  = False
        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __dec(self):
        self.word_integer = self.word_integer -1

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer is _HIGH_ORDER_BIT_WORD: # That is in octal
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
        
    def __inc(self, modifier):

        self.word_integer = self.word_integer + 1

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer is 0x7FFF: # again that is in octal
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __neg(self):
        if self.word_integer < _HIGH_ORDER_BIT_WORD:
            self.word_integer = (~self.word_integer + 1 ) # Two's compliment negate
        else:
            self.word_integer = _HIGH_ORDER_BIT_WORD
            
        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer is _HIGH_ORDER_BIT_WORD: # again that is in octal
            self.__condition_ove = True 
        else:
            self.__condition_ove = False

        if self.word_integer is 0: # again that is in octal
            self.__condition_car = False 
        else:
            self.__condition_car = True
        
    def __tst(self, modifier):

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __cmp(self, modifier):

        self.word_integer = (~self.word_integer)&_WORD_MASK

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = True

    def __clrb(self):
        self.firstb.setall(False)
        self.byte_integer = 0

        self.__condition_zer  = True
        self.__condition_neg  = False
        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __decb(self):

        self.byte_integer = self.byte_integer - 1

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer is 31:
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __incb(self, modifier):

        self.byte_integer = self.byte_integer + 1

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer is 31:
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __negb(self):
        if self.byte_integer < _HIGH_ORDER_BIT_BYTE:
            self.byte_integer = (~self.byte_integer + 1 ) # Two's compliment negate
        else:
            self.byte_integer = _HIGH_ORDER_BIT_BYTE
        
        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer is _HIGH_ORDER_BIT_BYTE: # again that is in octal binary 1000 0000
            self.__condition_ove = True 
        else:
            self.__condition_ove = False

        if self.byte_integer is 0: # again that is in octal
            self.__condition_car = False 
        else:
            self.__condition_car = True
        
    def __tstb(self, modifier):

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __comb(self):
      
        self.byte_integer = (~self.byte_integer) & _BYTE_MASK

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = True
        
    def __asr(self):
        holder = self.word_integer & _HIGH_ORDER_BIT_WORD
        self.word_integer = self.word_integer >> 1
        if holder:
            self.word_integer = self.word_integer | _HIGH_ORDER_BIT_WORD
            
        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.word_integer & _LOW_ORDER_BIT: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
            
    def __asl(self):
        self.word_integer = (self.word_integer << 1) & _WORD_MASK

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.word_integer & _HIGH_ORDER_BIT_WORD: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __asrb(self):
        holder = self.byte_integer & _HIGH_ORDER_BIT_BYTE
        self.byte_integer = self.byte_integer >> 1
        if holder:
            self.byte_integer = self.byte_integer | _HIGH_ORDER_BIT_BYTE

            
        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer & _LOW_ORDER_BIT: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
     
    def __aslb(self):
        self.byte_integer = (self.byte_integer << 1) & _BYTE_MASK

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
                
    def __adc(self):
        
        if self.word_integer is 0x7FFF and self.__condition_car:
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

        if self.word_integer is _WORD_MASK and self.__condition_car:
            self.__condition_car = True 
        else:
            self.__condition_car  = False
            
        # First two flag check depend on unaltered value and must be done first
        if self.__condition_car:
            self.word_integer = self.word_integer + 1

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        
    def __sbc(self):

        if self.__condition_car:
            self.word_integer = self.word_integer - 1

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.word_integer is 0 and self.__condition_car: 
            self.__condition_car  = False
        else:
            self.__condition_car  = True

        if self.word_integer is _HIGH_ORDER_BIT_WORD: 
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __adcb(self):

        if self.byte_integer is 0x7F and self.__condition_car:
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

        if self.byte_integer is _BYTE_MASK and self.__condition_car:
            self.__condition_car = True 
        else:
            self.__condition_car  = False
            
        # First two flag check depend on unaltered value and must be done first
        if self.__condition_car:
            self.byte_integer = self.byte_integer + 1

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        
    def __sbcb(self):

        if self.__condition_car:
            self.byte_integer = self.byte_integer - 1

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer is 0 and self.__condition_car: 
            self.__condition_car  = False
        else:
            self.__condition_car  = True

        if self.byte_integer is _HIGH_ORDER_BIT_BYTE: 
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __rol(self):

        holder = self.word_integer & _HIGH_ORDER_BIT_WORD
        self.word_integer = (self.word_integer << 1) & _WORD_MASK
        if holder is not 0:
            self.word_integer = self.word_integer | _LOW_ORDER_BIT
            
        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.word_integer & _HIGH_ORDER_BIT_WORD: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __ror(self):
        
        holder = self.word_integer & _LOW_ORDER_BIT
        self.word_integer = (self.word_integer >> 1) & _WORD_MASK
        if holder is not 0:
            self.word_integer = self.word_integer | _HIGH_ORDER_BIT_WORD
            
        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.word_integer & _LOW_ORDER_BIT: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

            
    def __rolb(self):

        holder = self.byte_integer & _HIGH_ORDER_BIT_BYTE
        self.byte_integer = (self.byte_integer << 1) & _BYTE_MASK
        if holder is not 0:
            self.byte_integer = self.byte_integer | _LOW_ORDER_BIT
            
        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __rorb(self):
        
        holder = self.byte_integer & _LOW_ORDER_BIT
        self.byte_integer = (self.byte_integer >> 1) & _BYTE_MASK
        if holder is not 0:
            self.byte_integer = self.byte_integer | _HIGH_ORDER_BIT_BYTE
            
        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer & _LOW_ORDER_BIT: 
            self.__condition_car  = True
        else:
            self.__condition_car  = False

        if self.__condition_car ^ self.__condition_neg: # exclusive or of condition flags
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

    def __mov(self):

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __add(self):

        holder = self.word_integer + self.word_integer_second
        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) ^ (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) is (self.word_integer & _HIGH_ORDER_BIT_WORD):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder > _WORD_MASK:
            self.__condition_car = True
        else:
            self.__condition_car = False

        self.word_integer = holder & _WORD_MASK
        
    def __sub(self):

        holder = (self.word_integer + (~self.word_integer_second + 1)) 
        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) is (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) is (self.word_integer & _HIGH_ORDER_BIT_WORD):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x10000:
            self.__condition_car = False
        else:
            self.__condition_car = True

        self.word_integer = holder & _WORD_MASK
        
    def __cmp(self):
        
        holder = self.word_integer_second + (~self.word_integer + 1)
        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) is (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) is (self.word_integer & _HIGH_ORDER_BIT):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x100:
            self.__condition_car = False
        else:
            self.__condition_car = True
        
    def __movb(self):

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __cmpb(self):
        
        holder = self.byte_integer_second + (~self.byte_integer + 1)
        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.byte_integer & _HIGH_ORDER_BIT_BYTE) is (self.byte_integer_second & _HIGH_ORDER_BIT_BYTE): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_BYTE) is (self.byte_integer & _HIGH_ORDER_BIT):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x100:
            self.__condition_car = False
        else:
            self.__condition_car = True
        
    def __bis(self):

        self.word_integer = self.word_integer | self.word_integer_second

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __bit(self):# bit does not change the destination

        holder = self.word_integer | self.word_integer_second

        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False        
        
    def __bic(self):
    
        self.word_integer = self.word_integer & ~(self.word_integer_second)

        if self.word_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
            
    def __bisb(self):

        self.byte_integer = self.byte_integer | self.byte_integer_second

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False

    def __bitb(self):

        holder = self.byte_integer | self.byte_integer_second

        if holder is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __bicb(self):
    
        self.byte_integer = self.byte_integer & ~(self.byte_integer_second)

        if self.byte_integer is 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False

    def __clc(self):
        self.__condition_car  = False
    def __clv(self):
        self.__condition_ove  = False
    def __clz(self):
        self.__condition_zer  = False
    def __cln(self):
        self.__condition_neg  = False
    def __sec(self):
        self.__condition_car  = True
    def __sev(self):
        self.__condition_ove  = True
    def __sez(self):
        self.__condition_zer  = True
    def __sen(self):
        self.__condition_neg  = True



    
# following code is to ease testing only    
# odd elements will be the MSB for the inputs on the test function
testALU = ALU

def test( stuff, ele1, ele2, ele3, ele4):
    
    elements1 = [ele1, ele2]
    elements2 = [ele3, ele4]
    ary = bytearray(elements1)
    ary2 = bytearray(elements2)

    return hex(testALU.execute(testALU, stuff, ary, ary2))
