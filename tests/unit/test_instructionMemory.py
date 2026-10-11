import os
import tempfile
import unittest
from elements.instructionMemory import InstructionMemory
from common import Value

class TestInstructionMemory(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile("w", suffix=".mem", delete=False) as file:
            file.write("0x00000000\t0x0000002a\tdata\n")
        self.filename = file.name

    def tearDown(self):
        os.remove(self.filename)

    def test_writeOutput(self):
        instructionMemory = InstructionMemory(self.filename)
        instructionMemory.connectInputs([Value(0)])
        instructionMemory.writeOutput()
        self.assertEqual(instructionMemory.outgoingInstruction.value, 42)
