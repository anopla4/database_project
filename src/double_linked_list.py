class Node:
    def __init__(self, trid, mode, status):
        self.previous = None
        self.next = None
        self.trid = trid
        self.mode = mode
        self.status = status


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        if self.head is None:
            return True
        return False

    def length(self):
        temp = self.head
        count = 0
        while temp is not None:
            temp = temp.next
            count += 1
        return count
    
    def find_by_position(self, index):
        temp = self.head
        count = 0
        while count < index is not None:
            temp = temp.next
            count += 1
        return temp

    def search(self, trid):
        temp = self.head
        isFound = False
        while temp is not None:
            if temp.trid == trid:
                isFound = True
                break
            temp = temp.next
        return isFound

    def insertAtBeginning(self, trid, mode, status):
        new_node = Node(trid, mode, status)
        if self.isEmpty():
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node

    def insertAtEnd(self, trid, mode, status):
        new_node = Node(trid, mode, status)
        if self.isEmpty():
            self.insertAtBeginning(trid, mode, status)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node
            new_node.previous = temp

    def insertAfterElement(self, trid, mode, status, element):
        temp = self.head
        while temp is not None:
            if temp.trid == element:
                break
            temp = temp.next
        if temp is None:
            print("{} is not present in the linked list. {} cannot be inserted into the list.".format(element, value))
        else:
            new_node = Node(trid, mode, status)
            new_node.next = temp.next
            new_node.previous = temp
            temp.next.previous = new_node
            temp.next = new_node

    def insertAtPosition(self, trid, mode, status, position):
        temp = self.head
        count = 0
        while temp is not None:
            if count == position - 1:
                break
            count += 1
            temp = temp.next
        if position == 1:
            self.insertAtBeginning(trid, mode, status)
        elif temp is None:
            print("There are less than {}-1 elements in the linked list. Cannot insert at {} position.".format(position,
                                                                                                               position))
        elif temp.next is None:
            self.insertAtEnd(trid, mode, status)
        else:
            new_node = Node(trid, mode, status)
            new_node.next = temp.next
            new_node.previous = temp
            temp.next.previous = new_node
            temp.next = new_node

    def printLinkedList(self):
        temp = self.head
        trids = []
        while temp is not None:
            trids.append(temp.trid)
            temp = temp.next
        print(*trids, sep=", ")

    def updateElement(self, old_value, new_value):
        temp = self.head
        isUpdated = False
        while temp is not None:
            if temp.status == old_value:
                temp.status = new_value
                isUpdated = True
            temp = temp.next
        if isUpdated:
            print("Value Updated in the linked list")
        else:
            print("Value not Updated in the linked list")

    def updateAtPosition(self, status, position):
        temp = self.head
        count = 0
        while temp is not None:
            if count == position:
                break
            count += 1
            temp = temp.next
        if temp is None:
            print("Less than {} elements in the linked list. Cannot update.".format(position))
        else:
            temp.status = status
            print("Value updated at position {}".format(position))

    def deleteFromBeginning(self):
        if self.isEmpty():
            print("Linked List is empty. Cannot delete elements.")
        elif self.head.next is None:
            self.head = None
        else:
            self.head = self.head.next
            self.head.previous = None

    def deleteFromLast(self):
        if self.isEmpty():
            print("Linked List is empty. Cannot delete elements.")
        elif self.head.next is None:
            self.head = None
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.previous.next = None
            temp.previous = None

    def delete(self, trid):
        if self.isEmpty():
            print("Linked List is empty. Cannot delete elements.")
        elif self.head.next is None:
            if self.head.trid == trid:
                self.head = None
        else:
            temp = self.head
            while temp is not None:
                if temp.trid == trid:
                    break
                temp = temp.next
            if temp is None:
                print("Element not present in linked list. Cannot delete element.")
            elif temp.next is None:
                self.deleteFromLast()
            else:
                temp.next = temp.previous.next
                temp.next.previous = temp.previous
                temp.next = None
                temp.previous = None

    def deleteFromPosition(self, position):
        if self.isEmpty():
            print("Linked List is empty. Cannot delete elements.")
        elif position == 1:
            self.deleteFromBeginning()
        else:
            temp = self.head
            count = 1
            while temp is not None:
                if count == position:
                    break
                temp = temp.next
            if temp is None:
                print("There are less than {} elements in linked list. Cannot delete element.".format(position))
            elif temp.next is None:
                self.deleteFromLast()
                temp.previous.next = temp.next
                temp.next.previous = temp.previous
                temp.next = None
                temp.previous = None


# x = DoublyLinkedList()
# print(x.isEmpty())
# x.insertAtBeginning(0, "X", "granted")
# print("0--------")
# x.printLinkedList()
# x.insertAtEnd(1, "S", "blocked")
# print("0, 1--------")
# x.printLinkedList()
# x.deleteFromLast()
# print("0--------")
# x.printLinkedList()
# x.insertAtEnd(2, "S", "blocked")
# print("0, 2--------")
# x.printLinkedList()
# x.deleteFromLast()
# x.deleteFromBeginning()
# x.insertAtEnd(3, "X", "granted")
# print("3--------")
# x.printLinkedList()