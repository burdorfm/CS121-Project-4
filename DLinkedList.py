class DLLNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DLinkedList:
    def __init__(self):
        self.first = None
        self.last = None

    def prepend(self, value):
        node = DLLNode(value)
        self.first, node.next = node, self.first
        node.prev = None
        if node.next == None:
            self.last = node
        else:
            node.next.prev = node

    def append(self, value):
        node = DLLNode(value)
        self.last, node.prev = node, self.last
        self.next = None
        if node.prev == None:
            self.first = node
        else:
            node.prev.next = node

    def remove(self, rval):
        current = self.first
        while current != None and current.value != rval:
            current = current.next
        if current != None:
            if current.prev == None:
                if current.next == None:
                    self.first = None
                    self.last = None 
                else:
                    self.first = current.next
                    current.next.prev = None
            else:
                if current.next == None:
                    current.prev.next = None
                    self.last = current.prev
                else:
                    current.prev.next, current.next.prev = current.next, current.prev

    def insert_at(self, index, value):
        l = self.length()
        node = DLLNode(value)
        if index >= 0 and index <= l:
            if l == 0 and index == 0:
                self.first = node
                self.last = node
            elif index == 0:
                current = self.first
                current.prev = node
                node.next = current
                node.prev = None
                self.first = node
            else:
                if index == l:
                    pos = 1
                    current = self.first
                    while pos < l:
                        current = current.next
                        pos += 1
                    current.next = node
                    node.prev = current
                    node.next = None
                    self.last = node
                else: # if not inserting in firs or last spot
                    pos = 0 
                    current = self.first
                    while pos < index:
                        current = current.next
                        pos += 1
                    node.prev = current.prev
                    node.next = current
                    current.prev.next = node
                    current.prev = node


        '''if index >= 0 and index <= l:
            pos = 0
            current = self.first
            while pos <= index:
                current = current.next
                pos = pos + 1
            node = DLLNode(value)
            if index == l:
                node.next = None
                node.prev = current
                current.next = node
                self.last = node
            else:
                if current.prev == None:
                    node.next = current
                    node.prev = None
                    current.prev = node
                    self.first = node
                else:
                    node.next = current
                    node.prev = current.prev
                    current.prev = node
                    node.prev.next = node'''

    def contains(self, value):
        current = self.first
        while current != None:
            if current.value == value:
                return True
            current = current.next
        return False

    def as_string(self):
        if self.first == None:
            return "<>"
        else:
            s = "<" + str(self.first.value)
            current = self.first.next
            while current != None:
                s = s + ", " + str(current.value)
                current = current.next
            s = s + ">"
            return s

    def length(self):
        count = 0
        current = self.first
        while current != None:
            count = count + 1
            current = current.next
        return count

    def is_empty(self):
        return (self.first == None)

    def display(self):
        print(self.as_string())

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string()

    def __bool__(self):
        return not self.is_empty() 