'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from elements.memory import Memory
from common import Value
from typing import List

class DataMemory(Memory):
    def __init__(self, filename: str):
        Memory.__init__(self, filename)
        
    def connectInputs(self, inputs: List[Value]):
        # Remove this and replace with your implementation!
        raise AssertionError("connect not implemented in class DataMemory!")
    
    def writeOutput(self):
        # Remove this and replace with your implementation!
        raise AssertionError("writeOutput not implemented in class DataMemory!")
