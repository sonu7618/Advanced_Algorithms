import csv
import time
import matplotlib.pyplot as plt

from vrptw import generate_instance, greedy_construct, evaluate_solution
from local_search import local_search
from simulated_annealing import simulated_annealing

SIZES = [25, 50, 100]
CSV_FILE = "benchmark_results.csv"


def time_it(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return end - start, result


def run_benchmark():

    results = []

    for n in SIZES:

        instance = generate_instance(
            n_customers=n,
            vehicle_capacity=100,
            seed=42,
        )

        greedy_time, greedy_routes = time_it(
            greedy_construct,
            instance,
            seed=42,
        )

        _, greedy_distance, greedy_vehicles = evaluate_solution(
            greedy_routes,
            instance,
        )

        ls_time, (ls_routes, scans) = time_it(
            local_search,
            greedy_routes,
            instance,
        )

        _, ls_distance, ls_vehicles = evaluate_solution(
            ls_routes,
            instance,
        )

        iterations = max(1000, n * 100)

        sa_time, (sa_routes, sa_distance, history) = time_it(
            simulated_annealing,
            greedy_routes,
            instance,
            initial_temp=50.0,
            cooling_rate=0.997,
            iterations=iterations,
            seed=42,
        )

        _, _, sa_vehicles = evaluate_solution(
            sa_routes,
            instance,
        )

        results.append({
            "n": n,
            "greedy_dist": greedy_distance,
            "greedy_vehicles": greedy_vehicles,
            "greedy_time": greedy_time,
            "ls_dist": ls_distance,
            "ls_vehicles": ls_vehicles,
            "ls_time": ls_time,
            "ls_scans": scans,
            "sa_dist": sa_distance,
            "sa_vehicles": sa_vehicles,
            "sa_time": sa_time,
            "sa_iterations": iterations,
        })

        print(f"\nCustomers : {n}")
        print(f"Greedy        : {greedy_distance:.2f}   {greedy_time:.4f}s")
        print(f"Local Search  : {ls_distance:.2f}   {ls_time:.4f}s")
        print(f"Annealing     : {sa_distance:.2f}   {sa_time:.4f}s")

    fields = [
        "n",
        "greedy_dist",
        "greedy_vehicles",
        "greedy_time",
        "ls_dist",
        "ls_vehicles",
        "ls_time",
        "ls_scans",
        "sa_dist",
        "sa_vehicles",
        "sa_time",
        "sa_iterations",
    ]

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    return results


def plot_results(results):

    sizes = [r["n"] for r in results]

    plt.figure(figsize=(7, 5))

    plt.plot(
        sizes,
        [r["greedy_dist"] for r in results],
        marker="o",
        label="Greedy",
    )

    plt.plot(
        sizes,
        [r["ls_dist"] for r in results],
        marker="o",
        label="Local Search",
    )

    plt.plot(
        sizes,
        [r["sa_dist"] for r in results],
        marker="o",
        label="Simulated Annealing",
    )

    plt.xlabel("Customers")
    plt.ylabel("Distance")
    plt.title("Solution Quality")
    plt.legend()
    plt.grid(True)

    plt.savefig("task4_quality_comparison.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 5))

    plt.plot(
        sizes,
        [r["greedy_time"] for r in results],
        marker="o",
        label="Greedy",
    )

    plt.plot(
        sizes,
        [r["ls_time"] for r in results],
        marker="o",
        label="Local Search",
    )

    plt.plot(
        sizes,
        [r["sa_time"] for r in results],
        marker="o",
        label="Simulated Annealing",
    )

    plt.xlabel("Customers")
    plt.ylabel("Time (seconds)")
    plt.title("Running Time")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.savefig("task4_runtime_comparison.png", dpi=150)
    plt.close()

    row = results[-1]

    plt.figure(figsize=(6, 5))

    names = ["Greedy", "Local Search", "Simulated Annealing"]
    distances = [
        row["greedy_dist"],
        row["ls_dist"],
        row["sa_dist"],
    ]

    times = [
        row["greedy_time"],
        row["ls_time"],
        row["sa_time"],
    ]

    for name, t, d in zip(names, times, distances):
        plt.scatter(t, d, s=100)
        plt.text(t, d, name)

    plt.xscale("log")
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.title(f"Comparison ({row['n']} customers)")
    plt.grid(True)

    plt.savefig("task4_tradeoff.png", dpi=150)
    plt.close()


if __name__ == "__main__":

    results = run_benchmark()

    plot_results(results)

    print("\nResults saved in", CSV_FILE)