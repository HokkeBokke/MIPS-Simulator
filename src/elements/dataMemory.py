'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from elements.memory import Memory
from common import Value

class DataMemory(Memory):
    def __init__(self, filename: str):
        Memory.__init__(self, filename)
        
        self.incomingAddress: Value
        self.outgoingData: Value
        
    def connectInputs(self, inputs: list[Value]):
        assert len(inputs) == 1, "InstructionMemory should have 1 input"
        
        self.incomingAddress = inputs[0]
    
    def writeOutput(self):
        self.outgoingData = self.memory[self.incomingAddress.value]
