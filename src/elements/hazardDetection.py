from elements.cpuElement import CPUElement
from common import Value
from typing import List

class HazardDetection(CPUElement):
    def __init__(self):
        # Inputs
        self.IDEXMemRead: Value
        self.IDEXRegisterRt: Value
        self.instruction: Value
        
        # Outputs
        self.stall: Value = Value(0)
        self.PCWrite: Value = Value(1)
        self.IFIDWrite: Value = Value(0)
        self.flush: Value = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        self.IDEXMemRead = inputs[0]
        self.IDEXRegisterRt = inputs[1]
        self.instruction = inputs[2]
    
    def writeOutput(self) -> None:
        self.PCWrite.value = 1
        IFIDRegisterRt = self.instruction.value & (0b11111 << 16)
        IFIDRegisterRs = self.instruction.value & (0b11111 << (16 + 5))
        
        if self.IDEXMemRead.value and ((self.IDEXRegisterRt.value == IFIDRegisterRs) or (self.IDEXRegisterRt.value == IFIDRegisterRt)):
            self.stall.value = 1
            self.PCWrite.value = 0
        
        

