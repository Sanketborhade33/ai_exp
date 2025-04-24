# 5 tower of hanoi
import tkinter as tk
import time

class TowerOfHanoiGUI:
    def __init__(self, disk_count):
        self.disk_count = disk_count
        self.window = tk.Tk()
        self.window.title("Tower of Hanoi")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.rods_x = [150, 300, 450]  # X-coordinates of the rods
        self.rod_width = 10
        self.rod_height = 200
        self.base_y = 300

        self.disks = [[] for _ in range(3)]  # Disks on rods: [rod1, rod2, rod3]
        self.disk_height = 20
        self.disk_colors = ["red", "green", "blue", "orange", "purple", "cyan"]

        self.draw_rods()
        self.create_disks()

        self.window.after(1000, lambda: self.solve(self.disk_count, 0, 1, 2))
        self.window.mainloop()

    def draw_rods(self):
        for x in self.rods_x:
            self.canvas.create_rectangle(x - self.rod_width/2, self.base_y - self.rod_height,
                                         x + self.rod_width/2, self.base_y, fill="black")

    def create_disks(self):
        for i in range(self.disk_count):
            width = 20 + (self.disk_count - i) * 20
            x = self.rods_x[0]
            y = self.base_y - (i + 1) * self.disk_height
            color = self.disk_colors[i % len(self.disk_colors)]
            disk = self.canvas.create_rectangle(x - width//2, y, x + width//2, y + self.disk_height, fill=color)
            self.disks[0].append(disk)

    def move_disk(self, from_rod, to_rod):
        if not self.disks[from_rod]:
            return

        disk = self.disks[from_rod].pop()
        x = self.rods_x[to_rod]
        y = self.base_y - len(self.disks[to_rod]) * self.disk_height - self.disk_height

        # Animate movement
        self.canvas.update()
        time.sleep(0.5)
        coords = self.canvas.coords(disk)
        width = coords[2] - coords[0]
        self.canvas.coords(disk, x - width/2, y, x + width/2, y + self.disk_height)
        self.disks[to_rod].append(disk)
        self.canvas.update()
        time.sleep(0.5)

    def solve(self, n, src, helper, dest):
        if n == 1:
            print(f"Move disk {n} from {src} to {dest}")
            self.move_disk(src, dest)
            return
        self.solve(n - 1, src, dest, helper)
        print(f"Move disk {n} from {src} to {dest}")
        self.move_disk(src, dest)
        self.solve(n - 1, helper, src, dest)

# Set the number of disks
TowerOfHanoiGUI(3)
