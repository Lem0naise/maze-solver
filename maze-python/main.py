from solve import MazeSolver;
from recognize import Recogniser;

# Runtime Parameters (N.B. Makes significantly slower)
show_debug = False
show_loading = False

# Solution Display Options
CAMERA = 0
resolution = (200, 200) # width, height
delay = 1 # ms, integer, >0

line = True # boolean, snake body or not
line_colour = (222, 98, 91)
line_thickness = 2

entity = True # boolean, snake head or not
entity_colour = (50, 20, 20) # colour of snake head


recogniser = Recogniser(resolution, CAMERA);

# waiting for frame
print('finished with recogniser')
frame = recogniser.frame;
while frame.any() == None:
    frame = recogniser.frame;
maze = frame;

height = len(maze)
width = len(maze[0])
solver = MazeSolver(maze, recogniser, show_debug, show_loading, line_thickness, line, line_colour, entity, entity_colour, delay);
