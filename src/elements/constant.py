'''
Implement a CPU-element for holding a single integer constant.

Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
from common import Value
from typing import List


class Constant(CPUElement):
    def __init__(self, constant: int):
        # Output
        self.constantValue = Value(constant)
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 0, 'Constant does not have any inputs'

    def writeOutput(self):
        pass
