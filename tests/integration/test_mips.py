from genericpath import exists
import pytest
import logging
import os  # nopep8
from common import fromUnsignedWordToSignedWord, Break, Overflow
from src.mipsSimulator import MIPSSimulator


log = logging.getLogger(__name__)


class SubTest():
    def __init__(self, name, destination, expectedValue, minCycles, maxCycles, code, check_memory):
        self.name = name
        self.destination = destination
        self.expectedValue = expectedValue
        self.minCycles = minCycles
        self.maxCycles = maxCycles
        self.code = code
        self.check_memory = check_memory


class MipsWrapper():
    def __init__(self, cwd, memfolder, file, trapTest):
        self.cd = cwd
        self.tmpFileFolder = os.getcwd()+'/'
        self.memfolder = memfolder
        self.filename = file
        self.trapTest = trapTest
        self.tests = {}
        self.currentTest = None
        self.simulator = None
        self.score = 0
        self.maxScore = 0
        # score rewarded for correct trap handling
        self.trapPoint = 1
        # score rewarded for correct mem/reg value
        self.valPoint = 1
        self.setupTests()

    def setupTests(self):
        log.debug(f"Wrapper setting up {self.filename}")
        filepath = self.memfolder + self.filename
        with open(filepath) as memfile:
            for line in memfile:
                if line.startswith(">"):
                    test = line[:-1]  # remove newline
                    _, _, dest, expVal, trap = line.split()
                    check_memory = "Test_sw" in test
                    if trap == "trap" and self.trapTest:
                        self.setupSubTest(filepath, dest, expVal, memfile, check_memory)
                    elif not self.trapTest:
                        self.setupSubTest(filepath, dest, expVal, memfile, check_memory)
        # Each subtest has a max score of 2(1 for trap, 1 for val)
        if self.trapTest:
            self.maxScore = len(self.tests.keys()) * (self.trapPoint)
        else:
            self.maxScore = len(self.tests.keys()) * (self.valPoint)

    def setupSubTest(self, test, dest, expVal, memfile, check_memory):
        log.debug(f"Parsing code for {test}")
        code = []
        minCycles = 0
        for line in memfile:
            if not line.startswith("0"):
                break
            # find number of lines until first break
            _, _, asm = line.split('\t')
            if not asm.startswith("break"):
                minCycles += 1
            code.append(line)
        log.debug(f"Initializing subtest for {test}")
        self.tests[test] = SubTest(
            test, dest, expVal, minCycles, len(code)*10, code, check_memory)

    def checkSimulator(self):
        assert hasattr(self.simulator, "registerFile")
        assert hasattr(self.simulator.registerFile, "register")
        assert type(self.simulator.registerFile.register) == dict
        assert hasattr(self.simulator.registerFile, "registerNames")
        assert type(self.simulator.registerFile.registerNames) == list
        assert hasattr(self.simulator, "dataMemory")
        assert hasattr(self.simulator.dataMemory, "memory")
        assert type(self.simulator.dataMemory.memory) == dict

    def prepare(self, test):
        log.debug(f"Wrapper setting up subtest {test.name}")
        self.simulator = MIPSSimulator(test.name)
        self.CT = test
        self.checkSimulator()

    def _runSimulator(self):
        log.debug(f"Running simulator with {self.CT.name}")
        while(self.simulator.nCycles <= self.CT.maxCycles):
            self.simulator.tick()
        log.critical(
            f"Simulation of '{self.CT.name}' exit due to exceeding cycle limit: {self.CT.maxCycles}")

    def addTrapPoint(self):
        log.debug(f"Adding point for correct trap in {self.CT}")
        self.score += self.trapPoint

    def addValPoint(self):
        log.debug(f"Adding point for correct value in {self.CT}")
        self.score += self.valPoint

    def writeResults(self):
        log.info(
            f"Subtest completed with: [{self.score}] out of [{self.maxScore}] points")
        with open("result", "a+") as res:
            res.write(f"{self.score}/{self.maxScore}\n")

    def getRegisterName(self):
        return self.simulator.registerFile.registerNames[int(self.CT.destination)]

    def getRegisterVal(self):
        return fromUnsignedWordToSignedWord(
            self.simulator.registerFile.register[int(self.CT.destination)])

    def getMemVal(self):
        return hex(self.simulator.dataMemory.memory[int(self.CT.destination, base=16)])

    def validateRun(self):
        log.debug(f"Validating values in {self.CT.name}")
        if self.CT.check_memory:
            try:
                self.validateMemory()
                self.addValPoint()
            except AssertionError:
                
                self.memErrInfo()
                self.simulator.printRegisterFile()
                self.simulator.dataMemory.printAll()
                raise ValueError(
                    f"Memory {self.CT.destination} value: {self.getMemVal()} expected: {self.CT.expectedValue}")
        else:
            try:
                self.validateRegister()
                self.addValPoint()
            except AssertionError:
                self.regErrInfo()
                raise ValueError(
                    f"Register {self.getRegisterName()} value: {self.getRegisterVal()} expected: {self.CT.expectedValue}")

    def memErrInfo(self):
        log.warning(
            f"Memory {self.CT.destination} value: {self.getMemVal()} expected: {self.CT.expectedValue}")

    def validateMemory(self):
        mem = self.simulator.dataMemory.memory
        try:
            sw = hex(mem[int(self.CT.destination, base=16)])
        except KeyError: 
            self.simulator.printRegisterFile()
            self.simulator.dataMemory.printAll()
            raise ValueError(f"Memory at address {hex(int(self.CT.destination, base=16))} hasn't been set")
        assert sw == self.CT.expectedValue
        k = bytes.fromhex(sw[2:]).decode("ASCII")
        log.info(f"Memory value OK...{k}")

    def regErrInfo(self):
        log.warning(
            f"Register {self.getRegisterName()} value: {self.getRegisterVal()} expected: {self.CT.expectedValue}")
        self.simulator.printRegisterFile()

    def validateRegister(self):
        reg = int(self.CT.destination)
        regValue = fromUnsignedWordToSignedWord(
            self.simulator.registerFile.register[reg])
        assert regValue == int(self.CT.expectedValue)
        log.info("Register value OK...")

class TestMips():
    cwd = os.path.dirname(os.path.abspath(__file__))
    testFolder = os.path.join(cwd, "memfiles/")
    valTestFiles = ["add1.mem", "add2.mem", "addu1.mem", "addu2.mem", "and.mem", 
                    "beq1.mem", "beq2.mem", "beq3.mem", "beq4.mem", "bne1.mem", "bne2.mem", "bne3.mem", 
                    "break1.mem", "break2.mem", "jump1.mem", "jump2.mem", "lui1.mem", "lui2.mem",
                    "lw.mem", "nop.mem", "nor1.mem", "nor2.mem", "or1.mem", "or2.mem",
                    "slt.mem", "sub1.mem", "sub2.mem", "subu.mem", "sw1.mem", "sw2.mem"]
    trapTestFiles = ["trap_add.mem", "trap_sub1.mem", "trap_sub2.mem"]
    mipsWrapper = None
    currentSubTest = None
    trap = True
    exception = None
    testName = None

    def _setupTest(self, test, trap):
        log.debug(f"Setting up test: {test}")
        self.mipsWrapper = MipsWrapper(
            self.cwd, self.testFolder, test, trap)
        if trap:
            self.exception = Overflow
        else:
            self.exception = Break

    def _prepareSubTest(self, subtest):
        log.debug(f"Preparing {subtest.name}")
        self.currentSubTest = subtest
        self.mipsWrapper.prepare(subtest)

    def _runTrapTest(self):
        log.debug(f"Running: {self.currentSubTest.name} ")
        with pytest.raises(self.exception):
            self.mipsWrapper._runSimulator()
        log.info("Trapps OK...")
        self.mipsWrapper.addTrapPoint()

    def _runValTest(self):
        log.debug(f"Running: {self.currentSubTest.name} ")
        with pytest.raises(self.exception):
            self.mipsWrapper._runSimulator()
        log.debug(f"Simulator ticks: {self.mipsWrapper.simulator.nCycles}")
        self._validateResult()

    def _validateResult(self):
        log.debug(f"Validating {self.currentSubTest.name} ")
        self.mipsWrapper.validateRun()

    @ pytest.mark.parametrize('test', trapTestFiles)
    def test_trap(self, test):
        self._setupTest(test, self.trap)
        for _, subtest in self.mipsWrapper.tests.items():
            log.debug(f"Starting test: {subtest.name}")
            try:
                self._prepareSubTest(subtest)
                self._runTrapTest()
            except AssertionError as ae:
                pytest.fail(
                    f"Assertion error while running test: {test} {ae}")
            except Break as b:
                pytest.fail(f"Excepted {self.exception} caught {b}")
            except Overflow as ovf:
                pytest.fail(f"Excepted {self.exception} caught {ovf}")
            except Exception as e:
                pytest.fail(f"Unexpected exception: {e}")

    @ pytest.mark.parametrize('test', valTestFiles)
    def test_val(self, test):
        self._setupTest(test, not self.trap)
        for _, subtest in self.mipsWrapper.tests.items():
            log.debug(f"Starting test: {subtest.name}")
            try:
                self._prepareSubTest(subtest)
                self._runValTest()
            except AssertionError as ae:
                pytest.fail(
                    f"Assertion error while running test: {test} {ae}")
            except ValueError as ve:
                pytest.fail(f"{ve}")
            except Exception as e:
                pytest.fail(f"Unexpected exception: {e}")


if __name__ == "__main__":
    print("Run: pytest [-flags].. Ex: pytest -rPf")
