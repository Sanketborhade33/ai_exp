import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Custom BFS implementation
def bfs(G, start, target):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == target:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]  # Return reversed path from start to target
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    return []  # No path found

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

# Add nodes to the graph
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

# Perform BFS from node 4 (D) to node 3 (C)
shortest_path = bfs(G, start=4, target=3)

# Generate layout
pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(
    G,
    pos,
    with_labels=False,
    node_size=3000,
    node_color="lightblue",
)

# IP address labels
node_labels = nx.get_node_attributes(G, "ip")
label_pos = {key: (value[0] + 0.1, value[1]) for key, value in pos.items()}
nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=8, font_color="red")

# Alphabetic labels (A, B, C...) for each node
alphabetic_labels = {node: chr(64 + node) for node in G.nodes()}  # 1->A, 2->B, etc.
nx.draw_networkx_labels(G, pos, labels=alphabetic_labels, font_size=10, font_color="blue")

# Highlight path (nodes and edges)
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color="yellow", node_size=3000)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="orange", width=2)

# Draw edge weights
edge_weights = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, font_size=8, font_color="green")

# Final touches
plt.title("Computer Network with BFS Path from D to C")
plt.axis("off")
plt.show()
