import unittest
from elements.shiftUpper import ShiftUpper
from common import Value

class TestShiftUpper(unittest.TestCase):
    def test_writeOutput(self):
        shift = ShiftUpper()
        shift.connectInputs([Value(1)])
        shift.writeOutput()
        self.assertEqual(shift.output.value, 0x10000)
