from graph_gen import generate_graph
from bfs_sequential import bfs_sequential
from bfs_threaded import bfs_threaded
from bfs_multiprocessing import bfs_multiprocessing


# Compare threaded BFS with sequential BFS
def test_threaded_matches_sequential_single_trial():
    adj = generate_graph(n_nodes=300, avg_degree=5, seed=7)
    seq_visited, seq_levels = bfs_sequential(adj, source=0, work_iterations=10)

    for n_threads in [1, 2, 4, 8]:
        t_visited, t_levels = bfs_threaded(
            adj,
            source=0,
            n_threads=n_threads,
            work_iterations=10,
        )

        assert t_visited == seq_visited, \
            f"threads={n_threads}: visited set mismatch"
        assert t_levels == seq_levels, \
            f"threads={n_threads}: BFS level mismatch"

    print("Threaded BFS matches sequential BFS (all thread counts).")


# Stress test for race conditions
def test_threaded_race_condition_stress_test(trials=25):
    adj = generate_graph(n_nodes=200, avg_degree=6, seed=3)
    seq_visited, seq_levels = bfs_sequential(adj, source=0, work_iterations=5)

    for trial in range(trials):
        visited, levels = bfs_threaded(
            adj,
            source=0,
            n_threads=8,
            work_iterations=5,
        )

        assert visited == seq_visited, \
            f"Trial {trial}: visited set mismatch"
        assert levels == seq_levels, \
            f"Trial {trial}: level mismatch"
        assert len(visited) == len(adj), \
            f"Trial {trial}: not all nodes visited"

    print(f"Threaded BFS stress test passed ({trials} trials).")


# Compare multiprocessing BFS with sequential BFS
def test_multiprocessing_matches_sequential():
    adj = generate_graph(n_nodes=150, avg_degree=5, seed=11)
    seq_visited, seq_levels = bfs_sequential(adj, source=0, work_iterations=10)

    for n_workers in [1, 2, 4]:
        mp_visited, mp_levels = bfs_multiprocessing(
            adj,
            source=0,
            n_workers=n_workers,
            work_iterations=10,
        )

        assert mp_visited == seq_visited, \
            f"processes={n_workers}: visited set mismatch"
        assert mp_levels == seq_levels, \
            f"processes={n_workers}: BFS level mismatch"

    print("Multiprocessing BFS matches sequential BFS.")


# Verify semaphore throttling does not affect correctness
def test_semaphore_throttling_still_correct():
    adj = generate_graph(n_nodes=200, avg_degree=6, seed=5)
    seq_visited, seq_levels = bfs_sequential(adj, source=0, work_iterations=10)

    throttled_visited, throttled_levels = bfs_threaded(
        adj,
        source=0,
        n_threads=8,
        work_iterations=10,
        max_concurrent_work=1,
    )

    assert throttled_visited == seq_visited
    assert throttled_levels == seq_levels

    print("Semaphore throttling correctness test passed.")


# Verify BFS handles disconnected graphs
def test_disconnected_graph_handled():
    adj = generate_graph(n_nodes=50, avg_degree=4, seed=13)
    adj[999] = []

    seq_visited, _ = bfs_sequential(adj, source=0, work_iterations=5)
    t_visited, _ = bfs_threaded(adj, source=0, n_threads=4, work_iterations=5)

    assert 999 not in seq_visited
    assert 999 not in t_visited
    assert t_visited == seq_visited

    print("Disconnected graph test passed.")


if __name__ == "__main__":
    test_threaded_matches_sequential_single_trial()
    test_threaded_race_condition_stress_test()
    test_multiprocessing_matches_sequential()
    test_semaphore_throttling_still_correct()
    test_disconnected_graph_handled()

    print("\nAll correctness tests passed.")