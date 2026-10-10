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
        self.Rs: Value
        self.Rt: Value
        self.EXMEMRd: Value
        self.MEMWBRd: Value
        
        # Output
        self.forwardA: Value = Value(0)
        self.forwardB: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.Rs = inputs[0]
        self.Rt = inputs[1]
        self.EXMEMRd = inputs[2]
        self.MEMWBRd = inputs[3]
    
    def writeOutput(self) -> None:
        self.forwardA.value = forwardSrc["idex"]
        self.forwardB.value = forwardSrc["idex"]
        
        if self.Rs == self.EXMEMRd:
            self.forwardA.value = forwardSrc["exmem"]
            
        if self.Rs == self.MEMWBRd:
            self.forwardA.value = forwardSrc["memwb"]
            
        if self.Rt == self.EXMEMRd:
            self.forwardB.value = forwardSrc["exmem"]
            
        if self.Rt == self.MEMWBRd:
            self.forwardB.value = forwardSrc["memwb"]