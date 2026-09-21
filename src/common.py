'''This file contains small utility functions for MIPS simulator.

Code written for inf-2200, University of Tromso
Author: Erlend Graff <erlend.h.graff@uit.no>
'''

# Number conversion function
# Used by ALU slt operation and debug print to display correct numbers
def fromUnsignedWordToSignedWord(num):
    # Python hack to convert from 32 bit unsigned value to signed (using 2's complement)
    # Tests if the most significant bit (sign bit) at position 31 is present,
    # and if so, convert to negative value according to 2's complement representation
    return num if not (num & 0x80000000) else -(((~num) & 0xffffffff) + 1)
  

def fromSignedWordToUnsignedWord(num):
    # Convert signed 32 bit (using 2's complement) to unsigned value
    # This is simply done by removing trailing sign bits, and replacing
    # them with zeros. Since a 32 bit integer is not represented using
    # 32 bits in python, this automatically renders the value "unsigned".
    return num & 0xffffffff

def printInstructionFormat(instr: int):
    '''
    Utility function to prints the different fields of an instruction in user-friendly manner 
    '''
    print(f"""
        opcode:    {bin(instr >> 26 & 0x3f)[2:].zfill(6)},
        rs:        {bin(instr >> 21 & 0x1f)[2:].zfill(5)},
        rt:        {bin(instr >> 16 & 0x1f)[2:].zfill(5)},
        rd:        {bin(instr >> 11 & 0x1f)[2:].zfill(5)},
        shamt:     {bin(instr >> 6  & 0x1f)[2:].zfill(5)},
        funct:     {bin(instr       & 0x3f)[2:].zfill(6)},
        imm:       {bin(instr       & 0xffff)[2:].zfill(16)},
        jump_addr: {bin(instr       & 0x3ffffff)[2:].zfill(26)},
    """)

class Value:
    def __init__(self, value: int):
        self.value = value

class Break(Exception):
    def __init__(self, message):
        self.message = message

class Overflow(Exception):
    def __init__(self, message):
        self.message = message
        
class MemoryAccessError(Exception):
    def __init__(self, message):
        self.message = message
