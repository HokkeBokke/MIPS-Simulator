'''
Code written for inf-2200, University of Tromso
'''

from elements.pc import PC
from elements.add import Add
from elements.mux import Mux
from elements.registerFile import RegisterFile
from elements.instructionMemory import InstructionMemory
from elements.dataMemory import DataMemory
from elements.constant import Constant
from elements.randomControl import RandomControl


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''

    def __init__(self, memoryFileName: str):
        self.nCycles = 0  # Used to hold number of clock cycles spent executing instructions

        self.dataMemory = DataMemory(memoryFileName)
        self.instructionMemory = InstructionMemory(memoryFileName)
        self.registerFile = RegisterFile()

        self.constant1 = Constant(1)
        self.constant3 = Constant(3)
        self.constant4 = Constant(4)
        self.randomControl = RandomControl()
        self.mux = Mux()
        self.adder = Add()
        self.pc = PC(self.startAddress())
        print(self.pc.currentAddress.value)

        self.elements = [self.constant1, self.constant3, self.constant4,
                         self.randomControl, self.adder, self.mux]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant1.connectInputs([])
        self.constant3.connectInputs([])
        self.constant4.connectInputs([])
        self.randomControl.connectInputs([])
        
        self.adder.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.pc.connectInputs([self.adder.result])
        self.instructionMemory.connectInputs([self.pc.currentAddress])
        
        return
        self.pc.connectInputs([self.mux.output])
        self.adder.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.mux.connectInputs([self.adder.result, self.constant3.constantValue, self.randomControl.controlSignal])

    def startAddress(self):
        '''
        Returns first instruction from instruction memory
        '''
        print("start address: ", hex(next(iter(sorted(self.instructionMemory.memory.keys())))))
        return next(iter(sorted(self.instructionMemory.memory.keys())))

    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def memory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''

        return self.dataMemory.memory

    def registers(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''

        return self.registerFile.register

    def printDataMemory(self):
        self.dataMemory.printAll()

    def printRegisterFile(self):
        self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''
        
        self.nCycles += 1
        
        # The following is just a small sample implementation
        self.pc.writeOutput()
        print("pc:", hex(self.pc.currentAddress.value))
        print("mem:", hex(self.instructionMemory.incomingAddress.value))
        self.instructionMemory.writeOutput()
        for elem in self.elements:
            elem.writeOutput()
