import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Custom DFS implementation
def dfs(G, start, target):
    # Initialize stack for DFS, visited set, and parent map
    stack = [start]
    visited = set([start])
    parent = {start: None}

    while stack:
        node = stack.pop()
        if node == target:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]  # Return reversed path from start to target

        # Explore neighbors in reverse order (like recursive DFS)
        for neighbor in reversed(list(G.neighbors(node))):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                stack.append(neighbor)

    return []  # Return empty list if no path is found

# Create a new graph
G = nx.Graph()

# Add nodes with IP addresses
ip_addresses = {
    1: "192.168.1.1",
    2: "192.168.1.2",
    3: "192.168.1.3",
    4: "192.168.1.4",
    5: "192.168.1.5",
    6: "192.168.1.6",
}

for node, ip in ip_addresses.items():
    G.add_node(node, ip=ip)

# Define connections with uneven weights
connections = [
    (1, 2, 5),
    (1, 3, 3),
    (1, 4, 1),
    (2, 5, 6),
    (3, 6, 7),
    (4, 5, 2),
    (4, 6, 4),
    (5, 6, 3),
]

# Add weighted edges
G.add_weighted_edges_from(connections)

# Perform DFS from node 4 (D) to node 3 (C)
path_dfs = dfs(G, start=4, target=3)

# Layout for graph visualization
pos = nx.spring_layout(G, seed=42)

# Plotting the graph
plt.figure(figsize=(8, 6))

# Draw base graph
nx.draw(
    G,
    pos,
    with_labels=False,
    node_size=3000,
    node_color="lightblue",
)

# IP labels
node_labels = nx.get_node_attributes(G, "ip")
label_pos = {key: (value[0] + 0.1, value[1]) for key, value in pos.items()}
nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=8, font_color="red")

# Alphabetic node labels (A, B, C...)
alphabetic_labels = {node: chr(64 + node) for node in G.nodes()}  # 1->A, etc.
nx.draw_networkx_labels(G, pos, labels=alphabetic_labels, font_size=10, font_color="blue")

# Highlight DFS path
path_edges = list(zip(path_dfs, path_dfs[1:]))
path_nodes = set(path_dfs)
nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color="yellow", node_size=3000)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="orange", width=2)

# Edge weights
edge_weights = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_size=8, font_color="green")

# Title and clean-up
plt.title("Computer Network with Custom DFS Path from D to C (Uneven Distances)")
plt.axis("off")
plt.show()
