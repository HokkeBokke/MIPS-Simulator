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
        self.output.value = (signBit << 31) | (self.input.value & 0b111111111111111)

