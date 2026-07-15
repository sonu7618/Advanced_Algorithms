"""
Empirical benchmark: BST vs AVL vs Hash Table vs Min-Heap.
Measures wall-clock time for insert / search / delete at n = 100, 1000, 10000.
Outputs a results table (CSV) and comparison graphs (PNG).
"""

import time
import random
import csv
import matplotlib.pyplot as plt

from bst import BST, City
from avl import AVLTree
from hash_table import HashTable
from min_heap import MinHeap

SIZES = [100, 1_000, 10_000]
RESULTS_CSV = "benchmark_results.csv"


def generate_cities(n, seed=42):
    random.seed(seed)
    cities = []
    for i in range(n):
        name = f"city_{i}_{random.randint(0, 10**9)}"  # unique keys
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        population = random.randint(1_000, 2_000_000)
        distance = random.uniform(0, 1000)
        cities.append(City(name, lat, lon, population, distance))
    return cities


def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    fn(*args, **kwargs)
    return time.perf_counter() - start


def benchmark_bst(cities):
    tree = BST()
    insert_t = time_it(lambda: [tree.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [tree.search(c.name) for c in cities])
    delete_t = time_it(lambda: [tree.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_avl(cities):
    tree = AVLTree()
    insert_t = time_it(lambda: [tree.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [tree.search(c.name) for c in cities])
    delete_t = time_it(lambda: [tree.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_hash_table(cities):
    ht = HashTable()
    insert_t = time_it(lambda: [ht.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [ht.search(c.name) for c in cities])
    delete_t = time_it(lambda: [ht.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_min_heap(cities):
    heap = MinHeap()
    insert_t = time_it(lambda: [heap.push(c.distance, c) for c in cities])
    # Min-heap doesn't support arbitrary search; peek is O(1), so we time repeated pops instead
    pop_t = time_it(lambda: [heap.pop() for _ in range(len(cities))])
    return insert_t, pop_t, None  # no delete-by-key benchmark for heap


def run_benchmarks():
    rows = []
    for n in SIZES:
        cities = generate_cities(n)

        bst_i, bst_s, bst_d = benchmark_bst(cities)
        avl_i, avl_s, avl_d = benchmark_avl(cities)
        ht_i, ht_s, ht_d = benchmark_hash_table(cities)
        heap_i, heap_pop, _ = benchmark_min_heap(cities)

        rows.append(["BST", n, bst_i, bst_s, bst_d])
        rows.append(["AVL", n, avl_i, avl_s, avl_d])
        rows.append(["HashTable", n, ht_i, ht_s, ht_d])
        rows.append(["MinHeap", n, heap_i, heap_pop, None])  # pop-all instead of delete

        print(f"n={n} done")

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["structure", "n", "insert_sec", "search_sec", "delete_sec"])
        writer.writerows(rows)

    return rows


def plot_results(rows):
    structures = ["BST", "AVL", "HashTable", "MinHeap"]
    operations = [("insert_sec", 2), ("search_sec", 3), ("delete_sec", 4)]

    for op_name, col_idx in operations:
        plt.figure(figsize=(7, 5))
        for structure in structures:
            xs, ys = [], []
            for row in rows:
                if row[0] == structure and row[col_idx] is not None:
                    xs.append(row[1])
                    ys.append(row[col_idx])
            if xs:
                plt.plot(xs, ys, marker="o", label=structure)
        plt.xlabel("Number of cities (n)")
        plt.ylabel("Time (seconds)")
        plt.title(f"{op_name.replace('_sec', '').capitalize()} time vs n")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(f"task1_{op_name}_comparison.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved task1_{op_name}_comparison.png")


if __name__ == "__main__":
    results = run_benchmarks()
    plot_results(results)
    print(f"\nResults written to {RESULTS_CSV}")
"""
Empirical benchmark: BST vs AVL vs Hash Table vs Min-Heap.
Measures wall-clock time for insert / search / delete at n = 100, 1000, 10000.
Outputs a results table (CSV) and comparison graphs (PNG).
"""

import time
import random
import csv
import matplotlib.pyplot as plt

from bst import BST, City
from avl import AVLTree
from hash_table import HashTable
from min_heap import MinHeap

SIZES = [100, 1_000, 10_000]
RESULTS_CSV = "benchmark_results.csv"


def generate_cities(n, seed=42):
    random.seed(seed)
    cities = []
    for i in range(n):
        name = f"city_{i}_{random.randint(0, 10**9)}"  # unique keys
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        population = random.randint(1_000, 2_000_000)
        distance = random.uniform(0, 1000)
        cities.append(City(name, lat, lon, population, distance))
    return cities


def time_it(fn, *args, **kwargs):
    start = time.perf_counter()
    fn(*args, **kwargs)
    return time.perf_counter() - start


def benchmark_bst(cities):
    tree = BST()
    insert_t = time_it(lambda: [tree.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [tree.search(c.name) for c in cities])
    delete_t = time_it(lambda: [tree.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_avl(cities):
    tree = AVLTree()
    insert_t = time_it(lambda: [tree.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [tree.search(c.name) for c in cities])
    delete_t = time_it(lambda: [tree.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_hash_table(cities):
    ht = HashTable()
    insert_t = time_it(lambda: [ht.insert(c.name, c) for c in cities])
    search_t = time_it(lambda: [ht.search(c.name) for c in cities])
    delete_t = time_it(lambda: [ht.delete(c.name) for c in cities])
    return insert_t, search_t, delete_t


def benchmark_min_heap(cities):
    heap = MinHeap()
    insert_t = time_it(lambda: [heap.push(c.distance, c) for c in cities])
    # Min-heap doesn't support arbitrary search; peek is O(1), so we time repeated pops instead
    pop_t = time_it(lambda: [heap.pop() for _ in range(len(cities))])
    return insert_t, pop_t, None  # no delete-by-key benchmark for heap


def run_benchmarks():
    rows = []
    for n in SIZES:
        cities = generate_cities(n)

        bst_i, bst_s, bst_d = benchmark_bst(cities)
        avl_i, avl_s, avl_d = benchmark_avl(cities)
        ht_i, ht_s, ht_d = benchmark_hash_table(cities)
        heap_i, heap_pop, _ = benchmark_min_heap(cities)

        rows.append(["BST", n, bst_i, bst_s, bst_d])
        rows.append(["AVL", n, avl_i, avl_s, avl_d])
        rows.append(["HashTable", n, ht_i, ht_s, ht_d])
        rows.append(["MinHeap", n, heap_i, heap_pop, None])  # pop-all instead of delete

        print(f"n={n} done")

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["structure", "n", "insert_sec", "search_sec", "delete_sec"])
        writer.writerows(rows)

    return rows


def plot_results(rows):
    structures = ["BST", "AVL", "HashTable", "MinHeap"]
    operations = [("insert_sec", 2), ("search_sec", 3), ("delete_sec", 4)]

    for op_name, col_idx in operations:
        plt.figure(figsize=(7, 5))
        for structure in structures:
            xs, ys = [], []
            for row in rows:
                if row[0] == structure and row[col_idx] is not None:
                    xs.append(row[1])
                    ys.append(row[col_idx])
            if xs:
                plt.plot(xs, ys, marker="o", label=structure)
        plt.xlabel("Number of cities (n)")
        plt.ylabel("Time (seconds)")
        plt.title(f"{op_name.replace('_sec', '').capitalize()} time vs n")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(f"task1_{op_name}_comparison.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved task1_{op_name}_comparison.png")


if __name__ == "__main__":
    results = run_benchmarks()
    plot_results(results)
    print(f"\nResults written to {RESULTS_CSV}")