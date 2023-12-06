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
                if isinstance(log, StartRecord):
                    break
                if isinstance(log, OperationRecord):
                    data_id = log.data_id
                    old_value = log.old_value
                    data[data_id] = old_value
                    log_manager.add_record(CompensationLogRecord(trid, old_value))

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

            if id_ in active_transactions:
                if isinstance(log_record, StartRecord):
                    active_transactions.remove(id_)
                else:
                    data_id = log_record.data_id
                    old_value = log_record.old_value
                    data[data_id] = old_value
                    log_manager.add_record(CompensationLogRecord(id_, old_value))

            i -= 1

    def redo(self, data, logs):
        active_transactions = []
        for log_record in logs:
            id_ = log_record.id
            if isinstance(log_record, OperationRecord) or isinstance(log_record, CompensationLogRecord):
                data_id = log_record.data_id
                val = log_record.value
                data[data_id] = val
            elif isinstance(log_record, StartRecord):
                active_transactions.append(id_)
            elif isinstance(log_record, CommitRecord) or isinstance(log_record, RollbackRecord):
                active_transactions.remove(id_)

        return active_transactions
