#8 puzzle
import tkinter as tk
import copy

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Manhattan Distance Heuristic
def heuristic(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(i - x) + abs(j - y)
    return distance

# Find position of 0 (blank space)
def get_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate valid children (moves)
def generate_children(state):
    i, j = get_zero(state)
    children = []
    moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    for x, y in moves:
        if 0 <= x < 3 and 0 <= y < 3:
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
            children.append(new_state)
    return children

# Convert state to a hashable tuple
def state_to_tuple(state):
    return tuple(map(tuple, state))

# Draw a single puzzle state
def draw_puzzle(canvas, state, x, y, tag):
    size = 30  # Tile size
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            color = 'white' if val != 0 else 'lightgray'
            canvas.create_rectangle(x + j*size, y + i*size, x + j*size + size, y + i*size + size, fill=color, tags=tag)
            if val != 0:
                canvas.create_text(x + j*size + size/2, y + i*size + size/2, text=str(val), font=('Arial', 10), tags=tag)

# A* Tree Visualization
class AStarTree:
    def __init__(self, canvas, root_state):
        self.canvas = canvas
        self.level_y = 20
        self.x_offset = 120
        self.y_offset = 120
        self.visited = set()
        self.run_astar(root_state, 800, self.level_y, 0)  # Start from center horizontally

    def run_astar(self, state, x, y, depth):
        state_key = state_to_tuple(state)
        if state_key in self.visited:
            return
        self.visited.add(state_key)

        draw_puzzle(self.canvas, state, x, y, tag=str(depth) + str(x))
        cost = heuristic(state) + depth
        self.canvas.create_text(x + 30, y + 90, text=f"f={cost}", font=('Arial', 8))

        if state == GOAL_STATE:
            self.canvas.create_text(x + 30, y - 20, text="GOAL", font=('Arial', 10, 'bold'), fill='green')
            return

        children = generate_children(state)
        children = sorted(children, key=lambda s: heuristic(s) + depth + 1)

        best_child = children[0]
        new_x = x - len(children) * self.x_offset / 2
        for child in children:
            cost = heuristic(child) + depth + 1
            child_x = new_x
            child_y = y + self.y_offset
            draw_puzzle(self.canvas, child, child_x, child_y, tag=str(depth+1) + str(child_x))
            self.canvas.create_text(child_x + 30, child_y + 90, text=f"f={cost}", font=('Arial', 8))
            self.canvas.create_line(x + 30, y + 90, child_x + 30, child_y, arrow=tk.LAST)
            new_x += self.x_offset

        self.canvas.after(1000, lambda: self.run_astar(best_child, x - len(children) * self.x_offset / 2, y + self.y_offset, depth + 1))

# GUI Application with Scrollable Canvas
class PuzzleApp:
    def __init__(self, root_state):
        self.root = tk.Tk()
        self.root.title("8-Puzzle A* Tree Visualization")

        # Create scrollable canvas
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=900, height=600, bg='white', scrollregion=(0, 0, 5000, 3000))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar.config(command=self.canvas.yview)

        self.hbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.hbar.config(command=self.canvas.xview)

        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Search", command=lambda: AStarTree(self.canvas, root_state))
        self.start_button.pack(pady=5)

        self.root.mainloop()

# Initial state (you can change this)
initial_state = [[1, 2, 3],
                 [4, 0, 6],
                 [7, 5, 8]]

PuzzleApp(initial_state)
