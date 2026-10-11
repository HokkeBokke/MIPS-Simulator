import unittest
from elements.branchControl import BranchControl
from common import Value

class TestBranchControl(unittest.TestCase):
    def test_writeOutput(self):
        branchControl = BranchControl()
        branchControl.connectInputs([Value(0b10), Value(1), Value(0)])
        branchControl.writeOutput()
        self.assertEqual(branchControl.output.value, 1)
