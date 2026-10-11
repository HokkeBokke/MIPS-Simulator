import os
import tempfile
import unittest
from elements.dataMemory import DataMemory
from common import Value

class TestDataMemory(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile("w", suffix=".mem", delete=False) as file:
            file.write("0x00000000\t0x0000002a\tdata\n")
        self.filename = file.name

    def tearDown(self):
        os.remove(self.filename)

    def test_writeOutput(self):
        dataMemory = DataMemory(self.filename)
        dataMemory.connectInputs([Value(0), Value(0), Value(0), Value(1)])
        dataMemory.writeOutput()
        self.assertEqual(dataMemory.outgoingData.value, 42)
