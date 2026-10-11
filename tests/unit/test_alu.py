import unittest
from elements.alu import ALU
from common import Value, Overflow

class TestALU(unittest.TestCase):
    def run_alu(self, a, b, op):
        alu = ALU()
        alu.connectInputs([Value(a), Value(b), Value(op)])
        alu.writeOutput()
        return alu

    def test_writeOutput(self):
        alu = self.run_alu(5, 4, 0b0010)
        self.assertEqual(alu.result.value, 9)
        self.assertEqual(alu.isZero.value, 0)

    def test_add_overflow(self):
        with self.assertRaises(Overflow):
            self.run_alu(0x7fffffff, 1, 0b0010)

    def test_sub_overflow(self):
        with self.assertRaises(Overflow):
            self.run_alu(0x80000000, 1, 0b0110)

    def test_addu_no_overflow(self):
        alu = self.run_alu(0x7fffffff, 1, 0b1010)
        self.assertEqual(alu.result.value, 0x80000000)

    def test_subu_no_overflow(self):
        alu = self.run_alu(0x80000000, 1, 0b1110)
        self.assertEqual(alu.result.value, 0x7fffffff)

    def test_sub_zero(self):
        alu = self.run_alu(5, 5, 0b0110)
        self.assertEqual(alu.result.value, 0)
        self.assertEqual(alu.isZero.value, 1)

    def test_slt_negative(self):
        alu = self.run_alu(0xffffffff, 1, 0b0111)
        self.assertEqual(alu.result.value, 1)
