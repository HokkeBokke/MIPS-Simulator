from common import Value
from elements.cpuElement import CPUElement
from typing import List

class ShiftLeft2(CPUElement):
    def __init__(self):
        # Inputs
        self.input: Value = Value(0)
        
        # Output
        self.result = Value(0)

    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 1, 'Shifte left should have one inputs'
        
        # Inputs
        self.value_a = inputs[0]
        
    def writeOutput(self):
        # Output values
        assert isinstance(self.value_a.value, int)
        self.result.value = (self.value_a.value << 2) & 0xffffffff # Convert to 32-bit (ignore overflow)
