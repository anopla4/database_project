from log_manager import OperationRecord, CompensationLogRecord, StartRecord, CommitRecord, RollbackRecord
class RecoveryManager():
    def __init__(self) -> None:
        pass

    def rollback_transaction(self, data, log_manager, trid):
        old_records = log_manager.load_flushed_logs() 
        records = old_records + log_manager.log_records
        i = len(records) - 1
        while i >= 0:
            log = records[i]
            if log.id == trid:
                # stop when the start log is found
                if isinstance(log, StartRecord):
                    break
                # undo the write and add compensation log record
                if isinstance(log, OperationRecord):
                    data_id = log.data_id
                    old_value = log.old_value
                    data[data_id] = old_value
                    log_manager.add_record(CompensationLogRecord(trid, data_id, old_value))

            i -= 1


    def recover(self, data, log_manager):
        records = log_manager.log_records
        active_transactions = self.redo(data, records)
        self.undo(data, records, log_manager, active_transactions)
        log_manager.flush_records()

    def undo(self, data, logs, log_manager, active_transactions):
        i = len(logs) - 1
        while i >= 0 and len(active_transactions):
            log_record = logs[i]
            id_ = log_record.id
            # check if transaction is active
            if id_ in active_transactions:
                # if the start log record is found, remove from the active transactions list
                if isinstance(log_record, StartRecord):
                    active_transactions.remove(id_)
                # undo write operation and add compensation log record
                else:
                    data_id = log_record.data_id
                    old_value = log_record.old_value
                    data[data_id] = old_value
                    log_manager.add_record(CompensationLogRecord(id_, data_id, old_value))

            i -= 1

    def redo(self, data, logs):
        active_transactions = []
        for log_record in logs:
            id_ = log_record.id
            # redo write operation and compensation logs
            if isinstance(log_record, OperationRecord) or isinstance(log_record, CompensationLogRecord):
                data_id = log_record.data_id
                val = log_record.value
                data[data_id] = val
            # if a transaction starts, add it to the list of active transactions
            elif isinstance(log_record, StartRecord):
                active_transactions.append(id_)
            # if a transaction commits or rolls back, remove it from the list of active transactions
            elif isinstance(log_record, CommitRecord) or isinstance(log_record, RollbackRecord):
                active_transactions.remove(id_)

        return active_transactions
