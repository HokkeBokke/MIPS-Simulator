'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from typing import List
from common import Value

instruction_opcodes = {
    0x02: "j",
    0x04: "beq",
    0x05: "bne",
    0x08: "addi",
    0x09: "addiu",
    0x0F: "lui",
    0x23: "lw",
    0x2B: "sw",
}

extention_op = {
    "sext16": 0b00,
    "zext16": 0b01,
    "upper": 0b10
}

branch_op = {
    "bne": 0b01,
    "beq": 0b10
}

class Control(CPUElement):
    '''
    Control unit
    '''
    def __init__(self):
         # Input
        self.opcode: Value
                
        # Output
        self.PCSrc = Value(0)
        self.Branch = Value(0)
        self.Jump = Value(0)
        self.RegWrite = Value(0)
        self.RegDst = Value(0)
        self.ALUSrc = Value(0)
        self.ALUOp = Value(0)
        self.MemRead = Value(0)
        self.MemWrite = Value(0)
        self.MemtoReg = Value(0)
        self.ExtOp = Value(0)
        
    def reset_outputs(self):
        self.PCSrc.value = 0
        self.Branch.value = 0
        self.Jump.value = 0
        self.RegWrite.value = 0
        self.RegDst.value = 0
        self.ALUSrc.value = 0
        self.ALUOp.value = 0
        self.MemRead.value = 0
        self.MemWrite.value = 0
        self.MemtoReg.value = 0
        self.ExtOp.value = 0
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 1, 'Instruction as input'
        
        self.opcode = inputs[0]

    def writeOutput(self):
        self.reset_outputs()
        
        opcode = self.opcode.value
        if opcode == 0x0:
            self.decode_r_type()
        elif opcode == 0x02 or opcode == 0x03:
            self.decode_j_type(opcode)
        else:
            self.decode_i_type(opcode)


    def decode_r_type(self):
        self.RegDst.value = 1   # destination register is determined by $rd
        self.ALUSrc.value = 0   # ALU reads from the register output
        self.MemtoReg.value = 0 
        self.RegWrite.value = 1 # write ALU result to dest register
        self.MemRead.value = 0
        self.MemWrite.value = 0
        self.Branch.value = 0
        self.ALUOp.value = 0b10 # tells the ALU control unit to read the funct field to figure out what operation to perform


    def decode_j_type(self, opcode):
        op = instruction_opcodes[opcode]
        match op:
            case "j":
                self.Jump.value = 1
            case _:
                print("unsupported jump instruction")
                
    def decode_i_type(self, opcode):
        op = instruction_opcodes[opcode]
        match op:
            case "lui":
                self.ALUSrc.value = 1
                self.RegWrite.value = 1
                self.RegDst.value = 0
                self.ExtOp.value = extention_op["upper"]
            case "lw":
                self.ALUSrc.value = 1
                self.ALUOp.value = 0b00
                self.RegDst.value = 0
                self.ExtOp.value = extention_op["sext16"]
                self.RegWrite.value = 1
                self.MemRead.value = 1
                self.MemtoReg.value = 1
            case "sw":
                self.ALUSrc.value = 1
                self.RegWrite.value = 0
                self.MemWrite.value = 1
                self.ALUOp.value = 0b00
                self.ExtOp.value = extention_op["sext16"]
            case "addi":
                self.ALUSrc.value = 1
                self.RegWrite.value = 1
                self.ALUOp.value = 0b00
                self.ExtOp.value = extention_op["sext16"]
            case "addiu":
                self.ALUSrc.value = 1
                self.RegWrite.value = 1
                self.ALUOp.value = 0b00
                self.ExtOp.value = extention_op["sext16"]
            case "bne":
                self.ALUSrc.value = 0
                self.RegWrite.value = 0
                self.ALUOp.value = 0b01
                self.Branch.value = branch_op["bne"]
                self.ExtOp.value = extention_op["sext16"]
            case "beq":
                self.ALUSrc.value = 0
                self.RegWrite.value = 0
                self.ALUOp.value = 0b01
                self.Branch.value = branch_op["beq"]
                self.ExtOp.value = extention_op["sext16"]
            case _:
                print("invalid opcode:", hex(opcode))
        
        print("jump", self.Jump.value, "branch", self.Branch.value)
