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
from elements.memBuffer import DecodeBuffer, FetchBuffer, ExBuffer, MemBuffer

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
        
        self.fetchBuffer = FetchBuffer()
        self.decodeBuffer = DecodeBuffer()
        self.exBuffer = ExBuffer()
        self.memBuffer = MemBuffer()
        
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

        self.fetchStage = [self.pc, self.add4toPC, self.instructionMemory]
        
        self.decodeStage = [
            self.opcodeBitFilter, self.readReg1BitFilter, self.control,
            self.opcodeBitFilter, self.readReg2BitFilter,
            self.writeRegBitFilter, self.immBitFilter, self.functBitFilter,
            self.writeRegMux, self.registerFile
        ]

        self.elements = [
                         self.constant1, self.constant4, 
                         
                         self.beq, self.bne, 
                          self.shiftLeftJumpAddress, self.combineJumpAddress,
                         self.shiftUpper, self.zext,
                         self.signExtendImmediate, self.extMux, self.immediateMux, self.aluControl, self.alu, self.branchNot, self.branchEqAnd, self.branchNotEqAnd, self.branchOr, self.branchShiftLeft, self.branchAdder, self.branchMux, self.jumpMux, self.dataMemory, self.WBMux, 
                         self.registerFile # again in case of writeback
                        ]
        
        self.buffers = [self.fetchBuffer, self.decodeBuffer, self.exBuffer, self.memBuffer]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant1.connectInputs([])
        self.constant4.connectInputs([])
        
        # Fetch stage
        self.add4toPC.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.pc.connectInputs([self.jumpMux.output])
        self.instructionMemory.connectInputs([self.pc.currentAddress])
        
        
        # IF/ID buffer
        self.fetchBuffer.connectInputs([self.add4toPC.result, self.instructionMemory.outgoingInstruction])
        
        # Decode stage
        self.readReg2BitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.writeRegBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.immBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.functBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.shiftLeftJumpAddress.connectInputs([self.fetchBuffer.out_instruction])
        self.combineJumpAddress.connectInputs([self.fetchBuffer.out_pc, self.shiftLeftJumpAddress.result])
        self.jumpMux.connectInputs([self.branchMux.output, self.combineJumpAddress.output, self.control.Jump])
        self.opcodeBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.readReg1BitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.control.connectInputs([self.opcodeBitFilter.filteredBits])
        self.signExtendImmediate.connectInputs([self.immBitFilter.filteredBits])
        self.shiftUpper.connectInputs([self.immBitFilter.filteredBits])
        self.zext.connectInputs([self.immBitFilter.filteredBits])
        self.extMux.connectInputs([self.signExtendImmediate.output, self.zext.output, self.shiftUpper.output, self.control.ExtOp])

        self.registerFile.connectInputs(
            [
                self.control.RegWrite,
                self.readReg1BitFilter.filteredBits,
                self.readReg2BitFilter.filteredBits,
                self.writeRegMux.output,
                self.WBMux.output
            ]
        )

        # ID/EX buffer
        self.decodeBuffer.connectInputs([
            self.control.PCSrc, self.control.Branch, self.control.Jump,
            self.control.RegWrite, self.control.RegDst, self.control.ALUSrc,
            self.control.ALUOp, self.control.MemRead, self.control.MemWrite,
            self.control.MemtoReg, self.control.ExtOp, self.fetchBuffer.out_pc,
            self.registerFile.read_data1, self.registerFile.read_data2,
            self.signExtendImmediate.output, self.readReg2BitFilter.filteredBits,
            self.writeRegBitFilter.filteredBits
        ])
        
        # Execution stage
        self.immediateMux.connectInputs([self.registerFile.read_data2, self.extMux.output, self.control.ALUSrc])
        self.aluControl.connectInputs([self.fetchBuffer.out_instruction, self.control.ALUOp])
        self.alu.connectInputs([self.registerFile.read_data1, self.immediateMux.output, self.aluControl.aluInstr])
        self.writeRegMux.connectInputs([self.readReg2BitFilter.filteredBits, self.writeRegBitFilter.filteredBits, self.control.RegDst])
        self.branchShiftLeft.connectInputs([self.extMux.output])
        self.branchAdder.connectInputs([self.fetchBuffer.out_pc, self.branchShiftLeft.result])

        # EX/MEM buffer
        self.exBuffer.connectInputs([
            self.writeRegMux.output, self.decodeBuffer.out_readData2,
            self.alu.result, self.alu.isZero, self.branchAdder.result,
            self.decodeBuffer.out_Branch, self.decodeBuffer.out_MemWrite,
            self.decodeBuffer.out_MemRead, self.decodeBuffer.out_MemtoReg,
            self.decodeBuffer.out_RegWrite
        ])
       
        # Memory stage
        self.bne.connectInputs([self.control.Branch])
        self.beq.connectInputs([self.control.Branch])
        self.branchNot.connectInputs([self.alu.isZero])
        self.branchNotEqAnd.connectInputs([self.bne.filteredBits, self.branchNot.output])
        self.branchEqAnd.connectInputs([self.beq.filteredBits, self.alu.isZero])
        self.branchOr.connectInputs([self.branchNotEqAnd.output, self.branchEqAnd.output])
        self.branchMux.connectInputs([self.fetchBuffer.out_pc, self.branchAdder.result, self.branchOr.output])
        
        self.dataMemory.connectInputs([self.alu.result, self.registerFile.read_data2, self.control.MemWrite, self.control.MemRead])

        # MEM/WB buffer
        self.memBuffer.connectInputs([
            self.exBuffer.out_controlMemtoReg, self.exBuffer.out_controlRegWrite,
            self.dataMemory.outgoingData, self.exBuffer.out_aluResult,
            self.exBuffer.out_writeRegMux
        ])
        
        # Writeback stage
        self.WBMux.connectInputs([self.memBuffer.out_ALUResult, self.memBuffer.out_DataRead, self.memBuffer.out_MemtoReg])
        

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
        #self.pc.writeOutput()
        print("pc:", hex(self.pc.currentAddress.value))
        #self.instructionMemory.writeOutput()
        #print("mem:", hex(self.instructionMemory.incomingAddress.value))
        printInstructionFormat(self.instructionMemory.outgoingInstruction.value)
        
        for buffer in self.buffers:
            buffer.writeOutput()
        
        for elem in self.fetchStage:
            elem.writeOutput()
            
        for elem in self.elements:
            elem.writeOutput()
                
        for elem in self.fetchStage:
            elem.writeOutput()
                
        self.fetchBuffer.dump()
        print("pc:", hex(self.pc.currentAddress.value))
                
        
            
        self.registerFile.printAll()
