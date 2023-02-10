from solve import MazeSolver;
from recognize import Recogniser;

# Runtime Parameters (N.B. Makes significantly slower)
show_debug = False
show_loading = False

# Solution Display Options
CAMERA = 0
resolution = (200, 200) # width, height

dfs_opts = {
    'show_dfs': True,
    'show_dfs_delay': 0, # 0 for instant
    'dfs_line_colour': (100, 100, 255),
    'dfs_thickness': 1,
    'hide_dfs_on_bfs_show': False # hide dfs path when bfs path is calculated
}

bfs_opts = {
    'show_bfs_cleanup': True,
    'show_bfs_delay': 1, # 0 for instant
    'bfs_line_colour': (222, 98, 91),
    'bfs_thickness': 3
}

print('\n') # lil space

recogniser = Recogniser(resolution, CAMERA);

# waiting for frame
frame = recogniser.frame;
while frame.any() == None:
    frame = recogniser.frame;
maze = frame;

height = len(maze)
width = len(maze[0])
solver = MazeSolver(maze, recogniser, show_debug, dfs_opts, bfs_opts);
