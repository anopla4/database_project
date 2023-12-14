# Transaction Management System Simulation

## Instructions

You can run the simulation using one of the following alternatives:

  - **Config file**: You can change the simulation parameters in the config.json file provided in the solution, and then run the following command:
    `python src//main.py`   
If you want to enable testing comments, you can change the *testing* field in the config.json file.
If you want to force the commit of the transactions at the end of the simulation, you can change the *force_commit* field in the config.json file.
  - **Command line arguments**: You can provide the simulation parameters as command line arguments and run the following command:
    `python src//main.py <cycles> <transaction_size> <start_prob> <write_prob> <rollback_prop> <timeout>`
If you want to enable testing comments, you can run the following command:
    `python src//main.py <cycles> <transaction_size> <start_prob> <write_prob> <rollback_prop> <timeout> test`
If you want to force the commit of the transactions at the end of the simulation, you can run the following command:

    `python src//main.py <cycles> <transaction_size> <start_prob> <write_prob> <rollback_prop> <timeout> force_commit`

## Overview

### Simulation flow

The simulation of the transactions management system includes the following stages:
  - **Load logs and data from the disk**: Reads the data and log records from the src//db and src//log files, respectively.
  - **Recover**: The recovery manager applies the logs to the data. It performs redo and undo phases. Then, it writes the data to the disk and empties the log file.
  - **Run cycles**: Below, there is a description of the operations made in each cycle.

For each cycle in the simulation:
  - **Start transaction**: A transaction starts with start_prob probability.
  - **For each active transaction**:
    - If the transaction reaches the maximum number of operations, it commits.
    - If the transaction has been running for timeout cycles, it rolls back.
    - If none of the above occur, the transaction submits an operation (rollback or write).
    - If the number of write operations in the simulations becomes a multiple of 25, it writes the data to the disk.
  - **Unblock transactions**: Update the state of transactions in the simulation list after all have been run.

### Lock manager

The lock manager uses the lock table described in Section 18.1.4 of the textbook. It uses a hash table on the data ids. It stores a double-linked list for each of the hashed data ids. Each node in this linked list represents a data id, and points to another linked list of transactions that requested a lock on that data item. Some of these transactions may have been granted the lock, while others might be blocked.

The lock manager also keeps a list of the locks requested by each transaction. Each of the locks in a transaction locks list points to the locks in the hash table.

It prints "No locks to be released. Transaction id not in lock table." when the transaction does not hold any locks. This likely when the transaction rolls back right after it started.

### Log manager

The log manager keeps a list of the log records that have not been flushed. Logs are flushed when a transaction commits or aborts, or before the data on the disk is updated. There are five different types of log records:

  - StartRecord (trid,S): a transaction started.
  
  - OperationRecord (trid,data_id,old_value,new_value,F): a transaction performed a write.

  - RollbackRecord (trid,R): a transaction rolled back.

  - CommitRecord (trid,C): a transaction committed.

  - CompensationLogRecord (trid, data\_id, value, CLR): a transaction was rolled back during recovery.

The recovery manager performs the recovery when a simulation is started. This includes the redo and undo phases. It also rolls back a transaction whenever a rollback operation is submitted.
