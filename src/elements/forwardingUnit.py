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
        self.need_reg2: Value
        self.ExMemDest: Value
        self.MemWbDest: Value
        
        # Output
        self.forwardA: Value = Value(0)
        self.forwardB: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.need_reg1 = inputs[0]
        self.need_reg2 = inputs[1]
        self.ExMemDest = inputs[2]
        self.MemWbDest = inputs[3]
    
    def writeOutput(self) -> None:
        self.forwardA.value = forwardSrc["idex"]
        self.forwardB.value = forwardSrc["idex"]
        
        print("ID/EX rs", self.need_reg1.value)
        print("ID/EX rt", self.need_reg2.value)
        print("EX/MEM rd", self.ExMemDest.value)
        
        if self.need_reg1.value == self.ExMemDest.value:
            self.forwardA.value = forwardSrc["exmem"]
            
        if self.need_reg1.value == self.MemWbDest.value:
            self.forwardA.value = forwardSrc["memwb"]
            
        if self.need_reg2.value == self.ExMemDest.value:
            self.forwardB.value = forwardSrc["exmem"]
            
        if self.need_reg2.value == self.MemWbDest.value:
            self.forwardB.value = forwardSrc["memwb"]
            
        print("Forwarding signal", self.forwardA.value, self.forwardB.value)