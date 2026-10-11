import unittest
from elements.forwardingUnit import ForwardingUnit
from common import Value

class TestForwardingUnit(unittest.TestCase):
    def run_unit(self, rs, rt, exMemRegWrite, exMemDest, memWbRegWrite, memWbDest):
        forwardingUnit = ForwardingUnit()
        forwardingUnit.connectInputs([
            Value(rs), Value(rt), Value(exMemRegWrite), Value(exMemDest),
            Value(memWbRegWrite), Value(memWbDest)
        ])
        forwardingUnit.writeOutput()
        return forwardingUnit

    def test_writeOutput(self):
        forwardingUnit = self.run_unit(9, 10, 1, 9, 0, 0)
        self.assertEqual(forwardingUnit.forwardA.value, 0b10)
        self.assertEqual(forwardingUnit.forwardB.value, 0b00)

    def test_forward_from_memwb(self):
        forwardingUnit = self.run_unit(9, 10, 1, 11, 1, 10)
        self.assertEqual(forwardingUnit.forwardA.value, 0b00)
        self.assertEqual(forwardingUnit.forwardB.value, 0b01)

    def test_exmem_has_priority(self):
        forwardingUnit = self.run_unit(9, 10, 1, 9, 1, 9)
        self.assertEqual(forwardingUnit.forwardA.value, 0b10)

    def test_no_forward_from_zero_register(self):
        forwardingUnit = self.run_unit(0, 0, 1, 0, 1, 0)
        self.assertEqual(forwardingUnit.forwardA.value, 0b00)
        self.assertEqual(forwardingUnit.forwardB.value, 0b00)

    def test_no_forward_without_regwrite(self):
        forwardingUnit = self.run_unit(9, 10, 0, 9, 0, 10)
        self.assertEqual(forwardingUnit.forwardA.value, 0b00)
        self.assertEqual(forwardingUnit.forwardB.value, 0b00)
