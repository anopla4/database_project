from lock_table import LockTable, EXCLUSIVE, BLOCKED
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
        return self.lock_table.find_transaction_status(trid, data_id) == BLOCKED

if __name__ == "__main__":
    x = LockManager()
    x.request_lock(30, 0)
    x.request_lock(30, 1)
    x.request_lock(29, 1, mode="S")
    x.request_lock(29, 2, mode="S")
    x.request_lock(29, 3)


    print("-----------------------------------------------------------")
    print(x.lock_table)
    print("-----------------------------------------------------------")

    print("Unlock data item++++++")
    x.unlock_data_item(30, 0)

    print("-----------------------------------------------------------")
    print(x.lock_table)
    print("-----------------------------------------------------------")
    
    print("Release locks++++++")
    x.release_locks(2)

    print("-----------------------------------------------------------")
    print(x.lock_table)
    print("-----------------------------------------------------------")