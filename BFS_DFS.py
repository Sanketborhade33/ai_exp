#DFS AND BFS
import tkinter as tk
from collections import deque
import time


network = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}

positions = {
    'A': (100, 100),
    'B': (200, 50),
    'C': (200, 150),
    'D': (300, 30),
    'E': (300, 70),
    'F': (300, 170),
    'G': (400, 170)
}


class RoutingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Packet Routing with BFS & DFS Visualization")
        self.canvas = tk.Canvas(root, width=500, height=300, bg="white")
        self.canvas.pack()

        self.source = tk.StringVar()
        self.destination = tk.StringVar()

        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Label(control_frame, text="Source:").grid(row=0, column=0)
        tk.Entry(control_frame, textvariable=self.source, width=5).grid(row=0, column=1)
        tk.Label(control_frame, text="Destination:").grid(row=0, column=2)
        tk.Entry(control_frame, textvariable=self.destination, width=5).grid(row=0, column=3)

        tk.Button(control_frame, text="Run BFS", command=self.run_bfs).grid(row=0, column=4, padx=5)
        tk.Button(control_frame, text="Run DFS", command=self.run_dfs).grid(row=0, column=5, padx=5)
        tk.Button(control_frame, text="Reset", command=self.draw_graph).grid(row=0, column=6)

        self.node_circles = {}
        self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        self.node_circles = {}

       
        for node in network:
            x1, y1 = positions[node]
            for neighbor in network[node]:
                x2, y2 = positions[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", tags=f"line_{node}_{neighbor}")

   
        for node, (x, y) in positions.items():
            circle = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))
            self.node_circles[node] = circle

    def highlight_path(self, path, color="red"):
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i+1]
            x1, y1 = positions[node1]
            x2, y2 = positions[node2]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3)
            self.root.update()
            time.sleep(0.5)

    def bfs(self, graph, start, goal):
        visited = set()
        queue = deque([[start]])

        if start == goal:
            return [start]

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node not in visited:
                for neighbor in graph[node]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

                    if neighbor == goal:
                        return new_path
                visited.add(node)
        return None

    def dfs(self, graph, start, goal):
        visited = set()
        stack = [[start]]

        if start == goal:
            return [start]

        while stack:
            path = stack.pop()
            node = path[-1]

            if node not in visited:
                for neighbor in graph[node]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)

                    if neighbor == goal:
                        return new_path
                visited.add(node)
        return None

    def run_bfs(self):
        src = self.source.get().strip().upper()
        dest = self.destination.get().strip().upper()
        if src not in network or dest not in network:
            return
        self.draw_graph()
        path = self.bfs(network, src, dest)
        if path:
            self.highlight_path(path, "green")

    def run_dfs(self):
        src = self.source.get().strip().upper()
        dest = self.destination.get().strip().upper()
        if src not in network or dest not in network:
            return
        self.draw_graph()
        path = self.dfs(network, src, dest)
        if path:
            self.highlight_path(path, "blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoutingGUI(root)
    root.mainloop()
