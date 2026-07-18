import matplotlib.pyplot as plt
import matplotlib.patches as patches

from weighted_job_scheduling import schedule_jobs, reconstruct_selection
from min_platforms import min_platforms


// Dynamic Programming Visualization

def visualize_job_schedule(jobs, filename="task3_dp_gantt_chart.png"):

    max_profit, dp, sorted_jobs = schedule_jobs(jobs)

    selected_jobs = reconstruct_selection(dp, sorted_jobs)
    selected = set(selected_jobs)

    jobs = sorted(jobs, key=lambda job: job[0])

    fig, ax = plt.subplots(figsize=(9, 0.6 * len(jobs) + 1))

    for i, job in enumerate(jobs):

        start, end, profit = job

        color = "tab:green" if job in selected else "lightgray"

        ax.barh(
            i,
            end - start,
            left=start,
            height=0.6,
            color=color,
            edgecolor="black"
        )

        ax.text(
            start + (end - start) / 2,
            i,
            f"{profit}",
            ha="center",
            va="center",
            fontsize=8,
            color="white" if job in selected else "black"
        )

    ax.set_yticks(range(len(jobs)))
    ax.set_yticklabels([f"Job {i}" for i in range(len(jobs))])

    ax.set_xlabel("Time")
    ax.set_title(f"Weighted Job Scheduling (Profit = {max_profit})")
    ax.invert_yaxis()

    ax.legend(handles=[
        patches.Patch(color="tab:green", label="Selected"),
        patches.Patch(color="lightgray", label="Skipped")
    ])

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

    print(f"Saved {filename}")


// Greedy Visualization

def visualize_platform_timeline(arrivals, departures,
                                filename="task3_greedy_platform_timeline.png"):

    n = len(arrivals)

    trains = sorted(range(n), key=lambda i: arrivals[i])

    free_time = []
    platform = [0] * n

    for train in trains:

        placed = False

        for p in range(len(free_time)):

            if free_time[p] <= arrivals[train]:

                free_time[p] = departures[train]
                platform[train] = p
                placed = True
                break

        if not placed:
            free_time.append(departures[train])
            platform[train] = len(free_time) - 1

    total_platforms = min_platforms(arrivals, departures)

    fig, ax = plt.subplots(figsize=(9, 0.6 * total_platforms + 1))

    colors = plt.cm.tab10.colors

    for i in range(n):

        ax.barh(
            platform[i],
            departures[i] - arrivals[i],
            left=arrivals[i],
            height=0.6,
            color=colors[i % len(colors)],
            edgecolor="black"
        )

        ax.text(
            arrivals[i] + (departures[i] - arrivals[i]) / 2,
            platform[i],
            f"{arrivals[i]}-{departures[i]}",
            ha="center",
            va="center",
            fontsize=8
        )

    ax.set_yticks(range(total_platforms))
    ax.set_yticklabels([f"Platform {i+1}" for i in range(total_platforms)])

    ax.set_xlabel("Time")
    ax.set_title(f"Minimum Platforms ({total_platforms} Platforms)")
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

    print(f"Saved {filename}")


// Backtracking Visualization

def visualize_search_space(filename="task3_backtracking_search_space.png"):

    from hamiltonian_path import hamiltonian_path
    import random

    sizes = [8, 10, 12, 14]

    plain = []
    heuristic = []

    for n in sizes:

        random.seed(42)

        graph = {i: [] for i in range(n)}

        for u in range(n):
            for v in range(n):
                if u != v and random.random() < 0.4:
                    graph[u].append(v)

        _, plain_nodes = hamiltonian_path(graph, 0, use_heuristic=False)
        _, heuristic_nodes = hamiltonian_path(graph, 0, use_heuristic=True)

        plain.append(plain_nodes)
        heuristic.append(heuristic_nodes)

    x = range(len(sizes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(
        [i - width / 2 for i in x],
        plain,
        width,
        label="Plain",
        color="tab:red"
    )

    ax.bar(
        [i + width / 2 for i in x],
        heuristic,
        width,
        label="Heuristic",
        color="tab:green"
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels([f"n={n}" for n in sizes])

    ax.set_ylabel("Nodes Explored")
    ax.set_title("Hamiltonian Path Search Space")
    ax.legend()

    ax.grid(True, axis="y")

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

    print(f"Saved {filename}")


// Main Program

if __name__ == "__main__":

    jobs = [
        (1, 3, 50),
        (2, 5, 20),
        (4, 6, 70),
        (6, 7, 60),
        (5, 8, 30),
        (7, 9, 40)
    ]

    visualize_job_schedule(jobs)

    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]

    visualize_platform_timeline(arrivals, departures)

    visualize_search_space()