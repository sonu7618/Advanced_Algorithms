import random

# Generate a random connected undirected graph
def generate_graph(n_nodes, avg_degree=6, seed=42):
    rng = random.Random(seed)
    adj = {i: [] for i in range(n_nodes)}

    # Create a spanning path to ensure connectivity
    order = list(range(n_nodes))
    rng.shuffle(order)

    for a, b in zip(order, order[1:]):
        adj[a].append(b)
        adj[b].append(a)

    # Add extra random edges
    target_edges = (n_nodes * avg_degree) // 2
    existing_edges = n_nodes - 1
    attempts = 0

    while existing_edges < target_edges and attempts < target_edges * 5:
        u = rng.randrange(n_nodes)
        v = rng.randrange(n_nodes)
        attempts += 1

        if u == v or v in adj[u]:
            continue

        adj[u].append(v)
        adj[v].append(u)
        existing_edges += 1

    return adj


# Simulate CPU-intensive processing for each node
def node_work(node_id, iterations=2000):
    x = node_id

    for i in range(iterations):
        x = (x * 1103515245 + i + 12345) % 2147483647

    return x