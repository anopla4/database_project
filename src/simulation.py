from utils import proceed
from transaction import Transaction

class Simulation:
    def __init__(self, cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout) -> None:
        # maximum number of cycles for the simulation
        self.cycles = cycles
        # size of the transactions in number of operations
        self.transaction_size = transaction_size
        # probability of a transaction starting per cycle
        self.start_prob = start_prob
        # probability of a write operation
        self.write_prob = write_prob
        # probability of a rollback operation
        self.rollback_prob = rollback_prob
        # timeout wait
        self.timeout = timeout

        # validate arguments
        self.validate_args()

        # transactions
        self.transactions = {}
        # active transactions
        self.active_transactions = {}
        # blocked transactions
        self.blocked_transactions = {}

    def validate_args(self):
        pass

    def start(self):
        i = 0
        while i < self.cycles:
            # start transaction
            if proceed(self.start_prob):
                id_ = len(self.transactions)
                t = Transaction(id_)
                self.transactions[id_] = t
                self.active_transactions[id_] = t

