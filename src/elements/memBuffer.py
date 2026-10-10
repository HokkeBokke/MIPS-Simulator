'''
Code written for inf-2200, University of Tromso
'''

from common import Value
from elements.cpuElement import CPUElement
from typing import List

class FetchBuffer(CPUElement):
    def __init__(self):
        self.in_pc: Value
        self.out_pc = Value(0)
        
        self.in_instruction: Value
        self.out_instruction = Value(0)

    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 2, 'FetchBuffer should have 2 inputs'
        
        self.in_pc = inputs[0]
        self.in_instruction = inputs[1]
        
    def writeOutput(self):
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
        self.out_readReg2BitFilter = Value(0)
        self.out_writeRegBitFilter = Value(0)
        
        
    def connectInputs(self, inputs: List[Value]):
        self.in_PCSrc = inputs[0]
        self.in_Branch = inputs[1]
        self.in_Jump = inputs[2]
        self.in_RegWrite = inputs[3]
        self.in_RegDst = inputs[4]
        self.in_ALUSrc = inputs[5]
        self.in_ALUOp = inputs[6]
        self.in_MemRead = inputs[7]
        self.in_MemWrite = inputs[8]
        self.in_MemtoReg = inputs[9]
        self.in_ExtOp = inputs[10]
        self.in_add4toPC = inputs[11]
        self.in_readData1 = inputs[12]
        self.in_readData2 = inputs[13]
        self.in_signExtend = inputs[14]
        self.in_readReg2BitFilter = inputs[15]
        self.in_writeRegBitFilter = inputs[16]
    
    def writeOutput(self):
        self.out_PCSrc = self.in_PCSrc
        self.out_Branch = self.in_Branch
        self.out_Jump = self.in_Jump
        self.out_RegWrite = self.in_RegWrite
        self.out_RegDst = self.in_RegDst
        self.out_ALUSrc = self.in_ALUSrc
        self.out_ALUOp = self.in_ALUOp
        self.out_MemRead = self.in_MemRead
        self.out_MemWrite = self.in_MemWrite
        self.out_MemtoReg = self.in_MemtoReg
        self.out_ExtOp = self.in_ExtOp
        self.out_add4toPC = self.in_add4toPC
        self.out_readData1 = self.in_readData1
        self.out_readData2 = self.in_readData2
        self.out_signExtend = self.in_signExtend
        self.out_readReg2BitFilter = self.in_readReg2BitFilter
        self.out_writeRegBitFilter = self.in_writeRegBitFilter



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
        self.out_writeRegMux = self.in_writeRegMux
        self.out_readData2 = self.in_readData2 
        self.out_aluResult = self.in_aluResult 
        self.out_aluZero = self.in_aluZero 
        self.out_jumpAddr = self.in_branchAddr 
        self.out_controlBranch = self.in_controlBranch 
        self.out_controlMemWrite = self.in_controlMemWrite 
        self.out_controlMemRead = self.in_controlMemRead 
        self.out_controlMemtoReg = self.in_controlMemtoReg 
        self.out_controlRegWrite = self.in_controlRegWrite 
        

class MemBuffer(CPUElement):
    def __init__(self):
        self.in_MemtoReg = Value(0)
        self.in_RegWrite = Value(0)
        self.in_DataRead = Value(0)
        self.in_ALUResult = Value(0)
        self.in_writeRegMux = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        self.in_MemtoReg = inputs[0]
        self.in_RegWrite = inputs[1]
        self.in_DataRead = inputs[2]
        self.in_ALUResult = inputs[3]
        self.in_writeRegMux = inputs[4]
    
    def writeOutput(self):
        self.out_MemtoReg = self.in_MemtoReg
        self.out_RegWrite = self.in_RegWrite
        self.out_DataRead = self.in_DataRead
        self.out_ALUResult = self.in_ALUResult
        self.out_writeRegMux = self.in_writeRegMux