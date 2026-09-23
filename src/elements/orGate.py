from typing import List

from elements.cpuElement import CPUElement
from common import Value

class OrGate(CPUElement):
    def __init__(self) -> None:
        # Inputs
        self.input_a = Value(0)
        self.input_b = Value(0)
        
        # Output
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.input_a = inputs[0]
        self.input_b = inputs[1]
        
    def writeOutput(self) -> None:
        self.output.value = self.input_a.value | self.input_b.value
        print(f"bne: {self.input_a.value}, beq: {self.input_b.value}")
        print("branch?", self.output.value)