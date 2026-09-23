'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

class Mux(CPUElement):
    def __init__(self, numInputs):
        # Inputs
        self.inputs: list[Value] = []
        self.numInputs: int = numInputs
        self.controlSignal: Value = Value(0)
        
        # Output
        self.output: Value = Value(0) 
        
    def connectInputs(self, inputs: List[Value]):
        '''
        Connect mux to input sources and controller
        
        Note that the first inputs is input zero, and the second is input 1 >UPDATE THIS
        '''
        assert len(inputs)-1 == self.numInputs, 'Number of inputs must match'
        
        # Inputs
        self.numInputs = self.numInputs
        self.inputs: list[Value] = inputs[0:self.numInputs]
        self.controlSignal: Value = inputs[self.numInputs]

    def writeOutput(self):
        muxControl = self.controlSignal.value
        
        assert isinstance(muxControl, int)
        assert not isinstance(muxControl, bool)  # ...  (not bool)
        assert muxControl in range(0,self.numInputs+1), f"Invalid mux control signal value: {muxControl}"
        
        self.output.value = self.inputs[self.controlSignal.value].value
    
    def printOutput(self):
        '''
        Debug function that prints the output value
        '''
        print(f"mux.output = {self.output.value}")

