from vrptw import evaluate_route, evaluate_solution


def route_distance(route, instance):
    feasible, distance, _ = evaluate_route(route, instance)
    if feasible:
        return distance
    return float("inf")


def try_2opt(routes, instance):
    """Improve a route using 2-opt."""
    for r in range(len(routes)):
        route = routes[r]

        if len(route) < 2:
            continue

        current = route_distance(route, instance)

        for i in range(len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]

                if route_distance(new_route, instance) < current:
                    routes[r] = new_route
                    return True

    return False


def try_relocate(routes, instance):
    """Move one customer to another position or route."""
    total_routes = len(routes)

    for src in range(total_routes):
        for pos in range(len(routes[src])):

            customer = routes[src][pos]
            source_route = routes[src][:pos] + routes[src][pos + 1:]

            before_source = route_distance(routes[src], instance)
            after_source = route_distance(source_route, instance)

            for dst in range(total_routes + 1):

                if dst == src:
                    target_route = source_route
                elif dst < total_routes:
                    target_route = routes[dst]
                else:
                    target_route = []

                if dst == src:
                    before_target = after_source
                else:
                    before_target = route_distance(target_route, instance)

                for insert in range(len(target_route) + 1):

                    if dst == src and insert == pos:
                        continue

                    new_target = (
                        target_route[:insert]
                        + [customer]
                        + target_route[insert:]
                    )

                    after_target = route_distance(new_target, instance)

                    if after_target == float("inf"):
                        continue

                    if dst == src:
                        change = after_target - before_source
                    else:
                        change = (
                            after_source + after_target
                            - before_source
                            - before_target
                        )

                    if change < 0:
                        new_routes = [r[:] for r in routes]
                        new_routes[src] = source_route

                        if dst < total_routes:
                            new_routes[dst] = new_target
                        else:
                            new_routes.append(new_target)

                        routes[:] = [r for r in new_routes if r]
                        return True

    return False


def try_swap(routes, instance):
    """Swap customers between routes."""
    total_routes = len(routes)

    for a in range(total_routes):
        for b in range(a, total_routes):

            route_a = routes[a]
            route_b = routes[b]

            for i in range(len(route_a)):

                if a == b:
                    start = i + 1
                else:
                    start = 0

                for j in range(start, len(route_b)):

                    new_a = route_a[:]
                    new_b = route_b[:]

                    if a == b:
                        new_a[i], new_a[j] = new_a[j], new_a[i]
                        new_b = new_a
                    else:
                        new_a[i], new_b[j] = new_b[j], new_a[i]

                    before = route_distance(route_a, instance)

                    if a != b:
                        before += route_distance(route_b, instance)

                    after = route_distance(new_a, instance)

                    if a != b:
                        after += route_distance(new_b, instance)

                    if after < before and after != float("inf"):
                        routes[a] = new_a

                        if a != b:
                            routes[b] = new_b

                        return True

    return False


def local_search(routes, instance, max_scans=200):
    """Improve the routes until no better solution is found."""

    routes = [r[:] for r in routes]

    for scan in range(max_scans):

        improved = (
            try_2opt(routes, instance)
            or try_relocate(routes, instance)
            or try_swap(routes, instance)
        )

        if not improved:
            return routes, scan

    return routes, max_scans


if __name__ == "__main__":

    from vrptw import generate_instance, greedy_construct

    instance = generate_instance(
        n_customers=15,
        vehicle_capacity=60,
        seed=1,
    )

    routes = greedy_construct(instance, seed=1)

    _, start_distance, start_vehicles = evaluate_solution(routes, instance)

    best_routes, scans = local_search(routes, instance)

    feasible, final_distance, final_vehicles = evaluate_solution(
        best_routes,
        instance,
    )

    print("Initial distance :", round(start_distance, 2))
    print("Final distance   :", round(final_distance, 2))
    print("Vehicles used    :", final_vehicles)
    print("Feasible         :", feasible)
    print("Scans            :", scans)

    print("\nRoutes")

    for i, route in enumerate(best_routes, 1):
        _, distance, _ = evaluate_route(route, instance)
        print(f"Vehicle {i}: {route}  Distance = {distance:.2f}")