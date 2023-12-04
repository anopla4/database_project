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
    def __add_new(self, hashed_data_id, data_id, trid, mode):
        # new lock table data item entry
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

    def insert(self, data_id, trid, mode):
        hashed_data_id = hash(data_id)
        status = GRANTED
        # transaction node in the data item transaction waiting list
        tr_node = None

        # data id is in table
        if hashed_data_id in self.table:
            # get doubly linked list of the data item with id data_id
            data_id_doubly_linked_list = self.table[hashed_data_id]
            length = data_id_doubly_linked_list.length()

            # check for collisions
            is_data_item_locked, node = data_id_doubly_linked_list.search(data_id)

            # check the transactions list for that data item
            if is_data_item_locked:
                transactions = node.arguments["transactions"]
                data_item_node = transactions.find_by_position(length - 1)
                data_item_trid = data_item_node.id
                data_item_mode = data_item_node.arguments["mode"]
                data_item_status = data_item_node.arguments["status"]

                # grant lock if it's compatible with the granted ones and the last transaction was granted the lock
                if data_item_status == GRANTED and data_item_mode == SHARED and mode == SHARED:
                    transactions.insertAtEnd(trid, mode=mode, status=GRANTED)
                # block transaction in other case
                else:
                    status = BLOCKED
                    transactions.insertAtEnd(trid, mode=mode, status=BLOCKED)
                tr_node = data_item_node.next
            # no collisions, new data_id
            else:
                tr_node = self.__add_new(hashed_data_id, data_id, trid, mode)
                
        # new data id
        else:
            tr_node = self.__add_new(hashed_data_id, data_id, trid, mode)

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
        data_item_tr_list.delete(trid)
        if data_item_tr_list.isEmpty():
            data_id_hash_list = self.table[hash(data_id)]
            data_id_hash_list.delete(data_id)
            if data_id_hash_list.isEmpty():
                self.table.pop(data_id)

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
            text += f"{data_id}:\n   {str(self.table[data_id])}\n"

        return text

x = LockTable()
x.insert(30, 0, "X")
# print("------")
x.insert(30, 1, "X")
# print("------")
x.insert(29, 1, "X")
# print(x)
# print("Transactions++++++++++")
# print("\n-----\n".join([f'{tr}: {str(x.transactions[tr])}' for tr in x.transactions]))
# print("Delete testing++++++")
# x.delete_transaction(1)
# print("Transactions>>>>>")
# # print(x.transactions)
# print("\n-----\n".join([f'{tr}: {str(x.transactions[tr])}' for tr in x.transactions]))
# print("Lock table>>>>>")
# print(x)
print("Transaction status>>>>>>")
print(x.find_transaction_status(1, 29))
print(x.find_transaction_status(1, 30))