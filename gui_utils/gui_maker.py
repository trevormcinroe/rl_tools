"""

"""
# import tkinter
#
#
# class Window(tkinter.Frame):
#     def __init__(self, master=None):
#         tkinter.Frame.__init__(self, master)
#         self.master = master
#
#         menu = tkinter.Menu(self.master)
#         self.master.config(menu=menu)
#
#         file_menu = tkinter.Menu(menu)
#         file_menu.add_command(label="New Run")
#         file_menu.add_command(label="Exit", command=self._exit_program)
#         menu.add_cascade(label="File", menu=file_menu)
#
#
#
#     def _exit_program(self):
#         exit()
#
#
# root = tkinter.Tk()
# app = Window(root)
# root.wm_title("Tkinter window")
# root.mainloop()


import tkinter as tk
import numpy as np

class Window():

    def __init__(self, master=None):
        # tk.Frame.__init__(self, master)
        self.canvas = None

    def place_robot(self, root):
        """"""
        # Our grid is 10x10
        start = np.random.choice([x for x in range(100)])

        robot = tk.Text(root, height=10, width=10)
        robot.pack()
        robot.insert(tk.END, 'R')

    def create_grid(self, event=None):
        """"""
        w = self.canvas.winfo_width()  # Get current width of canvas
        h = self.canvas.winfo_height()  # Get current height of canvas
        self.canvas.delete('grid_line')  # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, w, 100):
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 100):
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')

    def run(self):
        root = tk.Tk()

        self.canvas = tk.Canvas(root, height=1000, width=1000, bg='white')

        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind('<Configure>', self.create_grid)

        self.place_robot(root=root)

        root.mainloop()

# a = Window()
# a.run()

class ArrayGui:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = None
        self.robot_position = None

    def _convert(self):
        """"""
        board = []
        for r in range(self.height):
            holder = []
            for c in range(self.width):
                holder.append('.')
            board.append(holder)

        self.grid = np.array(board)



    def place_robot(self):
        """"""
        robot_position = []
        robot_position.append(np.random.choice(self.width))
        robot_position.append(np.random.choice(self.height))
        self.robot_position = robot_position
        self.grid[robot_position[0], robot_position[1]] = 'R'

    def place_obstacles(self, num_obstacles):
        """"""
        obstacles = []

        for _ in range(num_obstacles):
            on_robot = True

            while on_robot:
                holder = []
                holder.append(np.random.choice(self.width))
                holder.append(np.random.choice(self.height))
                if not holder == self.robot_position:
                    obstacles.append(holder)
                    on_robot = False

        for ob in obstacles:
            self.grid[ob[0], ob[1]] = 'O'

    def read_lidar(self):
        """"""
        pass

    def go(self):
        self._convert()
        self.place_robot()
        self.place_obstacles(num_obstacles=10)
        print(self.grid)



a = ArrayGui(height=15, width=15)
a.go()
