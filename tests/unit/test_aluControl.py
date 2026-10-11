import unittest
from elements.aluControl import ALUControl
from common import Value

class TestALUControl(unittest.TestCase):
    def test_writeOutput(self):
        aluControl = ALUControl()
        aluControl.connectInputs([Value(0x20), Value(0b10)])
        aluControl.writeOutput()
        self.assertEqual(aluControl.aluInstr.value, 0b0010)
