# Hamiltonian Path and Cycle using Backtracking

def hamiltonian_path(graph, start, cycle=False, heuristic=False):

    visited = {start}
    path = [start]
    total_vertices = len(graph)
    nodes = [0]

    # Count unvisited neighbours (used for heuristic)
    def degree(vertex):
        count = 0
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                count += 1
        return count

    def backtrack():
        nodes[0] += 1

        # If all vertices are visited
        if len(path) == total_vertices:
            if not cycle:
                return True
            return start in graph[path[-1]]

        # Get all unvisited neighbours
        next_vertices = []
        for neighbour in graph[path[-1]]:
            if neighbour not in visited:
                next_vertices.append(neighbour)

        # Try the most constrained vertex first
        if heuristic:
            next_vertices.sort(key=degree)

        for vertex in next_vertices:
            visited.add(vertex)
            path.append(vertex)

            if backtrack():
                return True

            # Backtrack
            path.pop()
            visited.remove(vertex)

        return False

    found = backtrack()

    if found:
        return path, nodes[0]
    else:
        return None, nodes[0]


if __name__ == "__main__":

    graph = {
        "Kathmandu": ["Pokhara", "Butwal"],
        "Pokhara": ["Kathmandu", "Butwal", "Biratnagar"],
        "Butwal": ["Kathmandu", "Pokhara", "Biratnagar"],
        "Biratnagar": ["Pokhara", "Butwal"]
    }

    print("Hamiltonian Path and Cycle")
    print("-" * 35)

    print("\nGraph:")
    for city in graph:
        print(city, "->", graph[city])

    path, explored = hamiltonian_path(graph, "Kathmandu")

    print("\nHamiltonian Path:")
    if path:
        print(" -> ".join(path))
    else:
        print("No Hamiltonian Path Found")
    print("Nodes Explored:", explored)

    cycle_path, explored_cycle = hamiltonian_path(
        graph, "Kathmandu", cycle=True
    )

    print("\nHamiltonian Cycle:")
    if cycle_path:
        print(" -> ".join(cycle_path), "-> Kathmandu")
    else:
        print("No Hamiltonian Cycle Found")
    print("Nodes Explored:", explored_cycle)