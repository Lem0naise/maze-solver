import tkinter
from copy import deepcopy
from time import sleep
class Outputter:
	def __init__(self, i_maze, path, delay):
		self.delay = delay
		self.path = path
		self.o_maze = deepcopy(i_maze)
		self.draw(self.o_maze)
	def draw(self, maze):
		self.window = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.window, width=500, height=500, bg='White', highlightthickness=1, highlightbackground='White')
		self.canvas.pack()
		self.dens = 500 / 30
		for i in range(30):
			self.canvas.create_line(0, i * self.dens, 500, i * self.dens)
			self.canvas.create_line(i * self.dens, 0, i * self.dens, 500)
		for x in range(30):
			for y in range(30):
				if maze[y][x]== 1:
					self.canvas.create_rectangle(x*self.dens, y*self.dens, (x+1)*self.dens, (y+1)*self.dens, fill='Black')
				if maze[y][x]== 2:
					self.canvas.create_rectangle(x*self.dens, y*self.dens, (x+1)*self.dens, (y+1)*self.dens, fill='Gold')
				if maze[y][x]== 3:
					self.canvas.create_rectangle(x*self.dens, y*self.dens, (x+1)*self.dens, (y+1)*self.dens, fill='Gold')
		self.window.update()

	def solve(self):
		for y,x in self.path:
			self.window.update()
			self.canvas.create_rectangle(x*self.dens, y*self.dens, (x+1)*self.dens, (y+1)*self.dens, fill='Green')
			sleep(self.delay)