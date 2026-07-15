"""
Min-Heap (array-based binary heap) used as a priority queue.
Keyed on distance -> supports O(1) find-min and O(log n) push/pop.
Used for "next nearest city to visit" style greedy route planning.
"""

from bst import City  # reuse City class


class MinHeap:
    def __init__(self):
        self._heap = []  # list of (distance, city) tuples, min-heap on distance

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    # ---------- Push: O(log n) ----------
    def push(self, distance, city):
        self._heap.append((distance, city))
        self._sift_up(len(self._heap) - 1)

    # ---------- Pop (extract-min): O(log n) ----------
    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty heap")
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top

    # ---------- Peek (find-min): O(1) ----------
    def peek(self):
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i][0] < self._heap[parent][0]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < n and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            i = smallest


if __name__ == "__main__":
    heap = MinHeap()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("MIN-HEAP - DEMO (Priority Queue by Distance)")
    print("=" * 50)

    print("\nPush:")
    for c in cities:
        heap.push(c.distance, c)
        print(f"  Pushed  -> {c.name:<12} dist={c.distance}")

    print(f"\nHeap Size: {len(heap)}")
    nearest_dist, nearest_city = heap.peek()
    print(f"Peek (nearest city): {nearest_city.name}  dist={nearest_dist}")

    print("\nPop order (nearest -> farthest):")
    while not heap.is_empty():
        distance, city = heap.pop()
        print(f"  {city.name:<12} dist={distance}")

    print(f"\nHeap Size: {len(heap)}")
    print("=" * 50)
"""
Min-Heap (array-based binary heap) used as a priority queue.
Keyed on distance -> supports O(1) find-min and O(log n) push/pop.
Used for "next nearest city to visit" style greedy route planning.
"""

from bst import City  # reuse City class


class MinHeap:
    def __init__(self):
        self._heap = []  # list of (distance, city) tuples, min-heap on distance

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    # ---------- Push: O(log n) ----------
    def push(self, distance, city):
        self._heap.append((distance, city))
        self._sift_up(len(self._heap) - 1)

    # ---------- Pop (extract-min): O(log n) ----------
    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty heap")
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return top

    # ---------- Peek (find-min): O(1) ----------
    def peek(self):
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i][0] < self._heap[parent][0]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < n and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            i = smallest


if __name__ == "__main__":
    heap = MinHeap()
    cities = [
        City("Kathmandu", 27.7172, 85.3240, 1_500_000, 0),
        City("Pokhara", 28.2096, 83.9856, 400_000, 200),
        City("Butwal", 27.7000, 83.4486, 150_000, 280),
        City("Biratnagar", 26.4525, 87.2718, 250_000, 400),
        City("Dharan", 26.8065, 87.2846, 150_000, 370),
        City("Nepalgunj", 28.0500, 81.6167, 150_000, 550),
    ]

    print("=" * 50)
    print("MIN-HEAP - DEMO (Priority Queue by Distance)")
    print("=" * 50)

    print("\nPush:")
    for c in cities:
        heap.push(c.distance, c)
        print(f"  Pushed  -> {c.name:<12} dist={c.distance}")

    print(f"\nHeap Size: {len(heap)}")
    nearest_dist, nearest_city = heap.peek()
    print(f"Peek (nearest city): {nearest_city.name}  dist={nearest_dist}")

    print("\nPop order (nearest -> farthest):")
    while not heap.is_empty():
        distance, city = heap.pop()
        print(f"  {city.name:<12} dist={distance}")

    print(f"\nHeap Size: {len(heap)}")
    print("=" * 50)