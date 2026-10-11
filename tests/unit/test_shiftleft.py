import unittest
from elements.shiftleft import ShiftLeft2
from common import Value

class TestShiftLeft2(unittest.TestCase):
    def test_writeOutput(self):
        shift = ShiftLeft2()
        shift.connectInputs([Value(3)])
        shift.writeOutput()
        self.assertEqual(shift.result.value, 12)
