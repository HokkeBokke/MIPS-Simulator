from typing import List

from elements.cpuElement import CPUElement
from common import Value

alu_control_signal = {
    "add": 0b0010,
    "subtract": 0b0110,
    "AND": 0b0000,
    "OR": 0b0001,
    "slt": 0b0111, # set on less than
}

r_instruction_funct = {
    0x20: "add",
    0x21: "addu",
    0x22: "sub",
    0x23: "subu",
    0x24: "AND",
}

class ALUControl(CPUElement):
    def __init__(self):
        # INPUT
        self.funct = Value(0)
        self.aluOp = Value(0)
        
        # OUTPUT
        self.aluInstr: Value = Value(0)
        
    
    def connectInputs(self, inputs: List[Value]):
        self.funct = inputs[0]
        self.aluOp = inputs[1]
    
    def writeOutput(self) -> None:
        if self.aluOp.value == 0b10:
            funct = r_instruction_funct[(self.funct.value & 0b111111)]
            match funct:
                case "add":
                    self.aluInstr.value = alu_control_signal["add"]
                case "sub" "subu":
                    self.aluInstr.value = alu_control_signal["subtract"]
                case "AND":
                    self.aluInstr.value = alu_control_signal["AND"]
                case "OR":
                    self.aluInstr.value = alu_control_signal["OR"]
                case _:
                    print("INVALID INSTRUCTION BRO")
                    
        elif self.aluOp.value == 0b00:
            self.aluInstr.value = alu_control_signal["add"]
        elif self.aluOp.value == 0b01:
            self.aluInstr.value = alu_control_signal["subtract"]
        else:
            print("DEBUG: Unknown ALUOp")
