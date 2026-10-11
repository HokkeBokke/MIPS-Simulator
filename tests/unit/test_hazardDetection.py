import unittest
from elements.hazardDetection import HazardDetection
from common import Value

class TestHazardDetection(unittest.TestCase):
    def run_unit(self, inputs):
        hazardDetection = HazardDetection()
        hazardDetection.connectInputs([Value(i) for i in inputs])
        hazardDetection.writeOutput()
        return hazardDetection

    def test_writeOutput(self):
        hazardDetection = self.run_unit([9, 10, 0, 9, 0, 1, 0, 0, 0, 0, 0b01, 0])
        self.assertEqual(hazardDetection.stall.value, 1)
        self.assertEqual(hazardDetection.PCWrite.value, 0)
        self.assertEqual(hazardDetection.IFIDWrite.value, 0)

    def test_beq_stall(self):
        hazardDetection = self.run_unit([9, 10, 0, 9, 0, 1, 0, 0, 0, 0, 0b10, 0])
        self.assertEqual(hazardDetection.stall.value, 1)

    def test_stall_on_exmem(self):
        hazardDetection = self.run_unit([9, 10, 0, 0, 0, 0, 10, 1, 0, 0, 0b10, 0])
        self.assertEqual(hazardDetection.stall.value, 1)

    def test_stall_on_memwb(self):
        hazardDetection = self.run_unit([9, 10, 0, 0, 0, 0, 0, 0, 9, 1, 0b01, 0])
        self.assertEqual(hazardDetection.stall.value, 1)

    def test_no_stall_without_dependency(self):
        hazardDetection = self.run_unit([9, 10, 0, 11, 12, 1, 13, 1, 14, 1, 0b10, 0])
        self.assertEqual(hazardDetection.stall.value, 0)
        self.assertEqual(hazardDetection.PCWrite.value, 1)
        self.assertEqual(hazardDetection.IFIDWrite.value, 1)

    def test_no_stall_without_branch(self):
        hazardDetection = self.run_unit([9, 10, 0, 9, 0, 1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(hazardDetection.stall.value, 0)
