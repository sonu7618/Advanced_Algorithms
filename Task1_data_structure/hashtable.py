"""
Hash Table (separate chaining) for fast city lookup by name.
Provides O(1) average-case insert / search / delete.
Automatically resizes once the load factor crosses 0.75 to keep
chains short and performance close to constant time.
"""

from bst import City  # reuse City class


class HashTable:
    def __init__(self, capacity=8):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self._max_load_factor = 0.75

    def __len__(self):
        return self._size

    def _hash(self, key):
        return hash(key) % self._capacity

    # ---------- Insert: O(1) average, O(n) worst (all-collision case) ----------
    def insert(self, key, city):
        if (self._size + 1) / self._capacity > self._max_load_factor:
            self._resize(self._capacity * 2)

        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, city)  # update existing
                return
        bucket.append((key, city))
        self._size += 1

    # ---------- Search: O(1) average, O(n) worst ----------
    def search(self, key):
        idx = self._hash(key)
        for k, city in self._buckets[idx]:
            if k == key:
                return city
        return None

    # ---------- Delete: O(1) average, O(n) worst ----------
    def delete(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, city in bucket:
                self.insert(key, city)

    def load_factor(self):
        return self._size / self._capacity

    def max_chain_length(self):
        return max((len(b) for b in self._buckets), default=0)


if __name__ == "__main__":
    ht = HashTable()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("HASH TABLE - DEMO")
    print("=" * 50)

    print("\nInsertion:")
    for c in cities:
        ht.insert(c.name, c)
        print(f"  Inserted -> {c.name:<12} (load_factor={ht.load_factor():.2f})")

    print(f"\nTotal Entries: {len(ht)}")
    print(f"Max Chain Length: {ht.max_chain_length()}")

    print("\nSearch:")
    for name in ["Pokhara", "Itahari"]:
        result = ht.search(name)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nDeletion:")
    for name in ["Pokhara", "Itahari"]:
        deleted = ht.delete(name)
        status = "DELETED" if deleted else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nFinal Search Check:")
    for key, city in [(c.name, c) for c in cities]:
        result = ht.search(key)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {key:<12} -> {status}")

    print(f"\nTotal Entries: {len(ht)}")
    print("=" * 50)
"""
Hash Table (separate chaining) for fast city lookup by name.
Provides O(1) average-case insert / search / delete.
Automatically resizes once the load factor crosses 0.75 to keep
chains short and performance close to constant time.
"""

from bst import City  # reuse City class


class HashTable:
    def __init__(self, capacity=8):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self._max_load_factor = 0.75

    def __len__(self):
        return self._size

    def _hash(self, key):
        return hash(key) % self._capacity

    # ---------- Insert: O(1) average, O(n) worst (all-collision case) ----------
    def insert(self, key, city):
        if (self._size + 1) / self._capacity > self._max_load_factor:
            self._resize(self._capacity * 2)

        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, city)  # update existing
                return
        bucket.append((key, city))
        self._size += 1

    # ---------- Search: O(1) average, O(n) worst ----------
    def search(self, key):
        idx = self._hash(key)
        for k, city in self._buckets[idx]:
            if k == key:
                return city
        return None

    # ---------- Delete: O(1) average, O(n) worst ----------
    def delete(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, city in bucket:
                self.insert(key, city)

    def load_factor(self):
        return self._size / self._capacity

    def max_chain_length(self):
        return max((len(b) for b in self._buckets), default=0)


if __name__ == "__main__":
    ht = HashTable()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("HASH TABLE - DEMO")
    print("=" * 50)

    print("\nInsertion:")
    for c in cities:
        ht.insert(c.name, c)
        print(f"  Inserted -> {c.name:<12} (load_factor={ht.load_factor():.2f})")

    print(f"\nTotal Entries: {len(ht)}")
    print(f"Max Chain Length: {ht.max_chain_length()}")

    print("\nSearch:")
    for name in ["Pokhara", "Itahari"]:
        result = ht.search(name)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nDeletion:")
    for name in ["Pokhara", "Itahari"]:
        deleted = ht.delete(name)
        status = "DELETED" if deleted else "NOT FOUND"
        print(f"  {name:<12} -> {status}")

    print("\nFinal Search Check:")
    for key, city in [(c.name, c) for c in cities]:
        result = ht.search(key)
        status = "FOUND" if result else "NOT FOUND"
        print(f"  {key:<12} -> {status}")

    print(f"\nTotal Entries: {len(ht)}")
    print("=" * 50)