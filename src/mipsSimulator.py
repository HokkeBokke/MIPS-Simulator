'''
Code written for inf-2200, University of Tromso
'''

from elements.alu import ALU
from elements.aluControl import ALUControl
from elements.combineBits import CombineBits
from elements.control import Control
from elements.pc import PC
from elements.add import Add
from elements.mux import Mux
from elements.registerFile import RegisterFile
from elements.instructionMemory import InstructionMemory
from elements.dataMemory import DataMemory
from elements.constant import Constant
from elements.randomControl import RandomControl
from elements.shiftleft import ShiftLeft2
from elements.signExtend import SignExtend


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
        self.constant4 = Constant(4)
        self.add4toPC = Add()
        self.pc = PC(self.startAddress())
        self.control = Control()
        
        self.shiftLeftJumpAddress = ShiftLeft2()
        self.combineJumpAddress = CombineBits(range(28, 32), range(0, 28))
        self.jumpMux = Mux()
        
        self.signExtendImmediate = SignExtend()
        self.immediateMux = Mux()
        self.aluControl = ALUControl()
        self.alu = ALU()

        self.elements = [self.constant1, self.constant4, self.control, 
                         self.add4toPC, self.shiftLeftJumpAddress, self.combineJumpAddress, self.jumpMux,
                         self.signExtendImmediate, self.immediateMux, self.aluControl, self.alu]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant1.connectInputs([])
        self.constant4.connectInputs([])
        
        self.add4toPC.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.pc.connectInputs([self.jumpMux.output])
        self.instructionMemory.connectInputs([self.pc.currentAddress])
        self.control.connectInputs([self.instructionMemory.outgoingInstruction])
        
        self.shiftLeftJumpAddress.connectInputs([self.instructionMemory.outgoingInstruction])
        self.combineJumpAddress.connectInputs([self.pc.currentAddress, self.shiftLeftJumpAddress.result])
        self.jumpMux.connectInputs([self.add4toPC.result, self.combineJumpAddress.output, self.control.Jump])
        
        self.signExtendImmediate.connectInputs([self.instructionMemory.outgoingInstruction])
        self.immediateMux.connectInputs([self.registerFile.read_data2, self.signExtendImmediate.output, self.control.ALUSrc])
        self.aluControl.connectInputs([self.instructionMemory.outgoingInstruction, self.control.ALUOp])
        self.alu.connectInputs([self.registerFile.read_data1, self.immediateMux.output, self.aluControl.aluInstr])

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
