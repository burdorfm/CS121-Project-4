
class LLNode:
    def __init__(self,value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def prepend(self, value):
        
        self.length+=1
        node = LLNode(value)
        node.next = self.first
        self.first = node

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

    def append(self, value):
        self.length += 1
        if self.first == None:
            node = LLNode(value)
            self.first = node
            self.last = node

        else:
            node = LLNode(value)
            self.last = node
            current = self.first
            while current.next != None:
                current = current.next
            current.next = node

    def removeFirst(self):
        if self.length == 0:
            print("you are already dead")

        self.length -= 1

        self.first = self.first.next

    def addFirst(self, value):



    def removeLast(self):
        if self.length == 0:
            print("you are already dead")
            return
        if self.length == 1:
            self.first = None
            self.last = None
            self.length = 0
            return

        self.length -= 1

        current = self.first

        temp1 = None
        while current.next != None:
            print("made it")
            temp1 = current
            print(temp1.value)
            current = current.next

        self.last = temp1

        if self.last != None:
            self.last.next = None
        
    
    def remove(self, value):
        previous = None
        current  = self.first
        while current != None and current.value != value:
            previous = current
            current = current.next
        if current != None:
            if previous != None:
                previous.next = current.next
            else:
                self.first = current.next

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string()

    def __bool__(self):
        return not self.is_empty() 


