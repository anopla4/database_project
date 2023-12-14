from lock_table import LockTable, EXCLUSIVE, BLOCKED, SHARED
class LockManager():
    def __init__(self) -> None:
        self.lock_table = LockTable()

    def request_lock(self, data_id, trid, mode=EXCLUSIVE):
        is_granted = self.lock_table.insert(data_id, trid, mode)

        return is_granted

    def release_locks(self, trid):
        self.lock_table.delete_transaction(trid)

    def unlock_data_item(self, data_id, trid):
        self.lock_table.delete_data_item_lock(trid, data_id)

    def is_blocked(self, trid, data_id):
        temp = self.lock_table.transactions[trid].head
        while temp != None:
            id_ = temp.id
            if self.lock_table.find_transaction_status(trid, id_) == BLOCKED:
                return True
            temp = temp.next
        return False