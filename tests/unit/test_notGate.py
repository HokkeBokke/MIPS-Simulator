import unittest
from elements.notGate import NotGate
from common import Value

class TestNotGate(unittest.TestCase):
    def test_writeOutput(self):
        gate = NotGate()
        gate.connectInputs([Value(0)])
        gate.writeOutput()
        self.assertEqual(gate.output.value, 1)
