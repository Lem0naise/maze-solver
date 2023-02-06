from solve import MazeSolver;
from recognize import Recogniser;
from time import sleep;

# Runtime Parameters (N.B. Makes significantly slower)
show_debug = False
show_loading = False

# Solution Display Options (Negligibly affect speed)
line_thickness = 6
line_colour = (222, 98, 91)
entity_colour = (50, 50, 50) # colour of snake head
line = True # boolean, snake body or not
entity = True # boolean, snake head or not
delay = 1 # ms, integer, >0


# TODO CANNOT GO BELOW 
recogniser = Recogniser();
print('finished with recogniser')
frame = recogniser.frame;
while frame.any() == None:
    frame = recogniser.frame;
maze = frame;

height = len(maze)
width = len(maze[0])

solver = MazeSolver(maze, recogniser, show_debug, show_loading, line_thickness, line, line_colour, entity, entity_colour, delay);
