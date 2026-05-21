from __future__ import annotations

import heapq
from typing import Dict, List, Tuple, Optional


def build_hunter_map(edges: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """Build an undirected adjacency list from route pairs.

    Each tuple represents a two-way route between two monster sighting
    locations.

    Args:
        edges: A list of route pairs, such as
            [("Old Theater", "Train Station")].

    Returns:
        A dictionary where each key is a location and each value is a list
        of neighboring locations.

    Rules:
        - Add both directions for each route.
        - Include every location that appears in the input.
        - Do not duplicate neighbors if the same route appears more than once.
    """
    graph: Dict[str, List[str]] = {}

    for a, b in edges:
        if a not in graph:
            graph[a] = []

        if b not in graph:
            graph[b] = []

        if b not in graph[a]:
            graph[a].append(b)

        if a not in graph[b]:
            graph[b].append(a)

    return graph


def build_weighted_hunter_map(
    edges: List[Tuple[str, str, int]]
) -> Dict[str, Dict[str, int]]:
    """Build an undirected weighted graph from route triples.

    Each tuple represents a two-way route with a positive danger score.

    Args:
        edges: A list of route triples, such as
            [("Old Theater", "Train Station", 4)].

    Returns:
        A nested dictionary where graph[start][end] is the danger score.

    Rules:
        - Add both directions for each route.
        - Danger scores must be positive integers.
        - If danger score is 0 or negative, raise ValueError.
        - If the same route appears more than once, keep the lowest score.
    """
    graph: Dict[str, Dict[str, int]] = {}

    for a, b, weight in edges:
        if weight <= 0:
            raise ValueError("Danger score must be positive")

        if a not in graph:
            graph[a] = {}

        if b not in graph:
            graph[b] = {}

        if b not in graph[a] or weight < graph[a][b]:
            graph[a][b] = weight
            graph[b][a] = weight

    return graph


def map_summary(graph: Dict[str, List[str]]) -> Dict[str, int]:
    """Return the number of locations and undirected routes.

    Args:
        graph: An undirected adjacency list.

    Returns:
        A dictionary with:
            - "locations": number of locations
            - "routes": number of undirected routes
    """
    locations = len(graph)
    routes = sum(len(neighbors) for neighbors in graph.values()) // 2

    return {
        "locations": locations,
        "routes": routes,
    }


def most_connected_location(
    graph: Dict[str, List[str]]
) -> Optional[str]:
    """Return the location with the most neighbors.

    Args:
        graph: An undirected adjacency list.

    Returns:
        The location with the most neighbors.
        If the graph is empty, return None.
        If there is a tie, return the alphabetically first location.
    """
    if not graph:
        return None

    return min(
        graph,
        key=lambda location: (-len(graph[location]), location),
    )


def priority_hunt_order(
    reports: List[Tuple[int, str]]
) -> List[str]:
    """Return monster sighting locations from most urgent to least urgent.

    Lower priority number means more urgent.

    Args:
        reports: A list of tuples in the form (priority, location).

    Returns:
        A list of locations ordered from lowest priority number to highest.

    Requirement:
        Use heapq.
    """
    heap = []

    for priority, location in reports:
        heapq.heappush(heap, (priority, location))

    result = []

    while heap:
        _, location = heapq.heappop(heap)
        result.append(location)

    return result