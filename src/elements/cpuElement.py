'''
Implements base class from which all CPU elements inherit.

Code written for inf-2200, University of Tromso
'''
from typing import List
from common import Value

class CPUElement:
    '''
    Superclass for all elements in the datapath
    '''    
    
    def connectInputs(self, inputs: List[Value]):
        '''
        Connect the CPUElement to another CPUElement. This function is called once per CPU Element instance during simulator initialization.
        
        @param input: List of input sources. A source is a field defined in the other CPUElement class
        '''
        pass
    
    def writeOutput(self) -> None:
        '''
        Set output values based on input values and control signals
        
        This function is called once for each simulation step.
        '''
        raise AssertionError(f"writeOutput must be implemented by CPU Element {repr(self)}")
    
    def __str__(self):
        '''
        Returns the name of the class and its fields
        '''
        v = {field: hex(value.value) for field, value in self.__dict__.items()}
        return f"{self.__class__.__name__} {v}"
