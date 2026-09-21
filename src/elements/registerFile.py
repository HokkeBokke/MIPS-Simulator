'''
Code written for inf-2200, University of Tromso
'''

from elements.cpuElement import CPUElement
import common
from typing import List
from common import Value

class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}
        # Note that we won't actually use all the registers listed here...
        self.registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                              '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                              '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                              '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0
            
        self.read_data1 = Value(0)
        self.read_data2 = Value(0)


    def connectInputs(self, inputs: List[Value]):
        self.RegWrite = inputs[0]   # regWrite from Control unit
        self.read_addr1 = inputs[1] # instruction [25-21]
        self.read_addr2 = inputs[2] # instruction [20-16]
        self.write_addr = inputs[3] # instruction [15-11 or 20-16] mux
        self.write_data = inputs[4] # data from writeback stage
        
    def writeOutput(self):
        pass

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print(f"{self.registerNames[i]} \t=> {common.fromUnsignedWordToSignedWord(self.register[i])} ({hex(int(self.register[i]))[:-1]})")
        print("================")
        print()
        print()
