import unittest
from elements.constant import Constant

class TestConstant(unittest.TestCase):
    def test_writeOutput(self):
        constant = Constant(4)
        constant.connectInputs([])
        constant.writeOutput()
        self.assertEqual(constant.constantValue.value, 4)
