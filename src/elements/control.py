'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
import random
from typing import List
from common import Value

class Control(CPUElement):
    '''
    Control unit
    '''
    def __init__(self):
        # Output
        self.controlSignal: Value = Value(0)
        
    def connectInputs(self, inputs: List[Value]):
        assert len(inputs) == 0, 'Random control does not have any inputs'
        
    def writeOutput(self):
        self.controlSignal.value = random.randint(0, 1)
