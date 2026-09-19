'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

class Mux(CPUElement):
    def __init__(self):
        # Inputs
        self.inputZero: Value = Value(0)
        self.inputOne: Value = Value(0)
        self.controlSignal: Value = Value(0)
        
        # Output
        self.output: Value = Value(0) 
        
    def connectInputs(self, inputs: List[Value]):
        '''
        Connect mux to input sources and controller
        
        Note that the first inputs is input zero, and the second is input 1
        '''
        assert len(inputs) == 3, 'Mux should have three inputs'
        
        # Inputs
        self.inputZero: Value = inputs[0]
        self.inputOne: Value = inputs[1]
        self.controlSignal: Value = inputs[2]

    def writeOutput(self):
        muxControl = self.controlSignal.value
        
        assert isinstance(muxControl, int)
        assert not isinstance(muxControl, bool)  # ...  (not bool)
        assert muxControl == 0 or muxControl == 1, f"Invalid mux control signal value: {muxControl}"
        
        if muxControl == 0:
            self.output.value = self.inputZero.value
        else:  # muxControl == 1
            self.output.value = self.inputOne.value
        #print(hex(self.output.value))
    
    def printOutput(self):
        '''
        Debug function that prints the output value
        '''
        print(f"mux.output = {self.output.value}")

