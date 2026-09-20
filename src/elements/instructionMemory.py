'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from elements.memory import Memory
from common import Value

class InstructionMemory(Memory):
    def __init__(self, filename: str):
        Memory.__init__(self, filename)
        
        self.incomingAddress: Value = Value(0)
        self.outgoingInstruction: Value = Value(0)
    
    def connectInputs(self, inputs: list[Value]):
        assert len(inputs) == 1, "InstructionMemory should have 1 input"
        
        self.incomingAddress = inputs[0] # read address
    
    def writeOutput(self):
        print(self.incomingAddress.value, self.memory)
        self.outgoingInstruction = self.memory[self.incomingAddress.value]