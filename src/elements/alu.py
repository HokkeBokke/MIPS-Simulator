from typing import List
from elements.cpuElement import CPUElement
from common import Value

class ALU(CPUElement):
    def __init__(self):
        # INPUT
        self.value_a: Value
        self.value_b: Value
        self.aluControlOp: Value
        
        # OUTPUT
        self.result: Value = Value(0)
        self.isZero: Value = Value(0)
    
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 3, "ALU requires 2 inputs and ALU control op"
        
        self.value_a = inputs[0]
        self.value_b = inputs[1]
        self.aluControlOp = inputs[2]
    
    def writeOutput(self) -> None:
        self.isZero.value = 0
        
        match self.aluControlOp.value:
            case 0b0010:
                print("ALU add")
                print(f"ALU: {self.value_a.value} + {self.value_b.value} = {self.value_a.value + self.value_b.value}")
                self.result.value = self.value_a.value + self.value_b.value
            case 0b0110:
                print("ALU sub")
                self.result.value = self.value_a.value - self.value_b.value
            case 0b0000:
                print("ALU and")
                self.result.value = self.value_a.value & self.value_b.value
            case 0b0001:
                print("ALU or")
                self.result.value = self.value_a.value | self.value_b.value
            case _:
                print("ALU ?", bin(self.aluControlOp.value))
                
        print(f"ALU Output = {self.result.value} ({hex(self.result.value)})")
