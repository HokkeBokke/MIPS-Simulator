import unittest
from elements.eqComparator import EqualityComparator
from common import Value

class TestEqualityComparator(unittest.TestCase):
    def test_writeOutput(self):
        comparator = EqualityComparator()
        comparator.connectInputs([Value(7), Value(7)])
        comparator.writeOutput()
        self.assertEqual(comparator.output.value, 1)
