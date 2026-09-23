from typing import List

from elements.cpuElement import CPUElement
from common import Value

class NotGate(CPUElement):
    def __init__(self) -> None:
        # Inputs
        self.input = Value(0)
        
        # Output
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.input = inputs[0]
        
    def writeOutput(self) -> None:
        self.output.value = not self.input.value