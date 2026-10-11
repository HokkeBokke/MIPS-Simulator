from typing import List
from elements.cpuElement import CPUElement
from common import Value
from elements.control import branch_op

class BranchControl(CPUElement):
    """ 
    Determines what source PC takes from

    Outputs: 
        - 0 for next instruction
        - 1 for branch
        - 2 for jump
    """
    def __init__(self):
        # Inputs
        self.branchSignal: Value
        self.eqComp: Value
        self.jumpSignal: Value
        
        # Outputs
        self.output = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        self.branchSignal = inputs[0]
        self.eqComp = inputs[1]
        self.jumpSignal = inputs[2]
    
    def writeOutput(self) -> None:
        self.output.value = 0
        
        print(self.branchSignal.value, self.eqComp.value)
        
        if self.branchSignal.value == branch_op["beq"] and self.eqComp.value:
            self.output.value = 1
        elif self.branchSignal.value == branch_op["bne"] and not self.eqComp.value:
            self.output.value = 1
            
        if self.jumpSignal.value:
            self.output.value = 2
            
        print("BranchControl: ", self.output.value)
