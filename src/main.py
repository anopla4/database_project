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
            testing = config["testing"]
        except Exception as e:
            print(e)
    # read arguments from command line 
    else:
        if len(sys.argv) < 7:
            raise Exception("There are some arguments missing, you should provide: <cycles> <transaction_size> <start_prob> <write_prob> <rollback_prop> <timeout>.")
        if len(sys.argv) > 8:
            raise Exception("There are more arguments than required, you should provide: <cycles> <transaction_size> <start_prob> <write_prob> <rollback_prop> <timeout>.")

        cycles = int(sys.argv[1])
        transaction_size = int(sys.argv[2])
        start_prob = float(sys.argv[3])
        write_prob = float(sys.argv[4])
        rollback_prob = float(sys.argv[5])
        timeout = int(sys.argv[6])
        testing = False
        if len(sys.argv) == 8 and sys.argv[7] == "test":
            testing = True

    # start simulation
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout, testing=testing)
    simulation.start()