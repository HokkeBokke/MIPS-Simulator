from elements.cpuElement import CPUElement
from common import Value
from typing import List

class HazardDetection(CPUElement):
    def __init__(self):
        # Inputs
        self.IDEXMemRead: Value
        self.IDEXRegisterRt: Value
        self.IFIDRegisterRs: Value
        self.IFIDRegisterRt: Value
        
        # Outputs
        self.nopWrite: Value = Value(0)
        self.PCWrite: Value = Value(0)
        self.IFIDWrite: Value = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        self.IDEXMemRead = inputs[0]
        self.IDEXRegisterRt = inputs[1]
        self.IFIDRegisterRs = inputs[2]
        self.IFIDRegisterRt = inputs[3]
    
    def writeOutput(self) -> None:
        self.PCWrite.value = 1
        
        if self.IDEXMemRead.value and ((self.IDEXRegisterRt.value == self.IFIDRegisterRs.value) or (self.IDEXRegisterRt.value == self.IFIDRegisterRt.value)):
            self.nopWrite.value = 1
            self.PCWrite.value = 0
            
        
