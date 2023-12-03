from random import randint
from utils import generate_discrete_var
from transaction import Transaction
from log_manager import LogManager, StartRecord, OperationRecord, RollbackRecord
from recovery_manager import RecoveryManager
import json

class Simulation():
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
        # log manager
        self.log_manager = LogManager()
        # recovery manager
        self.recovery_manager = RecoveryManager()
        # data
        self.data = []

    def validate_args(self):
        pass

    def start_transaction(self):
        var = generate_discrete_var([0, 1], [1 - self.start_prob, self.start_prob])
        return var
    
    def get_operation(self):
        var = generate_discrete_var([0, 1, 2], [1 - self.write_prob - self.rollback_prob, self.write_prob, self.rollback_prob])

        if var == 1:
            data_id = randint(0, 31)
            old_value = self.data[data_id]
            return var, data_id, old_value
        return var, None, None
    
    def get_record(self, op, trid, data_id, old_value):
        return OperationRecord(trid, data_id, old_value) if op == 1 else RollbackRecord(trid)
    
    def load_data(self):
        db_path = ""
        with open("src\config.json") as fp:
            db_path = json.load(fp)["db_loc"]

        with open(db_path) as fp:
            self.data = fp.read().split()

    def perform_write(self):
        pass

    def perform_rollback():
        pass


    def start(self):
        i = 0
        self.load_data()
        self.log_manager.read_from_disk()
        self.recovery_manager.recover(self.data, self.log_manager)
        while i < self.cycles:
            # start transaction
            if self.start_transaction():
                id_ = len(self.transactions)
                t = Transaction(id_)
                self.transactions[id_] = t
                self.active_transactions[id_] = t
                self.log_manager.add_record(StartRecord(id_))

            # execute active transactions
            for act_tran in self.active_transactions:
                op, data_id, old_value = self.get_operation()
                if op:
                    self.log_manager.add_record(self.get_record(op, act_tran, data_id, old_value))

            i += 1

        self.log_manager.write_to_disk()

