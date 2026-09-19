'''
Code written for inf-2200, University of Tromso
'''

import sys
from mipsSimulator import MIPSSimulator

def runSimulator(sim: MIPSSimulator):
    # Replace this with your own main loop!
    while (1):
        sim.tick()
        print(hex(sim.pc.currentAddress.value))

if __name__ == '__main__':
    assert len(sys.argv) == 2, f"Usage: python {sys.argv[0]} memoryFile"
    memoryFile = sys.argv[1]
    
    simulator = MIPSSimulator(memoryFile)
    runSimulator(simulator)
