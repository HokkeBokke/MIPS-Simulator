'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from elements.memory import Memory
from common import Value, MemoryAccessError

class DataMemory(Memory):
    def __init__(self, filename: str):
        Memory.__init__(self, filename)
        
        self.incomingAddress = Value(0)
        self.write_data = Value(0)
        self.MemWriteSignal = Value(0)
        self.MemReadSignal = Value(0)
        
        self.outgoingData = Value(0)
        
    def connectInputs(self, inputs: list[Value]):
        assert len(inputs) == 4, "DataMemory should have 4 input"
        
        self.incomingAddress = inputs[0]
        self.write_data = inputs[1]
        self.MemWriteSignal = inputs[2]
        self.MemReadSignal = inputs[3]
    
    def writeOutput(self):
        if self.MemReadSignal.value == 1:
            if self.incomingAddress.value not in self.memory:
                self.outgoingData.value = 0
                return
            
            self.outgoingData.value = self.memory[self.incomingAddress.value]
            
        if self.MemWriteSignal.value == 1:
            self.memory[self.incomingAddress.value] = self.write_data.value
        
