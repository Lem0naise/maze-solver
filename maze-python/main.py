from solve_dfs import MazeSolver_dfs;
from solve_bfs import MazeSolver_bfs;
from recognize import Recogniser;


''' 
depth first search (dfs) v. breadth first search (bfs)
------------------------------------------------------

dfs - significantly faster, doesn't always get the shortest path
bfs - significantly slower, always gets the shortest possible path

'''

# Display & Traversal Options

CAMERA = 0
resolution = (200, 200) # width, height

transversal_algo = 'dfs' # dfs / bfs

dfs_opts = {
    'show_dfs': True,
    'show_dfs_delay': 0, # 0 for instant
    'dfs_line_colour': (100, 100, 255),
    'dfs_thickness': 1,
    'hide_dfs_on_bfs_show': False, # hide dfs path when bfs path is calculated
    'show_dfs_debug': False
}

dfs_bfs_opts = { # bfs after dfs
    'show_bfs_cleanup': False,
    'show_bfs_delay': 1, # 0 for instant
    'bfs_line_colour': (222, 98, 91),
    'bfs_thickness': 3,
    'show_bfs_debug': False
}

only_bfs_opts = {
    'show_debug': False,
    'show_loading': False,
    'line_thickness': 3,
    'line': True,
    'line_colour': (222, 98, 91),
    'entity': False,
    'entity_colour': (100, 100, 255),
    'delay':1
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

if transversal_algo == 'dfs':
    solver = MazeSolver_dfs(maze, recogniser, dfs_opts, dfs_bfs_opts);
elif transversal_algo == 'bfs':
    solver = MazeSolver_bfs(maze, recogniser, only_bfs_opts['show_debug'], only_bfs_opts['show_loading'], only_bfs_opts['line_thickness'], only_bfs_opts['line'], only_bfs_opts['line_colour'], only_bfs_opts['entity'], only_bfs_opts['entity_colour'], only_bfs_opts['delay']);
else:
    print(f'Traversal algorithm "{str(transversal_algo)}" not recognised.')
