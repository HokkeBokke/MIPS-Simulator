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
        self.PCWrite: Value
        
        # Output
        self.currentAddress: Value = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 2, 'PC should have two input'
        
        # Input
        #print("input:", self.incomingAddress.value)
        next = self.incomingAddress.value
        self.incomingAddress = inputs[0]
        self.incomingAddress.value = next
        #print("input:", self.incomingAddress.value)
        self.PCWrite = inputs[1]
        
    def writeOutput (self):
        # pc is updated by the input source
        print("PCWRITE:", self.PCWrite.value)
        if self.PCWrite.value:
            print("pc update:", hex(self.currentAddress.value), "=>", hex(self.incomingAddress.value))
            self.currentAddress.value = self.incomingAddress.value
            
        print("PC: ", hex(self.currentAddress.value))
