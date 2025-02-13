class Node:
    def __init__(self, key, value):
        self.key_value = key  
        self.payload = value  
        self.next_node = None  


class LinkedList:
    def __init__(self):
        self.head_node = None  

    def insert(self, key, value):
        
        cursor = self.head_node
        while cursor:
            if cursor.key_value == key:  
                return False
            cursor = cursor.next_node
        new_entry = Node(key, value)  
        new_entry.next_node = self.head_node  
        self.head_node = new_entry
        return True

    def search(self, key):
        cursor = self.head_node  
        while cursor:
            if cursor.key_value == key:  
                return cursor.payload
            cursor = cursor.next_node  
        return None  

    def remove(self, key):
        cursor = self.head_node  
        previous_entry = None  
        while cursor:
            if cursor.key_value == key:  
                if previous_entry:
                    previous_entry.next_node = cursor.next_node  
                else:
                    self.head_node = cursor.next_node  
                return True
            previous_entry = cursor  
            cursor = cursor.next_node
        return False  

    def __iter__(self):
        cursor = self.head_node
        while cursor:
            yield (cursor.key_value, cursor.payload)  
            cursor = cursor.next_node


class HashTable:
    def __init__(self, capacity=32):
        self._capacity = capacity  
        self.item_count = 0  
        self.hash_table = [None] * self._capacity  

    def _hash(self, key):
        return hash(key) % self._capacity  

    def _resize(self):
        old_table = self.hash_table  
        self._capacity *= 2  
        self.hash_table = [None] * self._capacity  
        self.item_count = 0  
        for chain in old_table:
            if chain:
                for key, value in chain:
                    self.insert(key, value)

    def insert(self, key, value):
        index = self._hash(key)  
        if self.hash_table[index] is None:
            self.hash_table[index] = LinkedList()  
        if not self.hash_table[index].insert(key, value): 
            return False 
        self.item_count += 1  
        if self.item_count / self._capacity > 0.7:
            self._resize()
        return True

    def modify(self, key, value):
        index = self._hash(key)  
        if self.hash_table[index] is None:
            return False  
        cursor = self.hash_table[index].head_node  
        while cursor:
            if cursor.key_value == key:  
                cursor.payload = value
                return True
            cursor = cursor.next_node  
        return False 

    def remove(self, key):
        index = self._hash(key)  
        if self.hash_table[index] is None:
            return False  
        if self.hash_table[index].remove(key):  
            self.item_count -= 1  
            return True
        return False  

    def search(self, key):
        index = self._hash(key)  
        if self.hash_table[index] is None:
            return None  
        return self.hash_table[index].search(key)  

    def capacity(self):  
        return self._capacity  

    def __len__(self):
        return self.item_count  
