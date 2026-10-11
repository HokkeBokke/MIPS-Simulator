'''
Code written for inf-2200, University of Tromso
'''

from elements.alu import ALU
from elements.aluControl import ALUControl
from elements.combineBits import CombineBits
from elements.control import Control
from elements.forwardingUnit import ForwardingUnit
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
from elements.eqComparator import EqualityComparator
from elements.branchControl import BranchControl
from elements.hazardDetection import HazardDetection

from common import Break, printInstructionFormat


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

        self.constant0 = Constant(0)
        self.constant1 = Constant(1)
        self.constant4 = Constant(4)
        self.add4toPC = Add()
        self.pcSrc = Mux(3)
        self.pc = PC(self.startAddress())
        self.control = Control()
        self.hazardDetection = HazardDetection()
        self.stallMux = Mux(2)
        
        self.fetchBuffer = FetchBuffer()
        self.decodeBuffer = DecodeBuffer()
        self.exBuffer = ExBuffer()
        self.memBuffer = MemBuffer()
        
        self.branchAdder = Add()
        self.branchShiftLeft = ShiftLeft2()
        
        self.branchControl = BranchControl()
        
        self.shiftLeftJumpAddress = ShiftLeft2()
        self.combineJumpAddress = CombineBits(range(28, 32), range(0, 28))
        self.jumpMux = Mux(2)
        
        self.shiftUpper = ShiftUpper()
        self.zext = ZeroExtend()
        self.extMux = Mux(3)
        
        self.reg1forwardMux = Mux(3)
        self.reg2forwardMux = Mux(3)
        
        self.signExtendImmediate = SignExtend()
        self.immediateMux = Mux(2)
        self.aluControl = ALUControl()
        self.alu = ALU()
        self.eqComparator = EqualityComparator()
        self.forwardingUnit = ForwardingUnit()

        self.fetchStage = [self.pcSrc, self.pc, self.add4toPC, self.instructionMemory]
        
        self.decodeStage = [
            self.opcodeBitFilter, self.readReg1BitFilter, self.readReg2BitFilter, 
            self.writeRegBitFilter, self.immBitFilter, self.functBitFilter,
            self.control, self.stallMux, 
            self.shiftUpper, self.zext ,self.signExtendImmediate, self.extMux,
            self.branchShiftLeft, self.branchAdder, 
            self.shiftLeftJumpAddress, self.combineJumpAddress,
            self.registerFile, self.eqComparator, self.branchControl
        ]

        self.executionStage = [
            self.reg1forwardMux, self.reg2forwardMux,
            self.aluControl, self.immediateMux, self.alu, self.writeRegMux
        ]
        
        self.memoryStage = [self.dataMemory]
        
        self.writebackStage = [self.WBMux]
        
        self.buffers = [self.memBuffer, self.exBuffer, self.decodeBuffer, self.fetchBuffer]

        self._connectCPUElements()

    def _connectCPUElements(self):
        self.constant0.connectInputs([])
        self.constant1.connectInputs([])
        self.constant4.connectInputs([])
        
        # Fetch stage
        self.pcSrc.connectInputs([self.add4toPC.result, self.branchAdder.result, self.combineJumpAddress.output, self.branchControl.output])
        self.add4toPC.connectInputs([self.pc.currentAddress, self.constant4.constantValue])
        self.pc.connectInputs([self.pcSrc.output, self.hazardDetection.PCWrite])
        self.instructionMemory.connectInputs([self.pc.currentAddress])
        
        
        # IF/ID buffer
        self.fetchBuffer.connectInputs([
            self.add4toPC.result,
            self.instructionMemory.outgoingInstruction,
            self.hazardDetection.flush,
            self.hazardDetection.IFIDWrite
        ])
        
        # Decode stage
        self.readReg2BitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.writeRegBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.immBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.functBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.opcodeBitFilter.connectInputs([self.fetchBuffer.out_instruction])
        self.readReg1BitFilter.connectInputs([self.fetchBuffer.out_instruction])
        
        self.shiftLeftJumpAddress.connectInputs([self.fetchBuffer.out_instruction])
        self.combineJumpAddress.connectInputs([self.fetchBuffer.out_pc, self.shiftLeftJumpAddress.result])
        
        self.control.connectInputs([self.opcodeBitFilter.filteredBits])
        
        # Put in own component
        self.signExtendImmediate.connectInputs([self.immBitFilter.filteredBits])
        self.shiftUpper.connectInputs([self.immBitFilter.filteredBits])
        self.zext.connectInputs([self.immBitFilter.filteredBits])
        self.extMux.connectInputs([self.signExtendImmediate.output, self.zext.output, self.shiftUpper.output, self.control.ExtOp])
        # ---------------------
        
        self.branchShiftLeft.connectInputs([self.signExtendImmediate.output])
        self.branchAdder.connectInputs([self.fetchBuffer.out_pc, self.branchShiftLeft.result])

        self.registerFile.connectInputs(
            [
                self.memBuffer.out_RegWrite,
                self.readReg1BitFilter.filteredBits,
                self.readReg2BitFilter.filteredBits,
                self.memBuffer.out_writeRegMux,
                self.WBMux.output
            ]
        ) 

        self.hazardDetection.connectInputs([
            self.readReg1BitFilter.filteredBits,
            self.readReg2BitFilter.filteredBits,
            self.decodeBuffer.out_MemRead,
            self.decodeBuffer.out_readReg1BitFilter,
            self.decodeBuffer.out_readReg2BitFilter,
            self.decodeBuffer.out_RegWrite,
            self.exBuffer.out_writeRegMux,
            self.exBuffer.out_controlRegWrite,
            self.memBuffer.out_writeRegMux,
            self.memBuffer.out_RegWrite,
            self.control.Branch
        ])
        
        self.eqComparator.connectInputs([self.registerFile.read_data1, self.registerFile.read_data2])
        self.branchControl.connectInputs([self.control.Branch, self.eqComparator.output, self.control.Jump])
        self.stallMux.connectInputs([self.control.signalsValue, self.constant0.constantValue, self.hazardDetection.stall])

        # ID/EX buffer (control via stallMux so stalls insert a bubble)
        self.decodeBuffer.connectInputs([
            self.stallMux.output,
            self.registerFile.read_data1, self.registerFile.read_data2,
            self.extMux.output, self.readReg1BitFilter.filteredBits,
            self.readReg2BitFilter.filteredBits, self.writeRegBitFilter.filteredBits,
            self.functBitFilter.filteredBits
        ])
        
        # Execution stage
        self.forwardingUnit.connectInputs([
            self.decodeBuffer.out_readReg1BitFilter,
            self.decodeBuffer.out_readReg2BitFilter,
            self.exBuffer.out_controlRegWrite,
            self.exBuffer.out_writeRegMux,
            self.memBuffer.out_RegWrite,
            self.memBuffer.out_writeRegMux
        ])
        
        self.reg1forwardMux.connectInputs([
            self.decodeBuffer.out_readData1,
            self.WBMux.output,
            self.exBuffer.out_aluResult,
            self.forwardingUnit.forwardA
        ])
        self.reg2forwardMux.connectInputs([
            self.decodeBuffer.out_readData2,
            self.WBMux.output,
            self.exBuffer.out_aluResult,
            self.forwardingUnit.forwardB
        ])
        
        self.aluControl.connectInputs([self.decodeBuffer.out_funct, self.decodeBuffer.out_ALUOp])
        self.immediateMux.connectInputs([self.reg2forwardMux.output, self.decodeBuffer.out_signExtend, self.decodeBuffer.out_ALUSrc])
        self.alu.connectInputs([self.reg1forwardMux.output, self.immediateMux.output, self.aluControl.aluInstr])
        self.writeRegMux.connectInputs([self.decodeBuffer.out_readReg2BitFilter, self.decodeBuffer.out_writeRegBitFilter, self.decodeBuffer.out_RegDst])
        

        # EX/MEM buffer
        self.exBuffer.connectInputs([
            self.writeRegMux.output, self.reg2forwardMux.output,
            self.alu.result, self.alu.isZero, self.branchAdder.result,
            self.decodeBuffer.out_Branch, self.decodeBuffer.out_MemWrite,
            self.decodeBuffer.out_MemRead, self.decodeBuffer.out_MemtoReg,
            self.decodeBuffer.out_RegWrite
        ])
       
        # Memory stage
        self.dataMemory.connectInputs([
            self.exBuffer.out_aluResult, 
            self.exBuffer.out_readData2, 
            self.exBuffer.out_controlMemWrite,
            self.exBuffer.out_controlMemRead
        ])

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
        print("cycle", self.nCycles)
        
        # The following is just a small sample implementation
        #self.pc.writeOutput()
        #print("pc:", hex(self.pc.currentAddress.value))
        #self.instructionMemory.writeOutput()
        #print("mem:", hex(self.instructionMemory.incomingAddress.value))
        #printInstructionFormat(self.instructionMemory.outgoingInstruction.value)
        
        # Refresh IF/ID-derived decode signals before hazard detection so it
        # sees the current instruction's Branch/rs/rt, not last cycle's.
        for elem in [self.opcodeBitFilter, self.readReg1BitFilter, self.readReg2BitFilter, self.control]:
            elem.writeOutput()

        self.hazardDetection.writeOutput()
        self.forwardingUnit.writeOutput()
        
        fetchStage = self.fetchStage
        if self.nCycles == 1:
            fetchStage = fetchStage[1:]
        
        try:
            for stage in [self.writebackStage, self.memoryStage, self.executionStage, self.decodeStage, fetchStage]:
                for elem in stage:
                    elem.writeOutput()
        except Break:
            self.registerFile.writeOutput()
            self.memBuffer.writeOutput()
            self.WBMux.writeOutput()
            self.registerFile.writeOutput()
            raise
        
        #for elem in fetchStage:
        #    elem.writeOutput()
        
        for buffer in self.buffers:
            buffer.writeOutput()
                
        printInstructionFormat(self.fetchBuffer.out_instruction.value)
            
        #print("branch control:", self.branchControl.output.value)
        #print("pc after:", hex(self.pc.currentAddress.value))
                
        
        self.registerFile.printAll()
