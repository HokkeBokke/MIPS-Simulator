from typing import List

from elements.cpuElement import CPUElement
from common import Value

class BitFilter(CPUElement):
    def __init__(self, start, end):
        if start > end:
            start, end = end, start
        self.range = start, end
        # Input
        self.incomingBits = Value(0)
        
        # Output
        self.filteredBits = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.incomingBits = inputs[0]
        
    def writeOutput(self) -> None:
        zeroed = (self.incomingBits.value >> self.range[0])
        mask = ((1 << (self.range[1] - self.range[0] + 1)) - 1)
        #print("bits", self.range)
        #print(f"mask: {bin(mask)} ({hex(mask)})")
        #print("value:", zeroed & mask)
        self.filteredBits.value = zeroed & mask
