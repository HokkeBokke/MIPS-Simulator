import unittest
from elements.registerFile import RegisterFile
from common import Value

class TestRegisterFile(unittest.TestCase):
    def test_writeOutput(self):
        registerFile = RegisterFile()
        registerFile.connectInputs([Value(1), Value(9), Value(0), Value(9), Value(42)])
        registerFile.writeOutput()
        self.assertEqual(registerFile.register[9], 42)
        registerFile.writeOutput()
        self.assertEqual(registerFile.read_data1.value, 42)
        self.assertEqual(registerFile.read_data2.value, 0)
