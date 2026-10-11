import unittest
from elements.andGate import AndGate
from common import Value

class TestAndGate(unittest.TestCase):
    def test_writeOutput(self):
        gate = AndGate()
        gate.connectInputs([Value(1), Value(1)])
        gate.writeOutput()
        self.assertEqual(gate.output.value, 1)
