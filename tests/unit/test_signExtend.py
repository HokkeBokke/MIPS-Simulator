import unittest
from elements.signExtend import SignExtend
from common import Value

class TestSignExtend(unittest.TestCase):
    def test_writeOutput(self):
        signExtend = SignExtend()
        signExtend.connectInputs([Value(0xffff)])
        signExtend.writeOutput()
        self.assertEqual(signExtend.output.value, 0xffffffff)
