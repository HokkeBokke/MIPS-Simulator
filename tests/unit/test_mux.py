import unittest
from elements.mux import Mux
from common import Value

class TestMux(unittest.TestCase):
    def test_writeOutput(self):
        mux = Mux(2)
        mux.connectInputs([Value(5), Value(9), Value(1)])
        mux.writeOutput()
        self.assertEqual(mux.output.value, 9)
