import unittest
from elements.zeroExtend import ZeroExtend
from common import Value

class TestZeroExtend(unittest.TestCase):
    def test_writeOutput(self):
        zeroExtend = ZeroExtend()
        zeroExtend.connectInputs([Value(0xffff)])
        zeroExtend.writeOutput()
        self.assertEqual(zeroExtend.output.value, 0xffff)
