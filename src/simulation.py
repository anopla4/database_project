class Simulation:
    def __init__(self, cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout) -> None:
        self.cycles = cycles
        self.transaction_size = transaction_size
        self.start_prob = start_prob
        self.write_prob = write_prob
        self.rollback_prob = rollback_prob
        self.timeout = timeout
