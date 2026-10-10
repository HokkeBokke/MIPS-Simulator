from elements.cpuElement import CPUElement
from common import Value
from typing import List

forwardSrc = {
    "idex": 0b00,
    "exmem": 0b10,
    "memwb": 0b01
}

class ForwardingUnit(CPUElement):
    def __init__(self):
        # Input
        self.need_reg1: Value
        self.need_reg3: Value
        self.ExMemResult: Value
        self.MemWbResult: Value
        
        # Output
        self.forwardA: Value = Value(0)
        self.forwardB: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.need_reg1 = inputs[0]
        self.need_reg2 = inputs[1]
        self.ExMemResult = inputs[2]
        self.MemWbResult = inputs[3]
    
    def writeOutput(self) -> None:
        self.forwardA.value = forwardSrc["idex"]
        self.forwardB.value = forwardSrc["idex"]
        
        if self.need_reg1 == self.ExMemResult:
            self.forwardA.value = forwardSrc["exmem"]
            
        if self.need_reg1 == self.MemWbResult:
            self.forwardA.value = forwardSrc["memwb"]
            
        if self.need_reg2 == self.ExMemResult:
            self.forwardB.value = forwardSrc["exmem"]
            
        if self.need_reg2 == self.MemWbResult:
            self.forwardB.value = forwardSrc["memwb"]