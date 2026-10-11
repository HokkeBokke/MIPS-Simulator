from typing import List
from elements.cpuElement import CPUElement
from common import Value

class EqualityComparator(CPUElement):
    def __init__(self):
        # Inputs
        self.value_a: Value
        self.value_b: Value
        
        # Output
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.value_a = inputs[0]
        self.value_b = inputs[1]
        
    def writeOutput(self) -> None:
        self.output.value = 0
        
        #print("eq cmp:", self.value_a.value, self.value_b.value)
        if self.value_a.value == self.value_b.value:
            self.output.value = 1
