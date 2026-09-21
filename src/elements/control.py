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
        assert len(inputs) == 1, 'Instruction [31-26]'
        PCSrc = 0
        RegWrite = 0
        RegDst = 0
        ALUSrc = 0
        ALUOp = 0
        ALUControl = 0
        MemRead = 0
        MemWrite = 0
        MemtoReg = 0
        
    def writeOutput(self):
        self.controlSignal.value = random.randint(0, 1)
