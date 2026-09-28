"""Interactive Streamlit visualization for GBFS and A* search."""

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from searchAlgos import a_star, gbfs, hospital_graph, locations


st.set_page_config(
    page_title="Emergency Supply Robot Search",
    page_icon="🏥",
    layout="wide",
)

st.title("Emergency Supply Robot: Informed Search")
st.write(
    "Choose a start location, goal location, and search algorithm. "
    "The app runs the search on the hospital's directed, weighted graph and "
    "highlights the returned solution path."
)

nodes = list(hospital_graph)
control_col, graph_col = st.columns([1, 2])

with control_col:
    start = st.selectbox(
        "Select Initial Node",
        nodes,
        index=nodes.index("Pharmacy"),
    )
    goal = st.selectbox(
        "Select Goal Node",
        nodes,
        index=nodes.index("Emergency_Ward"),
    )
    algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])
    run_search = st.button("Run Search", type="primary", width="stretch")

if run_search:
    search_function = gbfs if algorithm == "GBFS" else a_star
    path, cost, expansion_order = search_function(start, goal)

    if path is None:
        st.error(
            "No directed path exists for the selected start and goal nodes. "
            "Try a goal farther along the corridor network."
        )
    else:
        with control_col:
            st.subheader("Search Result")
            st.write(f"**Algorithm:** {algorithm}")
            st.write(f"**Solution Path:** {' → '.join(path)}")
            st.write(f"**Total Path Cost:** {cost:.2f}")
            st.write(f"**Expansion Order:** {' → '.join(expansion_order)}")
            st.metric("Nodes Expanded", len(expansion_order))

        graph = nx.DiGraph()
        for node, neighbors in hospital_graph.items():
            graph.add_node(node)
            for neighbor, weight in neighbors.items():
                graph.add_edge(node, neighbor, weight=weight)

        path_edges = list(zip(path, path[1:]))
        normal_edges = [edge for edge in graph.edges if edge not in path_edges]

        fig, ax = plt.subplots(figsize=(11, 7))
        nx.draw_networkx_nodes(
            graph,
            locations,
            node_color="#D9EAF7",
            edgecolors="#1F4E78",
            node_size=2300,
            linewidths=1.5,
            ax=ax,
        )
        nx.draw_networkx_nodes(
            graph,
            locations,
            nodelist=path,
            node_color="#FFD966",
            edgecolors="#B45F06",
            node_size=2400,
            linewidths=2,
            ax=ax,
        )
        nx.draw_networkx_labels(
            graph,
            locations,
            labels={node: node.replace("_", "\n") for node in graph.nodes},
            font_size=9,
            font_weight="bold",
            ax=ax,
        )
        nx.draw_networkx_edges(
            graph,
            locations,
            edgelist=normal_edges,
            edge_color="#7F8C8D",
            width=1.8,
            arrows=True,
            arrowsize=20,
            ax=ax,
        )
        nx.draw_networkx_edges(
            graph,
            locations,
            edgelist=path_edges,
            edge_color="#D62728",
            width=4,
            arrows=True,
            arrowsize=24,
            ax=ax,
        )
        nx.draw_networkx_edge_labels(
            graph,
            locations,
            edge_labels=nx.get_edge_attributes(graph, "weight"),
            font_size=9,
            label_pos=0.55,
            ax=ax,
        )
        ax.set_title(f"{algorithm} Solution Path", fontsize=16, fontweight="bold")
        ax.axis("off")
        fig.tight_layout()

        with graph_col:
            st.pyplot(fig, width="stretch")
        plt.close(fig)
else:
    with graph_col:
        st.info("Choose the search settings and click **Run Search**.")

