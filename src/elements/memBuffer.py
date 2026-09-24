'''
Code written for inf-2200, University of Tromso
'''

from common import Value
from elements.cpuElement import CPUElement
from typing import List

class FetchBuffer(CPUElement):
    def __init__(self):
        self.in_pc: Value
        self.out_pc = Value(0)
        
        self.in_instruction: Value
        self.out_instruction = Value(0)

    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 2, f'FetchBuffer should have 2 inputs'
        
        self.in_pc = inputs[0]
        self.in_instruction = inputs[1]
        
    def writeOutput(self):
        self.out_pc.value = self.in_pc.value
        self.out_instruction.value = self.in_instruction.value
