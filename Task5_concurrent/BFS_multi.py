import multiprocessing as mp

from graph_gen import generate_graph, node_work


# Worker process for parallel BFS
def _worker(worker_id, n_workers, adj, manager_ns, visited_set,
            next_frontier_list, levels_dict, lock,
            work_semaphore, barrier, work_iterations, done_flag):

    while True:
        frontier = manager_ns.frontier
        my_chunk = frontier[worker_id::n_workers]

        # Store newly discovered nodes locally
        local_new = []

        for u in my_chunk:
            for v in adj[u]:
                with lock:
                    if v in visited_set:
                        continue
                    visited_set[v] = True
                    levels_dict[v] = manager_ns.level + 1

                with work_semaphore:
                    node_work(v, work_iterations)

                local_new.append(v)

        # Update shared frontier
        with lock:
            next_frontier_list.extend(local_new)

        barrier.wait()

        if worker_id == 0:
            manager_ns.frontier = list(next_frontier_list)
            del next_frontier_list[:]
            manager_ns.level += 1
            done_flag.value = 1 if len(manager_ns.frontier) == 0 else 0

        barrier.wait()

        if done_flag.value:
            return


# Multiprocessing Breadth-First Search
def bfs_multiprocessing(adj, source, n_workers=4,
                        work_iterations=2000,
                        max_concurrent_work=None):

    if max_concurrent_work is None:
        max_concurrent_work = n_workers

    with mp.Manager() as manager:
        visited_set = manager.dict()
        levels_dict = manager.dict()
        next_frontier_list = manager.list()
        ns = manager.Namespace()
        done_flag = manager.Value("i", 0)

        visited_set[source] = True
        levels_dict[source] = 0
        node_work(source, work_iterations)

        ns.frontier = [source]
        ns.level = 0

        lock = mp.Lock()
        work_semaphore = mp.Semaphore(max_concurrent_work)
        barrier = mp.Barrier(n_workers)

        processes = [
            mp.Process(
                target=_worker,
                args=(
                    i, n_workers, adj, ns, visited_set,
                    next_frontier_list, levels_dict,
                    lock, work_semaphore, barrier,
                    work_iterations, done_flag,
                ),
            )
            for i in range(n_workers)
        ]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        return set(visited_set.keys()), dict(levels_dict)


if __name__ == "__main__":
    import time

    print("=" * 55)
    print("MULTIPROCESSING BFS - DEMO")
    print("=" * 55)

    # Generate a sample graph
    adj = generate_graph(n_nodes=2000, avg_degree=6, seed=1)

    for n_workers in [1, 2, 4, 8]:
        start = time.perf_counter()

        visited, levels = bfs_multiprocessing(
            adj,
            source=0,
            n_workers=n_workers,
            work_iterations=2000,
        )

        elapsed = time.perf_counter() - start

        print(
            f"processes={n_workers:<2}  "
            f"visited={len(visited):<5}  "
            f"max_level={max(levels.values())}  "
            f"time={elapsed:.4f}s"
        )

    print("=" * 55)