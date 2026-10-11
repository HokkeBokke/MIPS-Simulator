import unittest
from elements.combineBits import CombineBits
from common import Value

class TestCombineBits(unittest.TestCase):
    def test_writeOutput(self):
        combine = CombineBits(range(28, 32), range(0, 28))
        combine.connectInputs([Value(0xbfc00004), Value(0x00c00200)])
        combine.writeOutput()
        self.assertEqual(combine.output.value, 0xb0c00200)
