import sys
from simulation import Simulation
import json

if __name__ == "__main__":
    cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout = [None] * 6
    # load arguments from config file
    if len(sys.argv) < 2:
        try:
            config = {}
            with open("src\config.json") as fp:
                config = json.load(fp)
            cycles = config["cycles"]
            transaction_size = config["transaction_size"]
            start_prob = config["start_prob"]
            write_prob = config["write_prob"]
            rollback_prob = config["rollback_prob"]
            timeout = config["timeout"]
        except Exception as e:
            print(e)
    # read arguments from command line 
    else:
        cycles = sys.argvs[1]
        transaction_size = sys.argvs[2]
        start_prob = sys.argvs[3]
        write_prob = sys.argvs[4]
        rollback_prob = sys.argvs[5]
        timeout = sys.argvs[6]

    # start simulation
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout)
    simulation.start()