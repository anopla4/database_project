from random import randint
from utils import generate_discrete_var
from transaction import Transaction, ACTIVE, BLOCKED, TERMINATED
from log_manager import LogManager, StartRecord, OperationRecord, RollbackRecord, CommitRecord
from recovery_manager import RecoveryManager
from lock_manager import LockManager, SHARED
import json

class Simulation():
    def __init__(self, cycles, transaction_size, start_prob, write_prob, rollback_prob, timeout, testing=False) -> None:
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
        # lock manager
        self.lock_manager = LockManager()
        # data
        self.data = []
        # number of write operations
        self.write_operations = 0

        # testing mode
        self.testing = testing

    def validate_args(self):
        if self.write_prob + self.rollback_prob > 1:
            raise Exception("The write probability plus the rollback probability should be less than or equal to one.")

    def start_transaction(self):
        var = generate_discrete_var([0, 1], [1 - self.start_prob, self.start_prob])
        return var
    
    def get_operation(self):
        var = generate_discrete_var([0, 1, 2], [1 - self.write_prob - self.rollback_prob, self.write_prob, self.rollback_prob])

        if var <= 1:
            data_id = randint(0, 31)
            old_value = self.data[data_id]
            return var, data_id, old_value
        return var, None, None
    
    def get_record(self, op, trid, data_id, old_value):
        return OperationRecord(trid, data_id, old_value, old_value ^ 1) if op == 1 else RollbackRecord(trid)
    
    def load_data(self):
        db_path = ""
        with open("src\config.json") as fp:
            db_path = json.load(fp)["db_loc"]

        with open(db_path) as fp:
            content = fp.read().split()
            self.data = [int(i) for i in content]

    def update_data(self):
        db_path = ""
        with open("src\config.json") as fp:
            db_path = json.load(fp)["db_loc"]
        
        with open(db_path, 'w') as fp:
            fp.write(" ".join([str(i) for i in self.data]))

    def perform_write(self, data_id, trid, old_value):
        self.write_operations += 1
        if self.testing:
            print(f"REQUESTING LOCKS: trid: {trid}, data_id {data_id}")
        is_lock_granted = self.lock_manager.request_lock(data_id, trid)

        if is_lock_granted:
            if self.testing:
                print(f"WRITE UPDATE LOG RECORD+++++++++++++++")
            # write log record
            self.log_manager.add_record(self.get_record(1, trid, data_id, old_value))
            self.data[data_id] ^= 1
        else:
            self.transactions[trid].state = BLOCKED

    def perform_read(self, data_id, trid):
        is_lock_granted = self.lock_manager.request_lock(data_id, trid, mode=SHARED)

        if not is_lock_granted:
            self.transactions[trid].state = BLOCKED

    def perform_rollback(self, trid):
        self.recovery_manager.rollback_transaction(self.data, self.log_manager, trid)
        self.log_manager.add_record(RollbackRecord(trid))
        self.transactions[trid].state = TERMINATED

        self.log_manager.write_to_disk()
        self.log_manager.flush_records()

        self.lock_manager.release_locks(trid)

    def perform_commit(self, trid):
        self.log_manager.add_record(CommitRecord(trid))

        self.log_manager.write_to_disk()
        self.log_manager.flush_records()

        self.lock_manager.release_locks(trid)

    def perform_operation(self, op, data_id, trid, old_value=None):
        # read
        if op == 0:
            self.perform_read(data_id, trid)
        # write
        elif op == 1:
            self.perform_write(data_id, trid, old_value)
        # rollback
        else:
            self.perform_rollback(trid)

    def start(self):
        i = 0
        self.load_data()
        self.log_manager.read_from_disk()
        self.recovery_manager.recover(self.data, self.log_manager)
        self.update_data()
        self.log_manager.empty_log()

        while i < self.cycles:
            # start transaction
            if self.start_transaction():
                id_ = len(self.transactions)
                if self.testing:
                    print(f"START TRANSACTION {id_}+++++++++++++++")
                t = Transaction(id_)
                self.transactions[id_] = t
                self.active_transactions[id_] = t
                self.log_manager.add_record(StartRecord(id_))

            if self.testing:
                print("EXECUTE ACTIVE TRANSACTIONS+++++++++++++++")
            # execute active transactions
            for trid in self.transactions:
                transaction  = self.transactions[trid]
                state = transaction.state

                if state == ACTIVE:

                    
                    # increase number of cycles the transaction has been executing
                    transaction.cycles_in_execution += 1
                
                    # submit operation
                    op, data_id, old_value = self.get_operation()
                    if self.testing:
                        print(f"SUBMIT OPERATION: trid: {trid}, data item: {data_id}+++++++++++++++")
                    # try to perform operation: read, write or rollback
                    self.perform_operation(op, data_id, trid, old_value)
                    # increase number of transaction submitted operations
                    transaction.operations_submitted += 1
                    
                    # update database every 25 write operations (first cycle ignored since database was just read)
                    # TODO: change to 25
                    if self.write_operations > 0 and self.write_operations % 1 == 0:
                        if self.testing:
                            print(f"UPDATE DATABASE: number of operations submitted {self.write_operations}+++++++++++++++")

                        self.log_manager.write_to_disk()
                        self.log_manager.flush_records()
                        self.update_data()
                    
                    # terminate transaction that reached the maximum number of operations
                    if transaction.state != TERMINATED and transaction.operations_submitted == self.transaction_size:
                        if self.testing:
                            print(f"TERMINATE TRANSACTION {trid}+++++++++++++++")
                        self.perform_commit(trid)
                        transaction.state = TERMINATED
                        continue

                    # rollback transaction in deadlock
                    if transaction.state != TERMINATED and transaction.cycles_in_execution == self.timeout:
                        if self.testing:
                            print(f"ROLLBACK TRANSACTION {trid}+++++++++++++++")
                        self.perform_rollback(trid)
                        transaction.state = TERMINATED
                        continue
            if self.testing:
                print(f"UNBLOCK TRANSACTIONS+++++++++++++++")
            # unblock transactions
            for trid in self.transactions:
                transaction  = self.transactions[trid]
                if transaction.state == BLOCKED and not self.lock_manager.is_blocked(trid, None):
                    if self.testing:
                        print(f"UNBLOCKING TRANSACTION {trid}+++++++++++++++")
                    transaction.state = ACTIVE

            i += 1

