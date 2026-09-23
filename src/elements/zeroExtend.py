from typing import List

from elements.cpuElement import CPUElement
from common import Value

class ZeroExtend(CPUElement):
    def __init__(self) -> None:
        # Input
        self.input = Value(0)
        
        # Output
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.input = inputs[0]
        
    def writeOutput(self) -> None:
        self.output.value = (self.input.value & 0xffff) | 0x00000000
        
        #print("zero extended", bin(self.output.value), self.output.value)