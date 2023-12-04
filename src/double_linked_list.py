class Node:
    def __init__(self, id, **kwargs):
        self.previous = None
        self.next = None
        self.id = id
        self.arguments = kwargs


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

    def search(self, id):
        temp = self.head
        isFound = False
        while temp is not None:
            if temp.id == id:
                isFound = True
                break
            temp = temp.next
        return isFound, temp

    def insertAtBeginning(self, id, **kwargs):
        new_node = Node(id, **kwargs)
        if self.isEmpty():
            self.head = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node

    def insertAtEnd(self, id, **kwargs):
        new_node = Node(id, **kwargs)
        if self.isEmpty():
            self.insertAtBeginning(id, **kwargs)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = new_node
            new_node.previous = temp

    def insertAfterElement(self, id, element, **kwargs):
        temp = self.head
        while temp is not None:
            if temp.id == element:
                break
            temp = temp.next
        if temp is None:
            print("{} is not present in the linked list. {} cannot be inserted into the list.".format(element, value))
        else:
            new_node = Node(id, **kwargs)
            new_node.next = temp.next
            new_node.previous = temp
            temp.next.previous = new_node
            temp.next = new_node

    def insertAtPosition(self, id, position, **kwargs):
        temp = self.head
        count = 0
        while temp is not None:
            if count == position - 1:
                break
            count += 1
            temp = temp.next
        if position == 1:
            self.insertAtBeginning(id, **kwargs)
        elif temp is None:
            print("There are less than {}-1 elements in the linked list. Cannot insert at {} position.".format(position,
                                                                                                               position))
        elif temp.next is None:
            self.insertAtEnd(id, **kwargs)
        else:
            new_node = Node(id, **kwargs)
            new_node.next = temp.next
            new_node.previous = temp
            temp.next.previous = new_node
            temp.next = new_node

    def __str__(self):
        temp = self.head
        ids = []
        while temp is not None:
            temp_str = str(temp.id)
            a = "\n"
            args_str = '\n'.join([f'{arg}:{a}{str(temp.arguments[arg])}' for arg in temp.arguments])
            ids.append(f"{temp_str}, {args_str}")
            temp = temp.next
        return "\n".join(ids) if len(ids) else ""

    def updateElement(self, id, **kwargs):
        temp = self.head
        isUpdated = False
        while temp is not None:
            if temp.id == id:
                temp.arguments = kwargs
                isUpdated = True
            temp = temp.next
        if isUpdated:
            print("Value Updated in the linked list")
        else:
            print("Value not Updated in the linked list")

    def updateAtPosition(self, position, **kwargs):
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
            temp.arguments = kwargs
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

    def delete(self, id):
        if self.isEmpty():
            print("Linked List is empty. Cannot delete elements.")
        elif self.head.next is None:
            if self.head.id == id:
                self.head = None
        else:
            temp = self.head
            while temp is not None:
                if temp.id == id:
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
# x.insertAtBeginning(0, mode="X", status="granted")
# print("0--------")
# print(x)
# x.insertAtEnd(1, mode="S", status="blocked")
# print("0, 1--------")
# print(x)
# x.deleteFromLast()
# print("0--------")
# print(x)
# x.insertAtEnd(2, mode="S", status="blocked")
# print("0, 2--------")
# print(x)
# x.deleteFromLast()
# x.deleteFromBeginning()
# x.insertAtEnd(3, mode="X", status="granted")
# print("3--------")
# print(x)