import unittest
from elements.randomControl import RandomControl

class TestRandomControl(unittest.TestCase):
    def test_writeOutput(self):
        control = RandomControl()
        control.connectInputs([])
        control.writeOutput()
        self.assertIn(control.controlSignal.value, [0, 1])
