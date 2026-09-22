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
        print(self.input.value)
        signBit = self.input.value >> 15
        print(self.input.value)
        print("negative" if signBit == 1 else "positive")
        
        if signBit == 0:
            self.output.value = self.input.value & 0xffffffff
        elif signBit == 1:
            self.output.value = ((1 << 32) - 1) | (self.input.value & 0xffff)
            
        print(bin(self.output.value), self.output.value)
