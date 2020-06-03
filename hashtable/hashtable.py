class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        if capacity > MIN_CAPACITY:
            self.capacity = capacity
            self.data = [None] * self.capacity
        else:
            self.capacity = MIN_CAPACITY
            self.data = [None] * self.capacity
        self.num_items = 0
        self.max_load_factor = 0.7
        self.min_load_factor = 0.2


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.num_items / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        hash = 0xcbf29ce484222325 # decimal: 14695981039346656037
        fnv_64_prime = 0x00000100000001B3 # decimal: 1099511628211
        uint64_max = 2 ** 64
        for x in key:
            hash = hash ^ ord(x)
            hash = (hash * fnv_64_prime) % uint64_max
        return hash


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """

        if self.get_load_factor() > self.max_load_factor:
            self.resize(self.capacity * 2)

        slot = self.hash_index(key)
        node = self.data[slot]

        if node is None:
            self.data[slot] = HashTableEntry(key, value)
        else:
            previous = None

            while node:
                if node.key == key:
                    node.value = value
                    return
                previous = node
                node = node.next

            node = HashTableEntry(key, value)
            previous.next = node
        self.num_items += 1



    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

        if self.get_load_factor() < self.min_load_factor:
            if self.capacity // 2 >= 8:
                self.resize(self.capacity // 2)

        slot = self.hash_index(key)
        node = self.data[slot]

        if node is None:
            print("Key not found")
            return None

        else:
            previous = None
            while node:
                if node.key == key:
                    node.value = None
                    self.num_items -= 1
                    if previous:
                        previous.next = node.next
                        return
                    return
                previous = node
                node = node.next
            print("Key not found")
            return None



    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """

        slot = self.hash_index(key)
        node = self.data[slot]

        if node:
            while node:
                if node.key == key:
                    return node.value
                node = node.next
        return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        self.capacity = new_capacity
        old = self.data
        self.data = [None] * self.capacity

        for item in old:
            while item:
                self.put(item.key, item.value)
                item = item.next



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

    print(ht.djb2("line_1"))
    print(ht.fnv1("line_1"))
    print(ht.hash_index("line_1"))

    print(ht.djb2("line_9"))
    print(ht.fnv1("line_9"))
    print(ht.hash_index("line_9"))

    print(ht.djb2("line_10"))
    print(ht.fnv1("line_10"))
    print(ht.hash_index("line_10"))
