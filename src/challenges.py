"""Week 12: Monster Hunter Graphs — Challenge implementations."""

from __future__ import annotations


def build_hunter_map(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Build an undirected adjacency-list graph from a list of (a, b) edges.

    - Both directions are added.
    - Duplicate neighbours are ignored (no self-loops or repeated edges).
    """
    graph: dict[str, set[str]] = {}

    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    # Convert sets to lists for output
    return {node: list(neighbors) for node, neighbors in graph.items()}


def build_weighted_hunter_map(
    edges: list[tuple[str, str, int | float]],
) -> dict[str, dict[str, int | float]]:
    """Build an undirected weighted adjacency-map graph.

    - Both directions are added with the same weight.
    - If the same edge appears more than once, keep the lowest weight.
    - Raises ValueError for zero or negative weights.
    """
    graph: dict[str, dict[str, int | float]] = {}

    for a, b, weight in edges:
        if weight <= 0:
            raise ValueError(
                f"Edge weight must be positive, got {weight} for ({a!r}, {b!r})."
            )

        graph.setdefault(a, {})
        graph.setdefault(b, {})

        # Keep the lowest weight if the edge already exists
        current_ab = graph[a].get(b)
        new_weight = weight if current_ab is None else min(current_ab, weight)

        graph[a][b] = new_weight
        graph[b][a] = new_weight

    return graph


def map_summary(graph: dict[str, list[str]]) -> dict[str, int]:
    """Return a dict with the number of locations and undirected routes.

    Each undirected edge is counted once (not twice).
    """
    locations = len(graph)
    # Each edge is stored twice, so divide by 2
    routes = sum(len(neighbors) for neighbors in graph.values()) // 2
    return {"locations": locations, "routes": routes}


def most_connected_location(graph: dict[str, list[str]]) -> str | None:
    """Return the location with the most neighbours (highest degree).

    Ties are broken alphabetically (lexicographically smallest name wins).
    Returns None for an empty graph.
    """
    if not graph:
        return None

    # (-degree, name) → highest degree first, ties broken alphabetically
    return min(graph, key=lambda node: (-len(graph[node]), node))


def priority_hunt_order(reports: list[tuple[int, str]]) -> list[str]:
    """Return location names sorted by ascending priority number.

    Ties in priority are broken alphabetically by location name.
    """
    sorted_reports = sorted(reports, key=lambda r: (r[0], r[1]))
    return [location for _, location in sorted_reports]