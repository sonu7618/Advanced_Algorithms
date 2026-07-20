import threading

from graph_gen import generate_graph, node_work
from sync_primitives import Barrier


# Threaded Breadth-First Search
def bfs_threaded(adj, source, n_threads=4, work_iterations=2000,
                 max_concurrent_work=None):

    if max_concurrent_work is None:
        max_concurrent_work = n_threads

    visited = {source}
    levels = {source: 0}
    node_work(source, work_iterations)

    # Synchronization primitives
    visited_lock = threading.Lock()
    work_semaphore = threading.Semaphore(max_concurrent_work)
    barrier = Barrier(n_threads)

    frontier = [source]
    next_frontier = []
    level_holder = [0]
    done_holder = [False]

    # Worker thread
    def worker(thread_id):
        while True:
            # Divide the frontier among threads
            my_chunk = frontier[thread_id::n_threads]

            for u in my_chunk:
                for v in adj[u]:
                    # Update visited nodes safely
                    with visited_lock:
                        if v in visited:
                            continue
                        visited.add(v)
                        levels[v] = level_holder[0] + 1

                    # Perform node processing
                    with work_semaphore:
                        node_work(v, work_iterations)

                    # Add node to next frontier
                    with visited_lock:
                        next_frontier.append(v)

            # Wait for all threads
            barrier.wait()

            if thread_id == 0:
                # Prepare the next BFS level
                frontier[:] = next_frontier
                next_frontier.clear()
                level_holder[0] += 1
                done_holder[0] = (len(frontier) == 0)

            # Synchronize before continuing
            barrier.wait()

            if done_holder[0]:
                return

    threads = [
        threading.Thread(target=worker, args=(i,))
        for i in range(n_threads)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return visited, levels


if __name__ == "__main__":
    import time

    print("=" * 55)
    print("THREADED BFS - DEMO")
    print("=" * 55)

    # Generate a sample graph
    adj = generate_graph(n_nodes=2000, avg_degree=6, seed=1)

    for n_threads in [1, 2, 4, 8]:
        start = time.perf_counter()

        visited, levels = bfs_threaded(
            adj,
            source=0,
            n_threads=n_threads,
            work_iterations=2000,
        )

        elapsed = time.perf_counter() - start

        print(
            f"threads={n_threads:<2}  "
            f"visited={len(visited):<5}  "
            f"max_level={max(levels.values())}  "
            f"time={elapsed:.4f}s"
        )

    print("=" * 55)