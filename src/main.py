import sys
from simulation import Simulation

if __name__ == "__main__":
    cycles = sys.argvs[1]
    transaction_size = sys.argvs[2]
    start_prob = sys.argvs[3]
    write_prob = sys.argvs[4]
    rollback_prob = sys.argvs[5]
    timeout = sys.argvs[6]
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout)