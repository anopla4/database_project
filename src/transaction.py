ACTIVE = "active"
BLOCKED = "blocked"
TERMINATED = "terminated"
class Transaction():
    def __init__(self, id_) -> None:
        self.id = id_
        self.state = ACTIVE
        self.operations_submitted = 0
        self.cycles_blocked = 0

class Operation():
    def __init__(self, tran_id) -> None:
        self.trid = tran_id
class WriteOperation(Operation):
    def __init__(self, tran_id, data_id, old_val) -> None:
        super().__init__(tran_id)
        self.data_id = data_id
        self.old_value = old_val

class RollbackOperation(Operation):
    def __init__(self, tran_id) -> None:
        super().__init__(tran_id)

class CommitOperation(Operation):
    def __init__(self, tran_id) -> None:
        super().__init__(tran_id)