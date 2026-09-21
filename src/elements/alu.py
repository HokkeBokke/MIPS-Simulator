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
            case 0x0010:
                print("ALU add")
            case 0x0110:
                print("ALU sub")
            case 0x0000:
                print("ALU and")
            case 0x0001:
                print("ALU or")
            case _:
                print("ALU ?", self.aluControlOp.value)
