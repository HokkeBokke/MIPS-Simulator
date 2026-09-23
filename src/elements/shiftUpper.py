from typing import List

from elements.cpuElement import CPUElement
from common import Value

class ShiftUpper(CPUElement):
    def __init__(self):
        # Input
        self.input = Value(0)
        
        # Output
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.input = inputs[0]
        
    def writeOutput(self) -> None:
        self.output.value = self.input.value << 16
        
        #print("shift upper", bin(self.output.value), self.output.value)
