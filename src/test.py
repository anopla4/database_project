from simulation import Simulation

def test():
    with open("src\db", 'w') as fp:
        fp.write(" ".join(["0"] * 32))
    with open("src\log.csv", 'w') as fp:
        fp.write("")

    cycles = 1000
    transaction_size = 3
    start_prob = 1
    write_prob = 0.5
    rollback_prob = 0
    timeout = 10
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout, force_commit=True)
    simulation.start()

    prev_data = ""
    with open("src\db") as fp:
        prev_data = fp.read()

    transaction_size = 1001
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout, remove=True)
    simulation.start()

    cycles = 0
    simulation = Simulation(cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout)
    simulation.start()

    curr_data = ""
    with open("src\db") as fp:
        curr_data = fp.read()

    print(curr_data == prev_data)

if __name__ == "__main__":
    for i in range(10):
        test()