

import math
    
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

DEBUG_ON = False

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

    word_integer = primary[0]*256 + primary[1]
    byte_integer = primary[1]
    
    word_integer_second = secondary[0]*256 + secondary[1]
    byte_integer_second = secondary[1]

    mod = 0
    
    def execute(self, mnemonic, operand1 = primary, operand2 = secondary, modifier = 0):
        
        self.mod = modifier

        self.word_integer = operand1[0]*256 + operand1[1]
        self.byte_integer = operand1[1]
    
        self.word_integer_second = operand2[0]*256 + operand2[1]
        self.byte_integer_second = operand2[1]

        #converting the mnemonic to lowercase reduce case sensitivity 
        mnem_lower = mnemonic.lower()

        # Single operand instructions
        if mnem_lower == 'dec':
            self.__dec(self)
        elif mnem_lower == 'clr':
            self.__clr(self)
        elif mnem_lower == 'inc':
            self.__inc(self)
        elif mnem_lower == 'neg':
            self.__neg(self)
        elif mnem_lower == 'tst':
            self.__tst(self)
        elif mnem_lower == 'com':
            self.__com(self)
        elif mnem_lower == 'asr':
            self.__asr(self)
        elif mnem_lower == 'asl':
            self.__asl(self)
        elif mnem_lower == 'adc':
            self.__adc(self)
        elif mnem_lower == 'sbc':
            self.__sbc(self)
        elif mnem_lower == 'rol':
            self.__rol(self)
        elif mnem_lower == 'ror':
            self.__ror(self)
        elif mnem_lower == 'swab':
            self.word_integer = operand1[1]*256 + operand1[0] # Just re-initialized on reverse order
            self.__swab(self)
        # From here on out I have to re-initialize since the functions will only use the last byte

        elif mnem_lower == 'decb':
            self.__decb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'clrb':
            self.__clrb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'incb':
            self.__incb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'negb':
            self.__negb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'tstb':
            self.__tstb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'comb':
            self.__comb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'asrb':
            self.__asrb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'aslb':
            self.__aslb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'adcb':
            self.__adcb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'sbcb':
            self.__sbcb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'rolb':
            self.__rolb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'rorb':
            self.__rorb(self)
            self.word_integer = primary[0]*16 + byte_integer

        # Double operand instructions

        elif mnem_lower == 'add':
            self.__add(self)
        elif mnem_lower == 'mov':
            self.__mov(self)
        elif mnem_lower == 'sub':
            self.__sub(self)
        elif mnem_lower == 'cmp':
            self.__cmp(self)
        elif mnem_lower == 'bis':
            self.__bis(self)
        elif mnem_lower == 'bit':
            self.__bit(self)
        elif mnem_lower == 'bic':
            self.__bic(self)

        # From here on out I have to re-initialize word_integer, since the functions will only use the last byte
      
        elif mnem_lower == 'cmpb':
            self.__cmpb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'bisb':
            self.__bisb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'bitb':
            self.__bitb(self)
            self.word_integer = primary[0]*16 + byte_integer
        elif mnem_lower == 'bicb':
            self.__bicb(self)
            self.word_integer = primary[0]*16 + byte_integer

        # The final section is for Condition code operators
        elif mnem_lower == 'clc':
            self.__clc(self)
        elif mnem_lower == 'clv':
            self.__clv(self)
        elif mnem_lower == 'clz':
            self.__clz(self)
        elif mnem_lower == 'cln':
            self.__cln(self)
        elif mnem_lower == 'sec':
            self.__sec(self)
        elif mnem_lower == 'sev':
            self.__sev(self)
        elif mnem_lower == 'sez':
            self.__sez(self)
        elif mnem_lower == 'sen':
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
        self.word_integer = 0
        
        self.__condition_zer  = True
        self.__condition_neg  = False
        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __dec(self):
        self.word_integer = (self.word_integer -1) & _WORD_MASK

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer == 0x7FFF: 
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
        
    def __inc(self):

        self.word_integer = (self.word_integer + 1) & _WORD_MASK

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer == _HIGH_ORDER_BIT_WORD: 
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __neg(self):

        self.word_integer = (~self.word_integer + 1 ) & _WORD_MASK # Two's compliment negate
            
        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.word_integer == _HIGH_ORDER_BIT_WORD:
            self.__condition_ove = True 
        else:
            self.__condition_ove = False

        if self.word_integer == 0: 
            self.__condition_car = False 
        else:
            self.__condition_car = True
        
    def __tst(self):

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __com(self):

        self.word_integer = (~self.word_integer) & _WORD_MASK

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        self.__condition_ove  = False
        self.__condition_car  = True

    def __clrb(self):
        self.byte_integer = 0

        self.__condition_zer  = True
        self.__condition_neg  = False
        self.__condition_ove  = False
        self.__condition_car  = False
        
    def __decb(self):

        self.byte_integer = self.byte_integer - 1

        if self.byte_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer == 31:
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __incb(self):

        self.byte_integer = self.byte_integer + 1

        if self.byte_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer < 0:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer == 31:
            self.__condition_ove = True 
        else:
            self.__condition_ove = False
            
    def __negb(self):
        if self.byte_integer < _HIGH_ORDER_BIT_BYTE:
            self.byte_integer = (~self.byte_integer + 1 ) # Two's compliment negate
        else:
            self.byte_integer = _HIGH_ORDER_BIT_BYTE
        
        if self.byte_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
            
        if self.byte_integer == _HIGH_ORDER_BIT_BYTE: # again that is in octal binary 1000 0000
            self.__condition_ove = True 
        else:
            self.__condition_ove = False

        if self.byte_integer == 0: # again that is in octal
            self.__condition_car = False 
        else:
            self.__condition_car = True
        
    def __tstb(self):

        if self.byte_integer == 0: 
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

        if self.byte_integer == 0: 
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
            
        if self.word_integer == 0: 
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

        if self.word_integer == 0: 
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

            
        if self.byte_integer == 0: 
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

        if self.byte_integer == 0: 
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

        holder = self.word_integer

        if self.__condition_car:
            self.word_integer = (self.word_integer + 1) & _WORD_MASK

        if holder == 0x7FFF and self.__condition_car:
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

        if holder == _WORD_MASK and self.__condition_car:
            self.__condition_car = True 
        else:
            self.__condition_car  = False
        
        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        
    def __sbc(self):

        if self.__condition_car:
            self.word_integer = (self.word_integer - 1) & _WORD_MASK

        if self.word_integer  == _HIGH_ORDER_BIT_WORD:
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

        if self.word_integer == 0 and self.__condition_car:
            self.__condition_car = True 
        else:
            self.__condition_car  = False
        
        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
    def __adcb(self):

        if self.byte_integer == 0x7F and self.__condition_car:
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False

        if self.byte_integer == _BYTE_MASK and self.__condition_car:
            self.__condition_car = True 
        else:
            self.__condition_car  = False
            
        # First two flag check depend on unaltered value and must be done first
        if self.__condition_car:
            self.byte_integer = self.byte_integer + 1

        if self.byte_integer == 0: 
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

        if self.byte_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.byte_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        if self.byte_integer == 0 and self.__condition_car: 
            self.__condition_car  = False
        else:
            self.__condition_car  = True

        if self.byte_integer == _HIGH_ORDER_BIT_BYTE: 
            self.__condition_ove  = True
        else:
            self.__condition_ove  = False
        
    def __rol(self):

        holder = self.word_integer & _HIGH_ORDER_BIT_WORD
        self.word_integer = (self.word_integer << 1) & _WORD_MASK
        if holder:
            self.word_integer = self.word_integer | _LOW_ORDER_BIT
            
        if self.word_integer == 0: 
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
        if holder:
            self.word_integer = self.word_integer | _HIGH_ORDER_BIT_WORD
            
        if self.word_integer == 0: 
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
        if holder:
            self.byte_integer = self.byte_integer | _LOW_ORDER_BIT
            
        if self.byte_integer == 0: 
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
        if holder:
            self.byte_integer = self.byte_integer | _HIGH_ORDER_BIT_BYTE
            
        if self.byte_integer == 0: 
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

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False

    def __swab(self):

        if (self.word_integer & _BYTE_MASK) == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove = False
        self.__condition_car = False

        
    def __add(self):

        holder = self.word_integer + self.word_integer_second
        if holder == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) ^ (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) == (self.word_integer & _HIGH_ORDER_BIT_WORD):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder > _WORD_MASK:
            self.__condition_car = True
        else:
            self.__condition_car = False

        self.word_integer = holder & _WORD_MASK
        
    def __sub(self):

        holder = (self.word_integer + ((~self.word_integer_second + 1) & _WORD_MASK))
        if holder & _WORD_MASK == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) == (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) == (self.word_integer & _HIGH_ORDER_BIT_WORD):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x10000:
            self.__condition_car = False
        else:
            self.__condition_car = True

        self.word_integer = holder & _WORD_MASK
        
    def __cmp(self):

        holder = (self.word_integer_second + ((~self.word_integer + 1) & _WORD_MASK)) 
        if holder == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.word_integer & _HIGH_ORDER_BIT_WORD) == (self.word_integer_second & _HIGH_ORDER_BIT_WORD): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_WORD) == (self.word_integer & _HIGH_ORDER_BIT_WORD):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x10000:
            self.__condition_car = False
        else:
            self.__condition_car = True
        
    def __movb(self):

        if self.byte_integer == 0: 
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
        if holder == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False

        if (self.byte_integer & _HIGH_ORDER_BIT_BYTE) == (self.byte_integer_second & _HIGH_ORDER_BIT_BYTE): 
            self.__condition_ove  = False
        elif (holder & _HIGH_ORDER_BIT_BYTE) == (self.byte_integer & _HIGH_ORDER_BIT):
            self.__condition_ove  = False
        else:
            self.__condition_ove = True

        if holder & 0x100:
            self.__condition_car = False
        else:
            self.__condition_car = True
        
    def __bis(self):

        self.word_integer = self.word_integer | self.word_integer_second

        if self.word_integer == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if self.word_integer & _HIGH_ORDER_BIT_WORD:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __bit(self):# bit does not change the destination

        holder = self.word_integer & self.word_integer_second

        if DEBUG_ON:
            print('result->',hex(holder), end='\t') #for testing
        
        if holder == 0: 
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
        
        if self.word_integer == 0: 
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

        if self.byte_integer == 0: 
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

        if DEBUG_ON:
            print(hex(holder)) #for testing
        
        if holder == 0: 
            self.__condition_zer = True
        else:
            self.__condition_zer = False
            
        if holder & _HIGH_ORDER_BIT_BYTE:
            self.__condition_neg = True
        else:
            self.__condition_neg = False
        
        self.__condition_ove  = False
        
    def __bicb(self):
    
        self.byte_integer = (self.byte_integer & ~(self.byte_integer_second)) & _BYTE_MASK

        if self.byte_integer == 0: 
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

    #print('\tout_hex:', format(testALU.execute(testALU, stuff, ary, ary2), '04X'), "\tout_decimal:", format(testALU.execute(testALU, stuff, ary, ary2),'05d'),'\tcondition codes NZVC :', testALU.get_condition(testALU))

    print('\tout_hex:', format(testALU.execute(testALU, stuff, ary, ary2), '04X'), '\t\tcondition codes NZVC :', testALU.get_condition(testALU))
    
instructionsOneOperand = ['clr', 'dec', 'inc', 'neg', 'tst', 'com', 'asr', 'asl', 'adc', 'sbc', 'rol', 'ror', 'swab'] 
instructionsTwoOperand = ['mov', 'add', 'sub', 'cmp', 'bis', 'bit', 'bic']   

def testBench():

    global DEBUG_ON
    #DEBUG_ON = False

    print('\n------------ Double Operand Instructions ----------\n')
    
    for i in instructionsTwoOperand:

        print('-------------------------------------------------------------------------------')

        print(i, '0x00FF 0xFF02 ', end ='->')
        test(i,0x00, 0xFF, 0xFF, 0x02) 

        print(i, '0x7FFF 0x8002 ', end ='->')
        test(i,0x7F, 0xFF, 0x80, 0x02) 

        print('-------------------------------------------------------------------------------')

        print(i, '0x00FF 0x00F2 ', end ='->')
        test(i,0x00, 0xFF, 0x00, 0xF2) 
        
        print(i, '0x7FFF 0x7FF0 ', end ='->')
        test(i,0x7F, 0xFF, 0x7F, 0xF0) 

        print('-------------------------------------------------------------------------------')
    
        print(i, '0xFF00 0x00FF ', end ='->')
        test(i,0xFF, 0x00, 0x00, 0xFF) 

        print(i, '0x8000 0x7FFF ', end ='->')
        test(i,0x80, 0x00, 0x7F, 0xFF) 

        print('-------------------------------------------------------------------------------')

        print(i, '0xFF01 0xFF04 ', end ='->')
        test(i,0xFF, 0x01, 0xFF, 0x04) 

        print(i, '0x8000 0x8002 ', end ='->')
        test(i,0x80, 0x00, 0x80, 0x02) 

        print('-------------------------------------------------------------------------------')

        print(i, '0x00FF 0x00FF ', end ='->')
        test(i,0x00, 0xFF, 0x00, 0xFF) 

        print(i, '0x00FF 0x0000 ', end ='->')
        test(i,0x00, 0xFF, 0x00, 0x00) 

        print('-------------------------------------------------------------------------------')

        print(i, '0xFF02 0x0000 ', end ='->')
        test(i,0xFF, 0x02, 0x00, 0x00) 

        print(i, '0x0000 0x0000 ', end ='->')
        test(i,0x00, 0x00, 0x00, 0x00) 

        testALU.execute(testALU, 'clr')

    print('-------------------------------------------------------------------------------')
    
    print('\n------------ Single Operand Instructions ----------\n')
    for j in instructionsOneOperand:

        print('-------------------------------------------------------------------------------')

        print(j, '0xFF00', end ='->')
        test(j,0xFF, 0x00, 0x00, 0x00) 
    
        print(j, '0x00FF', end ='->')
        test(j,0x00, 0xFF, 0x00, 0x00) 

        print(j, '0x0000', end ='->')
        test(j,0x00, 0x00, 0x00, 0x00) 
    
