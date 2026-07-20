from graph_gen import generate_graph, node_work


# Sequential Breadth-First Search
def bfs_sequential(adj, source, work_iterations=2000):
    visited = {source}
    frontier = [source]
    levels = {source: 0}

    node_work(source, work_iterations)

    level = 0

    while frontier:
        next_frontier = []
        level += 1

        for u in frontier:
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    levels[v] = level
                    node_work(v, work_iterations)
                    next_frontier.append(v)

        frontier = next_frontier

    return visited, levels


if __name__ == "__main__":
    import time

    print("=" * 55)
    print("SEQUENTIAL BFS - DEMO")
    print("=" * 55)

    # Generate a sample graph
    adj = generate_graph(n_nodes=2000, avg_degree=6, seed=1)

    print(
        f"\nGraph: {len(adj)} nodes, "
        f"{sum(len(v) for v in adj.values()) // 2} edges"
    )

    start = time.perf_counter()
    visited, levels = bfs_sequential(adj, source=0, work_iterations=2000)
    elapsed = time.perf_counter() - start

    print(f"\nVisited {len(visited)} / {len(adj)} nodes")
    print(f"Max BFS level (hop count) reached: {max(levels.values())}")
    print(f"Time: {elapsed:.4f}s")
    print("=" * 55)