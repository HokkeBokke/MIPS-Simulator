'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

class CombineBits(CPUElement):
    '''
    Combine specified bits from two values into one value
    '''
    def __init__(self, bits1: range, bits2: range):
        self.bitmask1 = ((1 << len(bits1)) - 1) << bits1.start
        self.bitmask2 = ((1 << len(bits2)) - 1) << bits2.start
        
         # Input
        self.input1: Value
        self.input2: Value
                
        # Output
        self.output: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 2, 'CombineBits requires 2 inputs'
        
        self.input1 = inputs[0]
        self.input2 = inputs[1]
        
    def writeOutput(self):
        self.output.value = (self.input1.value & self.bitmask1) | (self.input2.value & self.bitmask2)
                
                
