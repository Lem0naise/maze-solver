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
		screen_dim = self.window.winfo_screenheight()-100
		height, width = len(maze), len(maze[0])
		self.xdens = screen_dim / width
		self.ydens = screen_dim / height
		self.window.geometry(f'{screen_dim}x{screen_dim}')
		self.canvas = tkinter.Canvas(self.window, width=screen_dim, height=screen_dim, bg='White')
		self.canvas.pack()
		for x in range(width):
			for y in range(height):
				if maze[y][x]== 0:
					self.canvas.create_rectangle(x*self.xdens, y*self.ydens, (x+1)*self.xdens, (y+1)*self.ydens, fill='White',outline='White') 
				if maze[y][x]== 1:
					self.canvas.create_rectangle(x*self.xdens, y*self.ydens, (x+1)*self.xdens, (y+1)*self.ydens, fill='Black',outline='Black')
				if maze[y][x]== 2 or maze[y][x]== 3:
					self.canvas.create_rectangle(x*self.xdens, y*self.ydens, (x+1)*self.xdens, (y+1)*self.ydens, fill='Gold',outline='Gold')
		self.window.update()
		self.window.mainloop();

	def solve(self):
		for y,x in self.path:
			self.window.update()
			self.canvas.create_rectangle(x*self.xdens, y*self.ydens, (x+1)*self.xdens, (y+1)*self.ydens, fill='Green',outline='Green')
			sleep(self.delay)
		self.window.mainloop()