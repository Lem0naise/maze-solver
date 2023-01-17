from tkinter import *
from time import sleep

class Outputter:
	def __init__(self, maze, path, delay):
		print("Starting window...");
		self.delay = delay;
		self.path = path;

		height = len(maze)
		width = len(maze[0]);

		# tkinter
		self.window = Tk();
		self.window.title("Maze Solver");
		self.window.geometry(f"{width*10}x{height*10}"); # calculate needed height and width
		self.window.columnconfigure(0, weight=0)
		
		self.cells = []

		for i in range(height):
			row = [];
			for j in range(width):
				colour_l = self.colour_calc(maze[i][j])

				l = Canvas(self.window, bg=colour_l, width=10, height=10, highlightthickness=0);
				l.grid(row=i, column = j, sticky="nsew");
				row.append(l);

			self.cells.append(row);

	def solve(self): # draw path
		
		print("Drawing path...");
		
		for each in self.path:

			e1, e2 = each; #tuple to two values

			self.cells[e1][e2].config(bg="red"); # change value to red
			sleep(self.delay) # sleep value before updating
			self.window.update(); # update window

		self.window.mainloop();

	def colour_calc(self, cell):

		colour = "nothing";

		if cell == 0:
			colour = "white";
		elif cell == 1:
			colour = "black";
		elif cell == 2:
			colour = "yellow";
		elif cell == 3:
			colour = "green";
		elif cell == 4:
			colour = "red";

		return colour;