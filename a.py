import networkx as nx
import matplotlib.pyplot as plt
import heapq

def a_star(graph, start, goal, heuristic):
    open_set = []  # Priority queue
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            total_cost = 0
            while current in came_from:
                path.append(current)
                total_cost += graph[came_from[current]][current]
                current = came_from[current]
            path.append(start)
            path.reverse()
            print("Minimum Distance:", total_cost)
            return path

        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

# Define the graph as an adjacency list with costs
graph = {
    'S': {'B': 4, 'C': 3},
    'B': {'F': 5, 'E': 12},
    'C': {'E': 10, 'D': 7},
    'D': {'E': 2},
    'E': {'G': 5},
    'F': {'G': 16},
    'G': {}
}

# Heuristic values
heuristic = {'S': 14, 'B': 12, 'C': 11, 'D': 6, 'E': 4, 'F': 11, 'G': 0}

# Run A*
start, goal = 'S', 'G'
path = a_star(graph, start, goal, heuristic)
print("A* Path:", path)

# Visualization
def draw_graph(graph, path):
    G = nx.DiGraph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = {
        'S': (0, 2),
        'B': (1, 3),
        'C': (1, 1),
        'D': (2, 0),
        'E': (2, 2),
        'F': (3, 3),
        'G': (4, 2)
    }

    plt.figure(figsize=(10, 7))
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
            node_size=2500, font_size=14, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title("A* Path Visualization", fontsize=14, fontweight='bold')
    plt.show()

# Draw the graph with the A* path
draw_graph(graph, path)
