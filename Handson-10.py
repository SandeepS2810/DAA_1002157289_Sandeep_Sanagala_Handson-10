import ctypes

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert(self, key, value):
        new_node = Node(key, value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    
    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return -1
    
    def remove(self, key):
        current = self.head
        while current:
            if current.key == key:
                if current == self.head and current == self.tail:
                    self.head = self.tail = None
                elif current == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                elif current == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return
            current = current.next

class HashTable:
    def __init__(self):
        self.default_capacity = 10
        self.load_factor = 0.75
        self.shrink_factor = 0.25
        self.capacity = self.default_capacity
        self.size = 0
        self.table = self._create_array(self.capacity)
    
    def _create_array(self, capacity):
        return [DoublyLinkedList() for _ in range(capacity)]
    
    def hash_function(self, key):
        A = 0.6180339887  # (sqrt(5) - 1) / 2
        return int(self.capacity * ((key * A) % 1))
    
    def rehash(self, new_capacity):
        new_table = self._create_array(new_capacity)
        for i in range(self.capacity):
            current = self.table[i].head if self.table[i] else None
            while current:
                new_index = self.hash_function(current.key)
                if not new_table[new_index]:
                    new_table[new_index] = DoublyLinkedList()
                new_table[new_index].insert(current.key, current.value)
                current = current.next
        self.table = new_table
        self.capacity = new_capacity
    
    def insert(self, key, value):
        index = self.hash_function(key)
        if not self.table[index]:
            self.table[index] = DoublyLinkedList()
        self.table[index].insert(key, value)
        self.size += 1
        
        if self.size / self.capacity >= self.load_factor:
            new_capacity = self.capacity * 2
            self.rehash(new_capacity)
    
    def get(self, key):
        index = self.hash_function(key)
        if not self.table[index]:
            return -1
        return self.table[index].find(key)
    
    def remove(self, key):
        index = self.hash_function(key)
        if self.table[index]:
            self.table[index].remove(key)
            self.size -= 1
            if self.size / self.capacity <= self.shrink_factor and self.capacity > self.default_capacity:
                new_capacity = self.capacity // 2
                self.rehash(new_capacity)

# Example usage
hash_table = HashTable()
hash_table.insert(1, 10)
hash_table.insert(2, 20)
hash_table.insert(3, 30)
hash_table.insert(11, 110)
hash_table.insert(12, 120)
hash_table.insert(13, 130)

print("Value for key 1:", hash_table.get(1))
print("Value for key 11:", hash_table.get(11))

hash_table.remove(2)
print("Value for key 2 after removal:", hash_table.get(2))
