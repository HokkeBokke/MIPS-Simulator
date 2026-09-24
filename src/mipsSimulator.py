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
from elements.bitFilter import BitFilter
from elements.shiftUpper import ShiftUpper
from elements.zeroExtend import ZeroExtend
from elements.andGate import AndGate
from elements.orGate import OrGate
from elements.notGate import NotGate

from common import printInstructionFormat


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''

    def __init__(self, memoryFileName: str):
        self.nCycles = 0  # Used to hold number of clock cycles spent executing instructions
        self.breakSignal = False

        self.dataMemory = DataMemory(memoryFileName)
        self.instructionMemory = InstructionMemory(memoryFileName)
        self.registerFile = RegisterFile()
        
        self.opcodeBitFilter = BitFilter(31, 26)
        self.readReg1BitFilter = BitFilter(25, 21)
        self.readReg2BitFilter = BitFilter(20, 16)
        self.writeRegBitFilter = BitFilter(15, 11)
        self.immBitFilter = BitFilter(15, 0)
        self.functBitFilter = BitFilter(5, 0)
        
        self.writeRegMux = Mux(2)
        self.WBMux = Mux(2)

        self.constant1 = Constant(1)
        self.constant4 = Constant(4)
        self.add4toPC = Add()
        self.pc = PC(self.startAddress())
        self.control = Control()
        
        self.bne = BitFilter(0, 0)
        self.beq = BitFilter(1, 1)
        self.branchNotEqAnd = AndGate()
        self.branchEqAnd = AndGate()
        self.branchNot = NotGate()
        self.branchOr = OrGate()
        self.branchMux = Mux(2)
        self.branchAdder = Add()
        self.branchShiftLeft = ShiftLeft2()
        
        self.shiftLeftJumpAddress = ShiftLeft2()
        self.combineJumpAddress = CombineBits(range(28, 32), range(0, 28))
        self.jumpMux = Mux(2)
        
        self.shiftUpper = ShiftUpper()
        self.zext = ZeroExtend()
        self.extMux = Mux(3)
        
        self.signExtendImmediate = SignExtend()
        self.immediateMux = Mux(2)
        self.aluControl = ALUControl()
        self.alu = ALU()

        self.elements = [self.opcodeBitFilter, self.readReg1BitFilter, 
                         self.readReg2BitFilter, self.writeRegBitFilter, self.immBitFilter, self.functBitFilter,
                         self.constant1, self.constant4, self.control,
                         self.beq, self.bne, 
                         self.writeRegMux, self.registerFile, self.add4toPC, self.shiftLeftJumpAddress, self.combineJumpAddress,
                         self.shiftUpper, self.zext,
                         self.signExtendImmediate, self.extMux, self.immediateMux, self.aluControl, self.alu, self.branchNot, self.branchEqAnd, self.branchNotEqAnd, self.branchOr, self.branchShiftLeft, self.branchAdder, self.branchMux, self.jumpMux, self.dataMemory, self.WBMux, 
                         self.registerFile # again in case of writeback
                        ]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant1.connectInputs([])
        self.constant4.connectInputs([])
        
        self.add4toPC.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.pc.connectInputs([self.jumpMux.output])
        self.instructionMemory.connectInputs([self.pc.currentAddress])
        self.control.connectInputs([self.opcodeBitFilter.filteredBits])
        
        self.shiftLeftJumpAddress.connectInputs([self.instructionMemory.outgoingInstruction])
        self.combineJumpAddress.connectInputs([self.pc.currentAddress, self.shiftLeftJumpAddress.result])
        self.jumpMux.connectInputs([self.branchMux.output, self.combineJumpAddress.output, self.control.Jump])
        
        self.bne.connectInputs([self.control.Branch])
        self.beq.connectInputs([self.control.Branch])
        self.branchNot.connectInputs([self.alu.isZero])
        self.branchNotEqAnd.connectInputs([self.bne.filteredBits, self.branchNot.output])
        self.branchEqAnd.connectInputs([self.beq.filteredBits, self.alu.isZero])
        self.branchOr.connectInputs([self.branchNotEqAnd.output, self.branchEqAnd.output])
        self.branchShiftLeft.connectInputs([self.extMux.output])
        self.branchAdder.connectInputs([self.add4toPC.result, self.branchShiftLeft.result])
        self.branchMux.connectInputs([self.add4toPC.result, self.branchAdder.result, self.branchOr.output])
        
        self.opcodeBitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        self.readReg1BitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        self.readReg2BitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        self.writeRegBitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        self.immBitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        self.functBitFilter.connectInputs([self.instructionMemory.outgoingInstruction])
        
        self.writeRegMux.connectInputs([self.readReg2BitFilter.filteredBits, self.writeRegBitFilter.filteredBits, self.control.RegDst])
        self.WBMux.connectInputs([self.alu.result, self.dataMemory.outgoingData, self.control.MemtoReg])
        
        self.registerFile.connectInputs(
            [
                self.control.RegWrite,
                self.readReg1BitFilter.filteredBits,
                self.readReg2BitFilter.filteredBits,
                self.writeRegMux.output,
                self.WBMux.output
            ]
        )

        self.shiftUpper.connectInputs([self.immBitFilter.filteredBits])
        self.zext.connectInputs([self.immBitFilter.filteredBits])
        self.extMux.connectInputs([self.signExtendImmediate.output, self.zext.output, self.shiftUpper.output, self.control.ExtOp])
        
        self.signExtendImmediate.connectInputs([self.immBitFilter.filteredBits])
        self.immediateMux.connectInputs([self.registerFile.read_data2, self.extMux.output, self.control.ALUSrc])
        self.aluControl.connectInputs([self.instructionMemory.outgoingInstruction, self.control.ALUOp])
        self.alu.connectInputs([self.registerFile.read_data1, self.immediateMux.output, self.aluControl.aluInstr])
        
        self.dataMemory.connectInputs([self.alu.result, self.registerFile.read_data2, self.control.MemWrite, self.control.MemRead])

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
        self.instructionMemory.writeOutput()
        #print("mem:", hex(self.instructionMemory.incomingAddress.value))
        printInstructionFormat(self.instructionMemory.outgoingInstruction.value)
        for elem in self.elements:
            elem.writeOutput()
        self.registerFile.printAll()
        
