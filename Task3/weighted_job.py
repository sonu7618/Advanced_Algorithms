from bisect import bisect_right


# Find the last job that finishes before the current job starts
def find_previous(end_times, start_time, limit):
    index = bisect_right(end_times, start_time, 0, limit)
    return index - 1


# Dynamic Programming Solution
def schedule_jobs(jobs):

    jobs = sorted(jobs, key=lambda x: x[1])
    n = len(jobs)

    end_times = [job[1] for job in jobs]
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        start, end, profit = jobs[i - 1]

        previous = find_previous(end_times, start, i - 1)

        take = profit + dp[previous + 1]
        skip = dp[i - 1]

        dp[i] = max(take, skip)

    return dp[n], dp, jobs


# Simple O(n²) method for comparison
def schedule_jobs_naive(jobs):

    jobs = sorted(jobs, key=lambda x: x[1])
    n = len(jobs)

    dp = [0] * (n + 1)

    for i in range(1, n + 1):

        start, end, profit = jobs[i - 1]

        previous = -1

        for j in range(i - 2, -1, -1):
            if jobs[j][1] <= start:
                previous = j
                break

        take = profit + dp[previous + 1]
        skip = dp[i - 1]

        dp[i] = max(take, skip)

    return dp[n]


# Find which jobs were selected
def reconstruct_selection(dp, jobs):

    end_times = [job[1] for job in jobs]
    selected = []

    i = len(jobs)

    while i > 0:

        start, end, profit = jobs[i - 1]

        previous = find_previous(end_times, start, i - 1)

        take = profit + dp[previous + 1]

        if take > dp[i - 1]:
            selected.append(jobs[i - 1])
            i = previous + 1
        else:
            i -= 1

    selected.reverse()
    return selected


if __name__ == "__main__":

    jobs = [
        (1, 3, 50),
        (2, 5, 20),
        (4, 6, 70),
        (6, 7, 60),
        (5, 8, 30),
        (7, 9, 40)
    ]

    print("Weighted Job Scheduling")
    print("-" * 35)

    print("\nJobs:")
    for job in jobs:
        print(job)

    max_profit, dp, sorted_jobs = schedule_jobs(jobs)

    selected_jobs = reconstruct_selection(dp, sorted_jobs)

    print("\nDP Table:")
    for i in range(len(dp)):
        print(f"dp[{i}] = {dp[i]}")

    print("\nSelected Jobs:")
    for job in selected_jobs:
        print(job)

    print("\nMaximum Profit:", max_profit)

    naive_profit = schedule_jobs_naive(jobs)

    print("Naive Solution Profit:", naive_profit)

    if max_profit == naive_profit:
        print("Both methods give the same result.")