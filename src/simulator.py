'''
Code written for inf-2200, University of Tromso
'''

import sys
from mipsSimulator import MIPSSimulator

def runSimulator(sim: MIPSSimulator):
    # Replace this with your own main loop!
    running = True
    while running:
        sim.tick()
        #print(hex(sim.instructionMemory.outgoingInstruction.value))
        
        
        #i = input("")
        #if i == "exit" or i == "quit" or i == "q":
        #    break

if __name__ == '__main__':
    assert len(sys.argv) == 2, f"Usage: python {sys.argv[0]} memoryFile"
    memoryFile = sys.argv[1]
    
    simulator = MIPSSimulator(memoryFile)
    runSimulator(simulator)
