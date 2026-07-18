# Minimum Number of Platforms using Greedy Algorithm

def min_platforms(arrivals, departures):
    n = len(arrivals)

    # Sort arrival and departure times
    arrivals.sort()
    departures.sort()

    i = 0
    j = 0
    current_platforms = 0
    max_platforms = 0

    while i < n and j < n:
        if arrivals[i] <= departures[j]:
            current_platforms += 1
            if current_platforms > max_platforms:
                max_platforms = current_platforms
            i += 1
        else:
            current_platforms -= 1
            j += 1

    return max_platforms


# Simple brute-force method to verify the result
def brute_force_platforms(arrivals, departures):
    n = len(arrivals)
    answer = 0

    for time in arrivals:
        count = 0
        for i in range(n):
            if arrivals[i] <= time <= departures[i]:
                count += 1
        answer = max(answer, count)

    return answer


if __name__ == "__main__":

    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]

    print("Train Schedule")
    print("-" * 30)

    for a, d in zip(arrivals, departures):
        print(f"Arrival: {a}  Departure: {d}")

    greedy_result = min_platforms(arrivals[:], departures[:])
    brute_result = brute_force_platforms(arrivals, departures)

    print("\nMinimum Platforms (Greedy):", greedy_result)
    print("Minimum Platforms (Brute Force):", brute_result)

    if greedy_result == brute_result:
        print("Both methods give the same answer.")