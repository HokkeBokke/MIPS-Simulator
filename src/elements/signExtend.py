'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

class SignExtend(CPUElement):
    def __init__(self):
        # Inputs
        self.input: Value
        
        # Output
        self.output: Value = Value(0) 
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 1, 'SignExtend should have 1 input'
        
        # Inputs
        self.input: Value = inputs[0]

    def writeOutput(self):
        signBit = self.input.value >> 15
        
        if signBit == 0:
            self.output.value = self.input.value & 0xffffffff
        elif signBit == 1:
            self.output.value = 0xffff0000 | (self.input.value & 0xffff)
            
        #print("sign extended", bin(self.output.value), self.output.value)
