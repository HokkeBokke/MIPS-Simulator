from typing import List
from elements.cpuElement import CPUElement
from common import Value, fromUnsignedWordToSignedWord, fromSignedWordToUnsignedWord, Overflow

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
        
        num1 = fromUnsignedWordToSignedWord(self.value_a.value)
        num2 = fromUnsignedWordToSignedWord(self.value_b.value)
        
        match self.aluControlOp.value:
            case 0b0010:
                self.result.value = num1 + num2
                print(f"ALU: {self.value_a.value} + {self.value_b.value} = {self.result.value} ({hex(fromSignedWordToUnsignedWord(self.result.value))})")
                if abs(self.result.value) >= 0x80000000:
                    raise Overflow("Addition overflow")
            case 0b0110:
                self.result.value = num1 - num2
                print(f"ALU: {self.value_a.value} - {self.value_b.value} = {self.result.value} ({hex(self.result.value)})")
                if abs(self.result.value) > 0x80000000:
                    raise Overflow("Subtraction overflow")
            case 0b0000:
                self.result.value = num1 & num2
                print(f"ALU: {self.value_a.value} & {self.value_b.value} = {self.result.value} ({hex(self.result.value)})")
            case 0b0001:
                self.result.value = num1 | num2
                print(f"ALU: {self.value_a.value} | {self.value_b.value} = {self.result.value} ({hex(self.result.value)})")
            case 0b0111:
                self.result.value = 1 if num1 < num2 else 0
            case 0b0101:
                self.result.value = ~(num1 | num2)
            case _:
                print("ALU ?", bin(self.aluControlOp.value))
        
        
        if self.result.value == 0:
            self.isZero.value = 1
