from elements.cpuElement import CPUElement
from common import Value, Break
from typing import List

class HazardDetection(CPUElement):
    def __init__(self):
        # Inputs
        self.IFIDRegisterRs: Value
        self.IFIDRegisterRt: Value
        self.IDEXMemRead: Value
        self.IDEXRegisterRt: Value
        self.IDEXRegisterRd: Value
        self.EXMEMRegisterDest: Value
        self.MEMWBRegisterDest: Value
        self.branch: Value
        self.breakSignal: Value
        
        # Outputs
        self.stall: Value = Value(0)
        self.PCWrite: Value = Value(1)
        self.IFIDWrite: Value = Value(0)
        self.flush: Value = Value(0)
        
        # 
        self.breakReached = False
    
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 12, "Hazard detection unit must have 12 inputs"
        
        self.IFIDRegisterRs = inputs[0]
        self.IFIDRegisterRt = inputs[1]
        self.IDEXMemRead = inputs[2]
        self.IDEXRegisterRt = inputs[3]
        self.IDEXRegisterRd = inputs[4]
        self.IDEXRegWrite = inputs[5]
        self.EXMEMRegisterDest = inputs[6]
        self.EXMEMRegWrite = inputs[7]
        self.MEMWBRegisterDest = inputs[8]
        self.MEMWBRegWrite = inputs[9]
        self.branch = inputs[10]
        self.breakSignal = inputs[11]
    
    def writeOutput(self) -> None:
        self.PCWrite.value = 1
        self.IFIDWrite.value = 1
        self.stall.value = 0
        self.flush.value = 0
        
        #print("IF/ID.rs", self.IFIDRegisterRs.value)
        #print("IF/ID.rt", self.IFIDRegisterRt.value)
        #print("ID/EX.rt", self.IDEXRegisterRt.value)
        #print("ID/EX.rd", self.IDEXRegisterRd.value)
        #print("EX/MEM.dest", self.EXMEMRegisterDest.value)
        #print("MEM/WB.dest", self.MEMWBRegisterDest.value)
        
        if self.branch.value == 1 and ((self.IDEXRegWrite.value and (self.IFIDRegisterRs.value == self.IDEXRegisterRt.value or self.IFIDRegisterRs.value == self.IDEXRegisterRd.value or self.IFIDRegisterRt.value == self.IDEXRegisterRt.value or self.IFIDRegisterRt.value == self.IDEXRegisterRd.value)) or (self.EXMEMRegWrite.value and (self.IFIDRegisterRs.value == self.EXMEMRegisterDest.value or self.IFIDRegisterRt.value == self.EXMEMRegisterDest.value)) or (self.MEMWBRegWrite.value and (self.IFIDRegisterRs.value == self.MEMWBRegisterDest.value or self.IFIDRegisterRt.value == self.MEMWBRegisterDest.value))):
            self.stall.value = 1
            self.PCWrite.value = 0
            self.IFIDWrite.value = 0
        
        if self.breakSignal.value:
            self.breakReached = True
            
        if self.breakReached:
            self.flush.value = 1
            self.IDEXRegWrite.value = 0
                        
            if not (self.IDEXRegWrite.value or self.EXMEMRegWrite.value or self.MEMWBRegWrite.value):
                raise Break("Break instruction reached")
        
