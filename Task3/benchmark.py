import csv
import random
import sys
import time
import matplotlib.pyplot as plt

from weighted_job_scheduling import schedule_jobs, schedule_jobs_naive
from min_platforms import min_platforms, min_platforms_brute_force
from hamiltonian_path import hamiltonian_path

sys.setrecursionlimit(20000)


#Helper Functions
def timer(func, *args, repeat=5, **kwargs):
    """Return the fastest execution time."""
    best = float("inf")
    result = None

    for _ in range(repeat):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        best = min(best, time.perf_counter() - start)

    return best, result


def save_csv(filename, rows):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# Dynamic Programming 

def generate_jobs(n):
    random.seed(42)
    jobs = []

    for _ in range(n):
        start = random.randint(0, 10000)
        end = start + random.randint(1, 200)
        profit = random.randint(1, 1000)
        jobs.append((start, end, profit))

    return jobs


def benchmark_dp():

    sizes = [100, 500, 1000, 2000, 4000, 8000, 16000]
    rows = []

    for n in sizes:

        jobs = generate_jobs(n)

        opt, _ = timer(schedule_jobs, jobs)
        naive, _ = timer(schedule_jobs_naive, jobs)

        rows.append({
            "n": n,
            "optimised_sec": opt,
            "naive_sec": naive
        })

        print(f"n={n}  Optimised={opt:.6f}s  Naive={naive:.6f}s")

    save_csv("task3_dp_results.csv", rows)

    plt.plot(sizes, [r["optimised_sec"] for r in rows], marker="o", label="Optimised")
    plt.plot(sizes, [r["naive_sec"] for r in rows], marker="o", label="Naive")
    plt.xlabel("Jobs")
    plt.ylabel("Time (s)")
    plt.title("Weighted Job Scheduling")
    plt.legend()
    plt.grid()
    plt.savefig("task3_dp_comparison.png")
    plt.close()


# Greedy 

def generate_schedule(n):

    random.seed(42)

    arrivals = [random.randint(0, 10000) for _ in range(n)]
    departures = [a + random.randint(1, 100) for a in arrivals]

    return arrivals, departures


def benchmark_greedy():

    sizes = [100, 500, 1000, 2000, 4000]
    rows = []

    for n in sizes:

        arr, dep = generate_schedule(n)

        greedy, _ = timer(min_platforms, arr, dep)
        brute, _ = timer(min_platforms_brute_force, arr, dep)

        rows.append({
            "n": n,
            "greedy_sec": greedy,
            "brute_force_sec": brute
        })

        print(f"n={n}  Greedy={greedy:.6f}s  Brute={brute:.6f}s")

    save_csv("task3_greedy_results.csv", rows)

    plt.plot(sizes, [r["greedy_sec"] for r in rows], marker="o", label="Greedy")
    plt.plot(sizes, [r["brute_force_sec"] for r in rows], marker="o", label="Brute Force")
    plt.xlabel("Trains")
    plt.ylabel("Time (s)")
    plt.title("Minimum Platforms")
    plt.legend()
    plt.grid()
    plt.savefig("task3_greedy_comparison.png")
    plt.close()


# Backtracking 

def random_graph(n, p):

    random.seed(42)

    graph = {i: [] for i in range(n)}

    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                graph[u].append(v)

    return graph


def no_path_graph(n):

    graph = {}

    for i in range(n - 1):
        graph[i] = [j for j in range(n - 1) if j != i]

    graph[n - 1] = []

    return graph


def benchmark_backtracking():

    rows = []

    for n in [8, 10, 12, 14, 16, 18]:

        graph = random_graph(n, 0.4)

        t1, (_, nodes1) = timer(hamiltonian_path, graph, 0, use_heuristic=False)
        t2, (_, nodes2) = timer(hamiltonian_path, graph, 0, use_heuristic=True)

        rows.append({
            "graph": "random",
            "n": n,
            "plain_time": t1,
            "plain_nodes": nodes1,
            "heuristic_time": t2,
            "heuristic_nodes": nodes2
        })

        print(f"Random Graph {n}: {t1:.5f}s vs {t2:.5f}s")

    for n in [6, 7, 8, 9, 10, 11]:

        graph = no_path_graph(n)

        t1, (_, nodes1) = timer(hamiltonian_path, graph, 0, repeat=3, use_heuristic=False)
        t2, (_, nodes2) = timer(hamiltonian_path, graph, 0, repeat=3, use_heuristic=True)

        rows.append({
            "graph": "worst_case",
            "n": n,
            "plain_time": t1,
            "plain_nodes": nodes1,
            "heuristic_time": t2,
            "heuristic_nodes": nodes2
        })

        print(f"Worst Case {n}: {nodes1} vs {nodes2}")

    save_csv("task3_backtracking_results.csv", rows)

    random_rows = [r for r in rows if r["graph"] == "random"]

    plt.plot(
        [r["n"] for r in random_rows],
        [r["plain_time"] for r in random_rows],
        marker="o",
        label="Plain"
    )

    plt.plot(
        [r["n"] for r in random_rows],
        [r["heuristic_time"] for r in random_rows],
        marker="o",
        label="Heuristic"
    )

    plt.xlabel("Vertices")
    plt.ylabel("Time (s)")
    plt.yscale("log")
    plt.legend()
    plt.grid()
    plt.savefig("task3_backtracking_runtime.png")
    plt.close()



if __name__ == "__main__":

    print("Task 3 Benchmark")

    print("\nDynamic Programming")
    benchmark_dp()

    print("\nGreedy")
    benchmark_greedy()

    print("\nBacktracking")
    benchmark_backtracking()

    print("\nDone!")