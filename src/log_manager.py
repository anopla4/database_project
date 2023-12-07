import json
import os
class LogManager():
    def __init__(self) -> None:
        self.log_records = []
        self.parser = LogParser()

    def add_record(self, log_record):
        self.log_records.append(log_record)

    def empty_log(self):
        log_path = ""
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
        with open(log_path, 'w') as fp:
            fp.write("")
            fp.close()

    def write_to_disk(self):
        if not len(self.log_records):
            return
        log_path = ""
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
        log_text = "\n".join([str(lr) for lr in self.log_records])
        with open(log_path, 'a') as fp:
            log_text = log_text if os.path.getsize(log_path) else log_text
            fp.write(log_text + "\n")
            fp.close()

    def read_from_disk(self):
        log_path = ""
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
            fp.close()
        if os.path.getsize(log_path):
            with open(log_path) as fp:
                text = fp.read().split('\n')
                self.log_records = [self.parser.parse(lr) for lr in text if lr != ""]
                fp.close()

    def load_flushed_logs(self):
        log_path = ""
        records = []
        with open("src\config.json") as fp:
            log_path = json.load(fp)["log_loc"]
            fp.close()
        with open(log_path) as fp:
            if os.path.getsize(log_path):
                records = [self.parser.parse(lr) for lr in fp.read().split('\n') if lr != ""]
            fp.close()

        return records

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
    def __init__(self, id_, data_id, old_value, value) -> None:
        super().__init__(id_)
        self.data_id = data_id
        self.old_value = old_value
        self.value = value

    def __str__(self) -> str:
        return f"{self.id},{self.data_id},{self.old_value},{self.value},F"

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
    
class CompensationLogRecord(LogRecord):
    def __init__(self, id_, data_id, val) -> None:
        super().__init__(id_)
        self.data_id = data_id
        self.value = val

    def __str__(self) -> str:
        return f"{self.id},{self.data_id},{self.value},CLR"
    
class LogParser:
    def __init__(self) -> None:
        pass

    def parse(self, log_record):
        args = log_record.split(",")
        log_type = args[-1]
        id_ = int(args[0])

        if log_type == "S":
            return StartRecord(id_)
        if log_type == "C":
            return CommitRecord(id_)
        if log_type == "R":
            return RollbackRecord(id_)
        if log_type == "CLR":
            data_id = int(args[1])
            value = int(args[2])
            return CompensationLogRecord(id_, data_id, value)
        if log_type == "F":
            data_id = int(args[1])
            old_value = int(args[2])
            value = int(args[3])
            return OperationRecord(id_, data_id, old_value, value)
        return None