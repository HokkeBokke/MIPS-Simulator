import unittest
from elements.control import Control
from common import Value

class TestControl(unittest.TestCase):
    def run_control(self, opcode):
        control = Control()
        control.connectInputs([Value(opcode)])
        control.writeOutput()
        return control

    def test_writeOutput(self):
        control = self.run_control(0x23)
        self.assertEqual(control.RegWrite.value, 1)
        self.assertEqual(control.MemRead.value, 1)
        self.assertEqual(control.MemtoReg.value, 1)
        self.assertEqual(control.ALUSrc.value, 1)

    def test_r_type(self):
        control = self.run_control(0x00)
        self.assertEqual(control.RegDst.value, 1)
        self.assertEqual(control.RegWrite.value, 1)
        self.assertEqual(control.ALUSrc.value, 0)
        self.assertEqual(control.ALUOp.value, 0b10)

    def test_sw(self):
        control = self.run_control(0x2B)
        self.assertEqual(control.MemWrite.value, 1)
        self.assertEqual(control.RegWrite.value, 0)
        self.assertEqual(control.ALUSrc.value, 1)

    def test_beq(self):
        control = self.run_control(0x04)
        self.assertEqual(control.Branch.value, 0b10)
        self.assertEqual(control.RegWrite.value, 0)
        self.assertEqual(control.ALUOp.value, 0b01)

    def test_bne(self):
        control = self.run_control(0x05)
        self.assertEqual(control.Branch.value, 0b01)

    def test_jump(self):
        control = self.run_control(0x02)
        self.assertEqual(control.Jump.value, 1)
        self.assertEqual(control.RegWrite.value, 0)

    def test_lui(self):
        control = self.run_control(0x0F)
        self.assertEqual(control.ExtOp.value, 0b10)
        self.assertEqual(control.RegWrite.value, 1)
