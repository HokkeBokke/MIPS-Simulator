import unittest
from elements.add import Add
from common import Value

class TestAdd(unittest.TestCase):
    def setUp(self):
        self.adder = Add()
        self.value_a = Value(5)
        self.value_b = Value(4)
        
    def test_connectInputs(self):
        self.adder.connectInputs([self.value_a, self.value_b])
        self.assertEqual(self.adder.value_a.value, 5)
        self.assertEqual(self.adder.value_b.value, 4)
        
    def test_writeOutput(self):
        self.adder.connectInputs([self.value_a, self.value_b])
        self.adder.writeOutput()
        self.assertEqual(self.adder.result.value, 9)
