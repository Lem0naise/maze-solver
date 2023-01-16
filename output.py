# william

# zac temporarily
import matplotlib.pyplot as mpl;
from matplotlib import colors as colours;
import numpy as np
from copy import deepcopy
from time import sleep

class Outputter:
	def __init__(self, i_maze, path):
		self.path = path;
		self.o_maze = deepcopy(i_maze);
		self.draw(self.o_maze);

	def draw(self, maze):

		c_map = colours.ListedColormap(['white', 'black', 'gold', 'red']);

		c_fig, c_ax = mpl.subplots();
		c_ax.imshow(maze, cmap=c_map);

		# draw gridlines
		c_ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
		c_ax.set_xticks([]);
		c_ax.set_yticks([]);
		mpl.show();	


	def solve(self):

		for each in self.path:
			print(each)
			self.o_maze[each[0]][each[1]] = 4; # 4 is red for path
			self.draw(self.o_maze)



