"""Search algorithms and graph data for the Week 6 Streamlit app."""

from __future__ import annotations

import heapq
import math
from itertools import count


locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current: str, goal: str) -> float:
    """Return the Euclidean distance between two hospital locations."""
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.hypot(x2 - x1, y2 - y1)


def reconstruct_path(came_from: dict[str, str | None], current: str) -> list[str]:
    """Reconstruct a start-to-goal path from a parent mapping."""
    path = [current]
    while came_from[current] is not None:
        current = came_from[current]  # type: ignore[assignment]
        path.append(current)
    path.reverse()
    return path


def path_cost(path: list[str]) -> float:
    """Calculate the actual edge cost of a path."""
    return sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start: str, goal: str) -> tuple[list[str] | None, float, list[str]]:
    """Run Greedy Best-First Search using h(n) as the priority."""
    if start not in hospital_graph or goal not in hospital_graph:
        raise ValueError("Start and goal must be valid hospital locations.")

    tie_breaker = count()
    frontier = [(heuristic(start, goal), next(tie_breaker), start)]
    came_from: dict[str, str | None] = {start: None}
    visited: set[str] = set()
    expansion_order: list[str] = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, path_cost(path), expansion_order

        for neighbor in hospital_graph[current]:
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), next(tie_breaker), neighbor),
                )

    return None, math.inf, expansion_order


def a_star(start: str, goal: str) -> tuple[list[str] | None, float, list[str]]:
    """Run A* Search using f(n) = g(n) + h(n)."""
    if start not in hospital_graph or goal not in hospital_graph:
        raise ValueError("Start and goal must be valid hospital locations.")

    tie_breaker = count()
    frontier = [(heuristic(start, goal), next(tie_breaker), start)]
    came_from: dict[str, str | None] = {start: None}
    g_cost = {node: math.inf for node in hospital_graph}
    g_cost[start] = 0.0
    closed: set[str] = set()
    expansion_order: list[str] = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue

        closed.add(current)
        expansion_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_cost[current], expansion_order

        for neighbor, edge_cost in hospital_graph[current].items():
            tentative_g = g_cost[current] + edge_cost
            if tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                priority = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (priority, next(tie_breaker), neighbor),
                )
                if neighbor in closed:
                    closed.remove(neighbor)

    return None, math.inf, expansion_order

