'''
Code written for inf-2200, University of Tromso
'''

from common import Value
from elements.cpuElement import CPUElement
from typing import List

class PC(CPUElement):
    def __init__(self, baseaddr: int):
        # Input
        self.incomingAddress: Value = Value(0)
        self.incomingAddress.value = baseaddr
        
        # Output
        self.currentAddress: Value = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 1, 'PC should have one input'
        
        # Input
        next = self.incomingAddress.value
        self.incomingAddress = inputs[0]
        self.incomingAddress.value = next
        
    def writeOutput (self):
        # pc is updated by the input source
        self.currentAddress.value = self.incomingAddress.value
