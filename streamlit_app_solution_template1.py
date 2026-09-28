"""Completed single-file version of the supplied Streamlit template."""

import heapq
import math
from itertools import count

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st


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


def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.hypot(x2 - x1, y2 - y1)


def reconstruct_path(came_from, current):
    path = [current]
    while came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def get_path_cost(path):
    return sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal):
    tie_breaker = count()
    frontier = [(heuristic(start, goal), next(tie_breaker), start)]
    came_from = {start: None}
    visited = set()
    expansion_order = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, get_path_cost(path), expansion_order

        for neighbor in hospital_graph[current]:
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (heuristic(neighbor, goal), next(tie_breaker), neighbor),
                )

    return None, math.inf, expansion_order


def a_star(start, goal):
    tie_breaker = count()
    frontier = [(heuristic(start, goal), next(tie_breaker), start)]
    came_from = {start: None}
    g_cost = {node: math.inf for node in hospital_graph}
    g_cost[start] = 0.0
    closed = set()
    expansion_order = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in closed:
            continue
        closed.add(current)
        expansion_order.append(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current], expansion_order

        for neighbor, edge_cost in hospital_graph[current].items():
            tentative_g = g_cost[current] + edge_cost
            if tentative_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g
                heapq.heappush(
                    frontier,
                    (
                        tentative_g + heuristic(neighbor, goal),
                        next(tie_breaker),
                        neighbor,
                    ),
                )
                if neighbor in closed:
                    closed.remove(neighbor)

    return None, math.inf, expansion_order


st.set_page_config(page_title="Emergency Supply Robot Search", page_icon="🏥", layout="wide")
st.title("Emergency Supply Robot: Informed Search")
st.write(
    "Select two hospital locations and compare Greedy Best-First Search with A*. "
    "The returned route is highlighted on the directed, weighted graph."
)

nodes = list(hospital_graph)
start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])

if st.button("Run Search", type="primary"):
    path, cost, expansion_order = (gbfs if algorithm == "GBFS" else a_star)(start, goal)

    if path is None:
        st.error("No directed path exists for the selected start and goal nodes.")
    else:
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Expansion Order:** {' → '.join(expansion_order)}")

        graph = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            graph.add_node(node)
            for neighbor, weight in neighbors.items():
                graph.add_edge(node, neighbor, weight=weight)

        path_edges = list(zip(path, path[1:]))
        normal_edges = [edge for edge in graph.edges if edge not in path_edges]
        fig, ax = plt.subplots(figsize=(11, 7))
        nx.draw_networkx_nodes(
            graph, locations, node_color="#D9EAF7", edgecolors="#1F4E78",
            node_size=2300, linewidths=1.5, ax=ax
        )
        nx.draw_networkx_nodes(
            graph, locations, nodelist=path, node_color="#FFD966",
            edgecolors="#B45F06", node_size=2400, linewidths=2, ax=ax
        )
        nx.draw_networkx_labels(
            graph, locations,
            labels={node: node.replace("_", "\n") for node in graph.nodes},
            font_size=9, font_weight="bold", ax=ax
        )
        nx.draw_networkx_edges(
            graph, locations, edgelist=normal_edges, edge_color="#7F8C8D",
            width=1.8, arrows=True, arrowsize=20, ax=ax
        )
        nx.draw_networkx_edges(
            graph, locations, edgelist=path_edges, edge_color="#D62728",
            width=4, arrows=True, arrowsize=24, ax=ax
        )
        nx.draw_networkx_edge_labels(
            graph, locations,
            edge_labels=nx.get_edge_attributes(graph, "weight"),
            font_size=9, ax=ax
        )
        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        fig.tight_layout()
        st.pyplot(fig, width="stretch")
        plt.close(fig)

