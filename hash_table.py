
class HashTable:
    """
    Class HashTable -- supports indexing songs into a Hash Table and supports finding them by using words as keys
    to finding songs in the hash_table
    """

    def __init__(self):
        """
        Initializer (Constructor) for the HashTable -- supports creating an empty Hash Table that will be used to
        index songs and will be used to find the songs later
        Parameters:
            size: represents the size of the hash table
            data: holds the songs and their key
            slots: holds just the keys
            occupied: represents the number of slots occupied by data
            load_factor: represents how much of the hash table is taken up
            conflicts: represents the amount of hashing conflicts
        """
        f = open('logfile.txt', 'a')
        f.write('Program Start')
        self.size = 31
        self.data = [None] * self.size
        self.slots = [None] * self.size
        self.occupied = 0
        self.load_factor = 0
        self.conflicts = 0
        f.write('\nHashTable Details: ' + str(self.size) + ' Slots, ' + str(self.occupied) + ' Occupied, '
                + ' Load Factor = ' + str(self.load_factor))

    def __str__(self):
        """
        __str__ method for HashTable -- supports returning a string representation of how many slots there are, how
        many of those slots are occupied, and the current load factor
        Returns:
            a string representation of how many slots there are, how many of those slots are occupied, and the
            current load factor
        """
        length = len(self.data)
        return str(length) + ' Slots, ' + str(self.occupied) + ' Occupied, Load Factor =' \
            + str(self.occupied / self.size)

    def store(self, word, tup):
        """
        store method for HashTable -- supports storing a word and tuple containing the song name, id, and creator.
        Uses the hash_function to find a slot for the key (word) and makes a list of the key and tuples associated
        with the key
        Parameters:
            word: represents the key that will be used to find songs later
            tup: represents the tuple that contains the song name, creator, and id
        Returns:
            Nothing
        """
        word = word.lower()
        slot = self.hash_function(word, len(self.slots))
        if self.slots[slot] is None:
            list_data = []
            self.slots[slot] = word
            list_data.append(word)
            list_data.append(tup)
            self.data[slot] = list_data
            self.occupied += 1
        else:
            if self.slots[slot] == word:
                list_data = self.data[slot]
                list_data.append(tup)
            else:
                new_slot = self.rehash(slot, len(self.slots))
                while self.slots[new_slot] is not None and self.slots[new_slot] != word:
                    new_slot = self.rehash(new_slot, len(self.slots))
                if self.slots[new_slot] is None:
                    list_data = []
                    self.slots[new_slot] = word
                    list_data.append(word)
                    list_data.append(tup)
                    self.data[new_slot] = list_data
                    self.occupied += 1
                else:
                    list_data = self.data[new_slot]
                    list_data.append(tup)
        self.load_factor = self.occupied / self.size
        if self.load_factor > 0.7:
            f = open('logfile.txt', 'a')
            f.write('\n    ' + str(self.occupied) + ' keys read, HashTable Expansion Needed')
            f.write('\n        Before Expansion: ' + str(self.size) + ' slots, ' + str(self.occupied) + ' occupied, '
                    + 'load factor = ' + str(self.load_factor))
            self.remap()
            f.write('\n        After Expansion: ' + str(self.size) + ' slots, ' + str(self.occupied) + ' occupied, '
                    + ' load factor = ' + str(self.load_factor))
            f.close()

    def get(self, item):
        """
        get method for HashTable -- supports getting returning the list connected with the key
        Parameters:
            item: represents the key that we will be looking for
        Returns:
            a list of songs associated with the key entered
        """
        start_slot = self.hash_function(item, len(self.slots))
        data = None
        stop = False
        found = False
        position = start_slot
        while self.slots[position] is not None and not found and not stop:
            if self.slots[position] == item:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position, len(self.slots))
                if position == start_slot:
                    stop = True
        return data

    def hash_function(self, item, size):
        """
        hash_function method for the HashTable class -- hashes words by taking the ASCII code of each letter and
        multiplying it by its position in the word
        Parameters:
            item: represents the word that we will be hashing
            size: represents the length of the hash_table
        Returns:
            the number of the slot to use
        Rationale:
            I thought that using the ASCII code for the letter would be best because we do need some type of number
            to be able to hash anything. I multiplied each letter by its position to avoid conflict with words that
            have the same exact letters. For example "this" and "hits" will not be in the same position.
        """
        total = 0
        position = 1
        for letter in item:
            total += ord(letter) * position
            position += 1
        slot_number = total % size
        return slot_number

    def rehash(self, previous_slot, size):
        """
        rehash method for HashTable class -- supports solving having conflicts by adding 1 to slot number and modding
        the result by the number of slots in the hash table
        Parameters:
            previous_slot: represents the slot number that we will be adding 1 to
            size: represents the number of slots in the hash table
        Returns:
            the new slot number
        Rationale:
            I chose this method because it seemed like it would be the simplest way to solve the hashing conflict,
            just by adding 1 to the previous slot number and modding by the size making a new slot number.
        """
        self.conflicts += 1
        return (previous_slot + 1) % size

    def remap(self):
        """
        remap method for HashTable -- supports adding slots to the hash table when the load factor has been
        passed
        Parameters:

        Returns:
            Nothing
        """
        old_slots = self.slots
        old_data = self.data
        self.size = self.prime(self.size * 2)
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.occupied = 0
        for i in range(len(old_slots)):
            if old_slots[i] is not None:
                x = old_data[i]
                x = x[1:]
                for items in x:
                    self.store(old_slots[i], items)

    def prime(self, num):
        """
        prime method for HashTable class -- finds the next prime number after a certain number
        Parameters:
            num: represents the number we will be starting at
        Returns:
            the next prime number
        """
        while not self.is_prime(num):
            num += 1
        return num

    def is_prime(self, num):
        """
        is_prime method for HashTable class -- supports returning True if a number is a prime number, False otherwise
        Parameters:
            num: represents the number we are looking at
        Returns:
            True if the number is prime, False otherwise
        """
        for i in range(2, num):
            if num % i == 0:
                return False
        return True
