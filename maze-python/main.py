from solve_dfs import MazeSolver_dfs;
from solve_bfs import MazeSolver_bfs;
from recognize import Recogniser;
import cv2


''' 
depth first search (dfs) v. breadth first search (bfs)
------------------------------------------------------

dfs - significantly faster, doesn't always get the shortest path
bfs - significantly slower, always gets the shortest possible path

'''

# Display & Traversal Options

CAMERA = 1
resolution = (300, 300) # height, width

traversal_algo = 'dfs' # dfs / bfs / both

dfs_opts = {
    'show_dfs': True,
    'show_dfs_delay': 0.1, # 0 for instant, can be float
    'dfs_line_colour': (100, 100, 255),
    'dfs_thickness': 5,
    'hide_dfs_on_bfs_show': False, # hide dfs path when bfs path is calculated
    'show_dfs_debug': False,
}
dfs_bfs_opts = { # bfs after dfs
    'show_bfs_cleanup': False,
    'show_bfs_delay': 1, # 0 for instant, int only
    'bfs_line_colour': (222, 98, 91),
    'bfs_thickness': 3,
    'show_bfs_debug': False
}


only_bfs_opts = {
    'show_debug': False,
    'show_loading': False,
    'line_thickness': 4,
    'line': True,
    'line_colour': (222, 98, 91),
    'entity': False,
    'entity_colour': (111, 49, 41),
    'delay':1
}

cap = cv2.VideoCapture(CAMERA) # capture object

dfs_opts['both_dfs_and_bfs'] = False
while True:

    print('\n') # lil space

    recogniser = Recogniser(resolution, cap);

    # waiting for frame
    frame = recogniser.frame;
    while frame.any() == None:
        frame = recogniser.frame;
    maze = frame;

    height = len(maze)
    width = len(maze[0])

    if traversal_algo == 'dfs':
        solver = MazeSolver_dfs(maze, recogniser, dfs_opts, dfs_bfs_opts, only_bfs_opts);
    elif traversal_algo == 'bfs':
        solver = MazeSolver_bfs(maze, recogniser, only_bfs_opts['show_debug'], only_bfs_opts['show_loading'], only_bfs_opts['line_thickness'], only_bfs_opts['line'], only_bfs_opts['line_colour'], only_bfs_opts['entity'], only_bfs_opts['entity_colour'], only_bfs_opts['delay'], dfs_opts['both_dfs_and_bfs']);
    elif traversal_algo == 'both':
        dfs_opts['both_dfs_and_bfs'] = True
        solver = MazeSolver_dfs(maze, recogniser, dfs_opts, dfs_bfs_opts, only_bfs_opts);
    else:
        print(f'Traversal algorithm "{str(traversal_algo)}" not recognised.')


recogniser.cap.release() # never runs