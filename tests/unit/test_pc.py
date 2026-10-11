import unittest
from elements.pc import PC
from common import Value

class TestPC(unittest.TestCase):
    def test_writeOutput(self):
        nextAddress = Value(0)
        pc = PC(0)
        pc.connectInputs([nextAddress, Value(1)])
        nextAddress.value = 8
        pc.writeOutput()
        self.assertEqual(pc.currentAddress.value, 8)
