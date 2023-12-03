import json
import os
class LogManager():
    def __init__(self) -> None:
        self.log_records = []

    def add_record(self, log_record):
        self.log_records.append(log_record)

    def write_to_disk(self):
        log_path = ""
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
        log_text = "\n".join([str(lr) for lr in self.log_records])
        
        with open(log_path, 'a') as fp:
            log_text = log_text if os.path.getsize(log_path) else log_text[1:]
            fp.write(log_text)
            fp.close()

    def read_from_disk(self):
        log_path = ""
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
            fp.close()
        with open(log_path) as fp:
            self.log_records = fp.read().split('\n')
            fp.close()

    def flush_records(self):
        self.log_records = []

class LogRecord():
    def __init__(self, id_) -> None:
        self.id = id_

    def __str__(self) -> str:
        return str(self.id)

class StartRecord(LogRecord):
    def __init__(self, id_) -> None:
        super().__init__(id_)

    def __str__(self) -> str:
        return str(self.id) + ",S"

class OperationRecord(LogRecord):
    def __init__(self, id_, data_id, old_value) -> None:
        super().__init__(id_)
        self.data_id = data_id
        self.old_value = old_value

    def __str__(self) -> str:
        return f"{self.id},{self.data_id},{self.old_value},F"

class RollbackRecord(LogRecord):
    def __init__(self, id_) -> None:
        super().__init__(id_)

    def __str__(self) -> str:
        return str(self.id) + ",R"

class CommitRecord(LogRecord):
    def __init__(self, id_) -> None:
        super().__init__(id_)

    def __str__(self) -> str:
        return str(self.id) + ",C"