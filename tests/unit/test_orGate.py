import unittest
from elements.orGate import OrGate
from common import Value

class TestOrGate(unittest.TestCase):
    def test_writeOutput(self):
        gate = OrGate()
        gate.connectInputs([Value(1), Value(0)])
        gate.writeOutput()
        self.assertEqual(gate.output.value, 1)
