import matplotlib.pyplot as plt
import networkx as nx

# Define states (ignoring M variables, only outputs and timers)
states = [
    "WAIT_FOR_START\n(I0.0=1)",
    "STATE 1\nQ0.3=1\nTM1 5s",
    "STATE 2\nQ0.1=1\nTM2 2s",
    "STATE 3\nQ0.2=1\nTM3 2.5s",
    "STATE 4\nQ0.0=1"
]

# Define transitions (start_state, end_state, label)
edges = [
    (0, 1, "Start Condition"),
    (1, 2, "TM1 Done"),
    (2, 3, "TM2 Done"),
    (3, 4, "TM3 Done"),
    (4, 0, "Reset Condition")
]

# Create directed graph
G = nx.DiGraph()
for i, label in enumerate(states):
    G.add_node(i, label=label)

for start, end, label in edges:
    G.add_edge(start, end, label=label)

# Layout (circular for clarity)
pos = nx.circular_layout(G)

# Draw nodes
plt.figure(figsize=(8, 8))
nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=3000, edgecolors="black")
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, "label"), font_size=8)

# Draw edges with labels
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color="black")
nx.draw_networkx_edge_labels(
    G, pos, 
    edge_labels={(u, v): d["label"] for u, v, d in G.edges(data=True)}, 
    font_size=8
)

# Title
plt.axis("off")
plt.title("State Diagram for Ladder Logic", fontsize=12, fontweight="bold")
plt.show()
