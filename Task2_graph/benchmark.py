import time
import random
import csv
import matplotlib.pyplot as plt

from graph import Graph
from dijkstra import dijkstra
from prim import prim_mst
from bellmanford import bellman_ford


SIZES = [50, 100, 200, 400, 800]
RESULTS_CSV = "benchmark_results.csv"


# Generate Random Graph

def generate_random_graph(v_count, edge_count, seed=42, directed=True):

    random.seed(seed)

    graph = Graph(directed=directed)

    vertices = [f"v{i}" for i in range(v_count)]

    for v in vertices:
        graph.add_vertex(v)

    random.shuffle(vertices)

    for i in range(len(vertices) - 1):

        graph.add_edge(vertices[i], vertices[i + 1], random.randint(1, 100))

        if directed:
            graph.add_edge(vertices[i + 1], vertices[i], random.randint(1, 100))

    extra_edges = edge_count - graph.num_edges()
    attempts = 0

    while extra_edges > 0 and attempts < edge_count * 5:

        u = random.choice(vertices)
        v = random.choice(vertices)

        attempts += 1

        if u == v:
            continue

        graph.add_edge(u, v, random.randint(1, 100))
        extra_edges -= 1

    return graph


# Timer

def timer(function):

    start = time.perf_counter()
    result = function()
    end = time.perf_counter()

    return end - start, result


# Run Benchmark

def run_benchmarks():

    rows = []

    for v in SIZES:

        sparse = 2 * v
        dense = (v * (v - 1)) // 4

        for graph_type, edges in [("sparse", sparse), ("dense", dense)]:

            graph = generate_random_graph(v, edges)

            source = "v0"

            dijkstra_time, _ = timer(lambda: dijkstra(graph, source))
            bellman_time, _ = timer(lambda: bellman_ford(graph, source))

            graph2 = graph.to_undirected()
            prim_time, _ = timer(lambda: prim_mst(graph2, source))

            rows.append({
                "V": graph.num_vertices(),
                "E": graph.num_edges(),
                "density": graph_type,
                "dijkstra_sec": dijkstra_time,
                "prim_sec": prim_time,
                "bellman_ford_sec": bellman_time
            })

            print(
                f"V={graph.num_vertices():<5} "
                f"E={graph.num_edges():<7} "
                f"{graph_type:<6} "
                f"Dijkstra={dijkstra_time:.5f}s "
                f"Prim={prim_time:.5f}s "
                f"Bellman-Ford={bellman_time:.5f}s"
            )

    with open(RESULTS_CSV, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "V",
                "E",
                "density",
                "dijkstra_sec",
                "prim_sec",
                "bellman_ford_sec"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    return rows


# Plot Results

def plot_results(rows):

    for graph_type in ["sparse", "dense"]:

        plt.figure(figsize=(7, 5))

        data = [r for r in rows if r["density"] == graph_type]

        vertices = [r["V"] for r in data]

        plt.plot(vertices,
                 [r["dijkstra_sec"] for r in data],
                 marker="o",
                 label="Dijkstra")

        plt.plot(vertices,
                 [r["prim_sec"] for r in data],
                 marker="o",
                 label="Prim")

        plt.plot(vertices,
                 [r["bellman_ford_sec"] for r in data],
                 marker="o",
                 label="Bellman-Ford")

        plt.xlabel("Vertices")
        plt.ylabel("Time (seconds)")
        plt.title(f"{graph_type.capitalize()} Graph")
        plt.legend()
        plt.grid(True)

        plt.savefig(f"task2_runtime_{graph_type}.png", dpi=150)
        plt.close()

        print(f"Saved task2_runtime_{graph_type}.png")

    plt.figure(figsize=(7, 5))

    for graph_type in ["sparse", "dense"]:

        data = [r for r in rows if r["density"] == graph_type]

        plt.plot(
            [r["V"] for r in data],
            [r["bellman_ford_sec"] for r in data],
            marker="o",
            label=graph_type.capitalize()
        )

    plt.xlabel("Vertices")
    plt.ylabel("Time (seconds)")
    plt.title("Bellman-Ford Comparison")
    plt.legend()
    plt.grid(True)

    plt.savefig("task2_bellman_ford_density_comparison.png", dpi=150)
    plt.close()

    print("Saved task2_bellman_ford_density_comparison.png")


# Main Program

if __name__ == "__main__":

    results = run_benchmarks()

    plot_results(results)

    print(f"\nResults saved in {RESULTS_CSV}")