'''
Code written for inf-2200, University of Tromso
'''

from common import Value
from elements.cpuElement import CPUElement
from typing import List

class FetchBuffer(CPUElement):
    def __init__(self):
        self.IFIDWrite: Value
        
        self.in_pc: Value
        self.out_pc = Value(0)
        
        self.in_instruction: Value
        self.out_instruction = Value(0)

    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 4, 'FetchBuffer should have 4 inputs'
        
        self.in_pc = inputs[0]
        self.in_instruction = inputs[1]
        self.bubble = inputs[2]
        self.IFIDWrite = inputs[3]
        
    def writeOutput(self):
        print("bubble:", self.bubble.value)
        if self.bubble.value == 1:
            self.out_instruction.value = 0
        if self.IFIDWrite.value == 0:
            return
        else:
            self.out_pc.value = self.in_pc.value
            self.out_instruction.value = self.in_instruction.value
        
    def dump(self):
        print(f"""fetch buffer:
=========
(pc)    {hex(self.in_pc.value)} => {hex(self.out_pc.value)}
(inst)  {hex(self.in_instruction.value)} => {hex(self.out_instruction.value)}
=========

""")
        
    
class DecodeBuffer(CPUElement):
    def __init__(self):
        # Output
        self.out_PCSrc = Value(0)
        self.out_Branch = Value(0)
        self.out_Jump = Value(0)
        self.out_RegWrite = Value(0)
        self.out_RegDst = Value(0)
        self.out_ALUSrc = Value(0)
        self.out_ALUOp = Value(0)
        self.out_MemRead = Value(0)
        self.out_MemWrite = Value(0)
        self.out_MemtoReg = Value(0)
        self.out_ExtOp = Value(0)
        self.out_add4toPC = Value(0)
        self.out_readData1 = Value(0)
        self.out_readData2 = Value(0)
        self.out_signExtend = Value(0)
        self.out_readReg1BitFilter = Value(0)
        self.out_readReg2BitFilter = Value(0)
        self.out_writeRegBitFilter = Value(0)
        self.out_funct = Value(0)
        
        
    def connectInputs(self, inputs: List[Value]):
        self.in_controlSignals = inputs[0]
        self.in_readData1 = inputs[1]
        self.in_readData2 = inputs[2]
        self.in_signExtend = inputs[3]
        self.in_readReg1BitFilter = inputs[4]
        self.in_readReg2BitFilter = inputs[5]
        self.in_writeRegBitFilter = inputs[6]
        self.in_funct = inputs[7]
    
    def writeOutput(self):
        self.out_PCSrc.value = (self.in_controlSignals.value >> 13) & 0b11
        self.out_Branch.value = (self.in_controlSignals.value >> 11) & 0b11
        self.out_Jump.value = (self.in_controlSignals.value >> 10) & 1
        self.out_RegWrite.value = (self.in_controlSignals.value >> 9) & 1
        self.out_RegDst.value = (self.in_controlSignals.value >> 8) & 1
        self.out_ALUSrc.value = (self.in_controlSignals.value >> 7) & 1
        self.out_ALUOp.value = (self.in_controlSignals.value >> 5) & 0b11
        self.out_MemRead.value = (self.in_controlSignals.value >> 4) & 1
        self.out_MemWrite.value = (self.in_controlSignals.value >> 3) & 1
        self.out_MemtoReg.value = (self.in_controlSignals.value >> 2) & 1
        self.out_ExtOp.value = self.in_controlSignals.value & 0b11
        self.out_readData1.value = self.in_readData1.value
        self.out_readData2.value = self.in_readData2.value
        self.out_signExtend.value = self.in_signExtend.value
        self.out_readReg1BitFilter.value = self.in_readReg1BitFilter.value
        self.out_readReg2BitFilter.value = self.in_readReg2BitFilter.value
        self.out_writeRegBitFilter.value = self.in_writeRegBitFilter.value
        self.out_funct.value = self.in_funct.value


class ExBuffer(CPUElement):
    def __init__(self):
        self.out_writeRegMux = Value(0)
        self.out_readData2 = Value(0)
        self.out_aluResult = Value(0)
        self.out_aluZero = Value(0)
        self.out_jumpAddr = Value(0)
        self.out_controlBranch = Value(0)
        self.out_controlMemWrite = Value(0)
        self.out_controlMemRead = Value(0)
        self.out_controlMemtoReg = Value(0)
        self.out_controlRegWrite = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        self.in_writeRegMux = inputs[0]
        self.in_readData2 = inputs[1]
        self.in_aluResult = inputs[2]
        self.in_aluZero = inputs[3]
        self.in_branchAddr = inputs[4]
        self.in_controlBranch = inputs[5]
        self.in_controlMemWrite = inputs[6]
        self.in_controlMemRead = inputs[7]
        self.in_controlMemtoReg = inputs[8]
        self.in_controlRegWrite = inputs[9]
    
    def writeOutput(self):
        print("exBuffer branch", self.in_controlBranch.value)
        self.out_writeRegMux.value = self.in_writeRegMux.value
        self.out_readData2.value = self.in_readData2 .value
        self.out_aluResult.value = self.in_aluResult .value
        self.out_aluZero.value = self.in_aluZero .value
        self.out_jumpAddr.value = self.in_branchAddr .value
        self.out_controlBranch.value = self.in_controlBranch .value
        self.out_controlMemWrite.value = self.in_controlMemWrite .value
        self.out_controlMemRead.value = self.in_controlMemRead .value
        self.out_controlMemtoReg.value = self.in_controlMemtoReg .value
        self.out_controlRegWrite.value = self.in_controlRegWrite .value
        

class MemBuffer(CPUElement):
    def __init__(self):
        self.out_MemtoReg = Value(0)
        self.out_RegWrite = Value(0)
        self.out_DataRead = Value(0)
        self.out_ALUResult = Value(0)
        self.out_writeRegMux = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        self.in_MemtoReg = inputs[0]
        self.in_RegWrite = inputs[1]
        self.in_DataRead = inputs[2]
        self.in_ALUResult = inputs[3]
        self.in_writeRegMux = inputs[4]
    
    def writeOutput(self):
        self.out_MemtoReg.value = self.in_MemtoReg.value
        self.out_RegWrite.value = self.in_RegWrite.value
        self.out_DataRead.value = self.in_DataRead.value
        self.out_ALUResult.value = self.in_ALUResult.value
        self.out_writeRegMux.value = self.in_writeRegMux.value