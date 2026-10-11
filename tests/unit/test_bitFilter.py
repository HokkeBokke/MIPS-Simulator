import unittest
from elements.bitFilter import BitFilter
from common import Value

class TestBitFilter(unittest.TestCase):
    def test_writeOutput(self):
        bitFilter = BitFilter(31, 26)
        bitFilter.connectInputs([Value(0x21290001)])
        bitFilter.writeOutput()
        self.assertEqual(bitFilter.filteredBits.value, 0x08)
