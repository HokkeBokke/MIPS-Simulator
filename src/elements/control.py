'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

i_instruction_opcodes = {
    0x02: "j",
    0x0F: "lui"
}

class Control(CPUElement):
    '''
    Control unit
    '''
    def __init__(self):
         # Input
        self.instruction: Value
                
        # Output
        self.PCSrc = Value(0)
        self.Branch = Value(0)
        self.Jump = Value(0)
        self.RegWrite = Value(0)
        self.RegDst = Value(0)
        self.ALUSrc = Value(0)
        self.ALUOp = Value(0)
        self.ALUControl = Value(0)
        self.MemRead = Value(0)
        self.MemWrite = Value(0)
        self.MemtoReg = Value(0)
        
    def reset_outputs(self):
        self.PCSrc.value = 0
        self.Branch.value = 0
        self.Jump.value = 0
        self.RegWrite.value = 0
        self.RegDst.value = 0
        self.ALUSrc.value = 0
        self.ALUOp.value = 0
        self.ALUControl.value = 0
        self.MemRead.value = 0
        self.MemWrite.value = 0
        self.MemtoReg.value = 0
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 1, 'Instruction as input'
        
        self.instruction = inputs[0]
        
    def writeOutput(self):
        self.reset_outputs()
        
        print("instr: ", format(self.instruction.value, "#034b"))
        opcode = self.instruction.value >> 26
        print("opcode:", opcode)
        
        if opcode == 0x0:
            self.decode_r_type()
        elif opcode == 0x02 or opcode == 0x03:
            self.decode_j_type(opcode)
        else:
            self.decode_i_type(opcode)
        
        
    def decode_r_type(self):
        self.RegDst.value = 1
        self.ALUSrc.value = 0       # 0 for all R type instructions
        self.MemtoReg.value = 0
        self.RegWrite.value = 1
        self.MemRead.value = 0
        self.MemWrite.value = 0
        self.Branch.value = 0
        self.ALUOp.value = 0b10     # 0b10 for all R type instructions
        

    def decode_j_type(self, opcode):
        op = i_instruction_opcodes[opcode]
        match op:
            case "j":
                self.Jump.value = 1
            case _:
                print("unsupported jump instruction")
                
    def decode_i_type(self, opcode):
        op = i_instruction_opcodes[opcode]
        match op:
            case "lui":
                self.ALUSrc.value = 1
                self.RegWrite.value = 1
            case _:
                print("invalid opcode:", hex(opcode))
