import unittest
from elements.memBuffer import FetchBuffer, DecodeBuffer, ExBuffer, MemBuffer
from common import Value

class TestFetchBuffer(unittest.TestCase):
    def test_writeOutput(self):
        buffer = FetchBuffer()
        buffer.connectInputs([Value(4), Value(0x21290001), Value(0), Value(1)])
        buffer.writeOutput()
        self.assertEqual(buffer.out_pc.value, 4)
        self.assertEqual(buffer.out_instruction.value, 0x21290001)

class TestDecodeBuffer(unittest.TestCase):
    def test_writeOutput(self):
        buffer = DecodeBuffer()
        buffer.connectInputs([
            Value(1 << 9 | 1 << 7), Value(5), Value(6), Value(7),
            Value(9), Value(10), Value(11), Value(0x20)
        ])
        buffer.writeOutput()
        self.assertEqual(buffer.out_RegWrite.value, 1)
        self.assertEqual(buffer.out_ALUSrc.value, 1)
        self.assertEqual(buffer.out_MemWrite.value, 0)
        self.assertEqual(buffer.out_readData1.value, 5)
        self.assertEqual(buffer.out_funct.value, 0x20)

class TestExBuffer(unittest.TestCase):
    def test_writeOutput(self):
        buffer = ExBuffer()
        buffer.connectInputs([Value(i) for i in range(10)])
        buffer.writeOutput()
        self.assertEqual(buffer.out_writeRegMux.value, 0)
        self.assertEqual(buffer.out_aluResult.value, 2)
        self.assertEqual(buffer.out_controlRegWrite.value, 9)

class TestMemBuffer(unittest.TestCase):
    def test_writeOutput(self):
        buffer = MemBuffer()
        buffer.connectInputs([Value(i) for i in range(5)])
        buffer.writeOutput()
        self.assertEqual(buffer.out_MemtoReg.value, 0)
        self.assertEqual(buffer.out_ALUResult.value, 3)
        self.assertEqual(buffer.out_writeRegMux.value, 4)
