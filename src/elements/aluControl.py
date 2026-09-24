from typing import List

from elements.cpuElement import CPUElement
from common import Value, Break

alu_control_signal = {
    "and": 0b0000,
    "or": 0b0001,
    "nor": 0b0101,
    "add": 0b0010,
    "subtract": 0b0110,
    "slt": 0b0111, # set on less than
}

r_instruction_funct = {
    0x00: "nop",
    0x0d: "break",
    0x20: "add",
    0x21: "addu",
    0x22: "sub",
    0x23: "subu",
    0x24: "and",
    0x25: "or",
    0x27: "nor",
    0x2a: "slt"
}

class ALUControl(CPUElement):
    def __init__(self):
        self.breakSignal = False
        
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
                case "nop":
                    return
                case "break":
                    raise Break("break instruction reached")
                case "add" | "addu":
                    self.aluInstr.value = alu_control_signal["add"]
                case "sub" | "subu":
                    self.aluInstr.value = alu_control_signal["subtract"]
                case "and":
                    self.aluInstr.value = alu_control_signal["and"]
                case "or":
                    self.aluInstr.value = alu_control_signal["or"]
                case "slt":
                    self.aluInstr.value = alu_control_signal["slt"]
                case "nor":
                    self.aluInstr.value = alu_control_signal["nor"]
                case _:
                    print("INVALID INSTRUCTION BRO")
                    
        elif self.aluOp.value == 0b00:
            self.aluInstr.value = alu_control_signal["add"]
        elif self.aluOp.value == 0b01:
            self.aluInstr.value = alu_control_signal["subtract"]
        else:
            print("DEBUG: Unknown ALUOp")
