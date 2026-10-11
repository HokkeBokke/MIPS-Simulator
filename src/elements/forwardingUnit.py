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
        self.ExMemRegWrite: Value
        self.ExMemDest: Value
        self.MemWbRegWrite: Value
        self.MemWbDest: Value
        
        # Output
        self.forwardA: Value = Value(0)
        self.forwardB: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.need_reg1 = inputs[0]
        self.need_reg2 = inputs[1]
        self.ExMemRegWrite = inputs[2]
        self.ExMemDest = inputs[3]
        self.MemWbRegWrite = inputs[4]
        self.MemWbDest = inputs[5]
    
    def writeOutput(self) -> None:
        self.forwardA.value = forwardSrc["idex"]
        self.forwardB.value = forwardSrc["idex"]
        
        if self.ExMemRegWrite.value and self.ExMemDest.value != 0 and self.need_reg1.value == self.ExMemDest.value:
            self.forwardA.value = forwardSrc["exmem"]
            
        if self.ExMemRegWrite.value and self.ExMemDest.value != 0 and self.need_reg2.value == self.ExMemDest.value:
            self.forwardB.value = forwardSrc["exmem"]

        if self.MemWbRegWrite.value and self.MemWbDest.value != 0 \
            and not (self.ExMemRegWrite.value and (self.ExMemDest.value != 0) \
            and (self.ExMemDest.value == self.need_reg1.value)) \
            and (self.need_reg1.value == self.MemWbDest.value):
            self.forwardA.value = forwardSrc["memwb"]

        if self.MemWbRegWrite.value and self.MemWbDest.value != 0 \
            and not (self.ExMemRegWrite.value and self.ExMemDest.value != 0 \
            and (self.ExMemDest.value == self.need_reg2.value)) \
            and (self.need_reg2.value == self.MemWbDest.value):
            self.forwardB.value = forwardSrc["memwb"]