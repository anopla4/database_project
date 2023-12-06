from double_linked_list import DoublyLinkedList

GRANTED = "granted"
BLOCKED = "blocked"
EXCLUSIVE = "X"
SHARED = "S"

class LockTable():
    def __init__(self) -> None:
        self.table = {}
        self.transactions = {}

    # add new transaction lock request to lock table
    def __add_new(self, data_id, trid, mode):
        # new lock table data item entry
        hashed_data_id = hash(data_id)
        self.table[hashed_data_id] = DoublyLinkedList()
        data_id_doubly_linked_list = self.table[hashed_data_id]

        # transactions waiting list for data item
        transactions = DoublyLinkedList()
        transactions.insertAtBeginning(trid, mode=mode, status=GRANTED)

        # insert in the new lock table data item entry
        data_id_doubly_linked_list.insertAtBeginning(data_id, transactions=transactions)
        return transactions.head
        

    # add new transaction lock request to transactions list
    def __add_to_transactions(self, trid, data_id, trid_node=None):
        # new transaction
        if trid not in self.transactions:
            tr_list = DoublyLinkedList()
            tr_list.insertAtBeginning(data_id, node=trid_node)
            self.transactions[trid] = tr_list

        # add request to already added transaction
        else:
            tr_list = self.transactions[trid]
            tr_list.insertAtEnd(data_id, node=trid_node)

    # remove transaction lock request from transactions list
    def __remove_from_transactions(self, trid, data_id):
        if trid not in self.transactions:
            print("Transaction id not in lock table.")
            return
        tr_list = self.transactions[trid]
        tr_list.delete(data_id)

    def get_transactions_with_granted_locks(self, data_id):
        count = 0
        transactions_with_granted_locks = []
        if hash(data_id) in self.table:
            temp = self.find_data_item_transactions_list(data_id).head
            while temp != None:
                if temp.arguments["status"] == GRANTED:
                    transactions_with_granted_locks.append(temp)
                    count += 1
                temp = temp.next
        return transactions_with_granted_locks, count

    def upgrade_lock(self, trid, data_id):
        tr_node = self.find_data_item_transactions_list(data_id).search(trid)
        tr_node.arguments["mode"] = EXCLUSIVE

    def downgrade_lock(self, trid, data_id):
        tr_node = self.find_data_item_transactions_list(data_id).search(trid)
        tr_node.arguments["mode"] = SHARED
        data_item_tr_list = self.find_data_item_transactions_list(data_id)
        self.__grant_locks(trid, data_item_tr_list)

    # insert in lock table
    def insert(self, data_id, trid, mode):
        hashed_data_id = hash(data_id)
        status = GRANTED
        # transaction node in the data item transaction waiting list
        tr_node = None
        # number of granted locks for the data item
        transactions_with_granted_locks, number_of_granted_locks = self.get_transactions_with_granted_locks(data_id)

        # data id is in table
        if hashed_data_id in self.table:
            # get doubly linked list of the data item with id data_id
            data_id_doubly_linked_list = self.table[hashed_data_id]
            # check for collisions
            is_data_item_locked, node = data_id_doubly_linked_list.search(data_id)

            # check the transactions list for that data item
            if is_data_item_locked:
                transactions = node.arguments["transactions"]
                data_item_node = transactions.find_by_position(transactions.length() - 1)
                data_item_mode = data_item_node.arguments["mode"]
                data_item_status = data_item_node.arguments["status"]

                # if the transaction is holding the lock then, if it's in the same mode, we don't do anything, if not,
                # we change it
                transaction_locks_list_for_data_id = [tr for tr in transactions_with_granted_locks if trid == tr.id]
                is_transaction_holding_lock = len(transaction_locks_list_for_data_id)
                if is_transaction_holding_lock:
                    transaction_lock = transaction_locks_list_for_data_id[0]
                    transaction_lock_mode = transaction_lock.arguments["mode"]
                    if transaction_lock_mode == SHARED and mode == EXCLUSIVE:
                        if number_of_granted_locks:
                            self.upgrade_lock(trid, data_id)
                        else:
                            self.delete_data_item_lock(trid, data_id)
                            tr_node = self.__add_new(data_id, trid, mode)
                            # add corresponding element to the transactions list
                            self.__add_to_transactions(trid, data_id, tr_node)
                    elif transaction_lock_mode == EXCLUSIVE and mode == SHARED:
                        self.downgrade_lock(trid, data_id)
                    return transaction_lock

                # grant lock if the last transaction was granted the lock and it's compatible with the granted ones or 
                # is held by the same transaction but the mode is shared or the only transaction holding locks over the 
                # data item is trid
                elif data_item_status == GRANTED:
                    if self.__is_compatible(data_item_mode, mode) or (is_transaction_holding_lock and mode == SHARED):
                        transactions.insertAtEnd(trid, mode=mode, status=GRANTED)
                    

                # block transaction in other case
                else:
                    status = BLOCKED
                    transactions.insertAtEnd(trid, mode=mode, status=BLOCKED)
                tr_node = data_item_node.next
            # no collisions, new data_id
            else:
                tr_node = self.__add_new(data_id, trid, mode)
                
        # new data id
        else:
            tr_node = self.__add_new(data_id, trid, mode)

        # add corresponding element to the transactions list
        self.__add_to_transactions(trid, data_id, tr_node)

        return status == GRANTED

    # delete all lock requests of a transaction from the  transactions list and the lock table
    def delete_transaction(self, trid):
        if trid not in self.transactions:
            print("Transaction id not in lock table.")
            return
        # transactions locks list
        tr_list = self.transactions[trid]
        # for each lock, remove from the transaction lock list and the lock table
        while not tr_list.isEmpty():
            tr_node = tr_list.find_by_position(0)
            data_id = tr_node.id
            self.__delete_data_item_lock(data_id, trid)
            self.__remove_from_transactions(trid, data_id)
        # remove id from transactions list
        self.transactions.pop(trid)

    # delete a transaction lock request of a data item
    def __delete_data_item_lock(self, data_id, trid):
        # data item transaction lock request list in lock table
        data_item_tr_list = self.find_data_item_transactions_list(data_id)
        # grant locks before deleting transaction from list
        self.__grant_locks(trid, data_item_tr_list)

        data_item_tr_list.delete(trid)
        if data_item_tr_list.isEmpty():
            data_id_hash_list = self.table[hash(data_id)]
            data_id_hash_list.delete(data_id)
            if data_id_hash_list.isEmpty():
                self.table.pop(hash(data_id))

    def __is_compatible(self, m1, m2):
        return (m1 == "S" and m2 == "S")

    def __grant_locks(self, trid, data_item_tr_list):
        _, temp = data_item_tr_list.search(trid)
        temp = temp.next

        if temp != None:
            if temp.arguments["status"] == GRANTED:
                return
            if temp.previous.previous == None:
                temp.arguments["status"] = GRANTED
                temp = temp.next

        while temp != None:
            m1 = temp.previous.arguments["mode"]
            m2 = temp.arguments["mode"]

            if self.__is_compatible(m1, m2):
                temp.arguments["status"] = GRANTED
            else:
                break

    def delete_data_item_lock(self, trid, data_id):
        self.__delete_data_item_lock(data_id, trid)
        self.__remove_from_transactions(trid, data_id)

    # find the status of a transaction
    def find_transaction_status(self, trid, data_id):
        tr_list = self.transactions[trid]
        found, tr_node = tr_list.search(data_id)
        if found:
            return tr_node.arguments["node"].arguments["status"]

    # find data item transaction lock request list in lock table
    def find_data_item_transactions_list(self, data_id):
        data_id_hash = hash(data_id)
        if data_id_hash not in self.table:
            return None
        data_id_hash_list = self.table[data_id_hash]
        
        # find element with data_id in the data item entry in the lock table
        _, data_id_node = data_id_hash_list.search(data_id)
        return data_id_node.arguments["transactions"]

    def __str__(self):
        text = ""
        for data_id in self.table:
            text += f"{data_id}:\n   {str(self.table[hash(data_id)])}\n"

        return text

if __name__ == "__main__":

    x = LockTable()
    x.insert(30, 0, "X")
    # print("------")
    x.insert(30, 1, "X")
    # print("------")
    x.insert(29, 1, "S")
    x.insert(29, 2, "S")
    x.insert(29, 3, "X")
    # print(x)
    # print("Transactions++++++++++")
    # print("\n-----\n".join([f'{tr}: {str(x.transactions[tr])}' for tr in x.transactions]))

    print("\n-----\n".join([f'{tr}: {str(x.transactions[tr])}' for tr in x.transactions]))
    print("-----------------------------------------------------------")
    print("Delete testing++++++")
    x.delete_transaction(0)
    x.delete_transaction(2)
    print("-----------------------------------------------------------")
    print("Transactions>>>>>")
    print("\n-----\n".join([f'{tr}: {str(x.transactions[tr])}' for tr in x.transactions]))
    print("-----------------------------------------------------------")
    print("Lock table>>>>>")
    print(x)

    # print("Transaction status>>>>>>")
    # print(x.find_transaction_status(1, 29))
    # print(x.find_transaction_status(1, 30))