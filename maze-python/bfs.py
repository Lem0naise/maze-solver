import time
import numpy as np

def path_to_bfs(path, height, width):
    # turning path into a 2d array
    maze = np.zeros((height, width))
    maze = np.invert(maze)

    for each in path:
        y, x = each
        maze[y][x] = 0

    print(maze)

def populate_maze(maze_in, start, end):

    stepped_pixels = 0
    
    # numpy.zeros()
    maze = []
    for i in range(len(maze_in)):
        maze.append([])
        for j in range(len(maze_in[i])):
            maze[-1].append(0)


    sy, sx = start;
    maze[sy][sx] = 1; # set starting point as "1" minimum path length
    
    ey, ex = end; # TODO doesn't even change anything if i switch x and y

    maze_in[ey][ex] = 0 # set the end to 0

    step = 1; # distance from start

    height = len(maze)
    width = len(maze[0])

    # TODO SOMETIMES GET STUCK IN THIS WHILE LOOP WHILE END IS BELOW START (doesn't populate below start y coord)
    
    prev_prog = 0
    while maze[ey][ex] == 0: # while end not pathfound to (while end is still an empty cell)

        move(maze, maze_in, step, height, width)
        step += 1; # increment distance
    
        # TODO debug print
        if step % 2000 == 0:
            print(step)

    return maze;


def move( maze, maze_input, step, height, width): # maze is the populating maze, and maze_input is the actual image
    
    # go through whole maze to find cells which match the current step
    for i in range(height):
        for j in range(width):

            # TODO problem is that: i > ey is never true as well as the if statement below

            if maze[i][j] == step: # if cell is within reach (match the current distance / step)
                
                # {guard clause} and {if we have not reached the cell yet} and {there is no wall}
                # then: set cell to NEXT STEP
                if i>0 and maze[i-1][j] == 0 and maze_input[i-1][j] == 0: # cell North
                    maze[i-1][j] = step + 1;
                
                    if j>width-1 and maze[i-1][j+1] == 0 and maze_input[i-1][j+1] == 0: # cell North East
                        maze[i-1][j+1] = step + 1;
                    
                    if j>0 and maze[i-1][j-1] == 0 and maze_input[i-1][j-1] == 0: # cell North West
                        maze[i-1][j-1] = step + 1;

                if i<height-1 and maze[i+1][j] == 0 and maze_input[i+1][j] == 0: # cell South
                    maze[i+1][j] = step + 1;

                    if j<width-1 and maze[i+1][j+1] == 0 and maze_input[i+1][j+1] == 0: # cell South East
                        maze[i+1][j+1] = step + 1;

                    if j>0 and maze[i+1][j-1] == 0 and maze_input[i+1][j-1] == 0: # cell South West
                        maze[i+1][j-1] = step + 1;
                
                if j>0 and maze[i][j-1] == 0 and maze_input[i][j-1] == 0: # cell West
                    maze[i][j-1] = step + 1;
                
                if j<width-1 and maze[i][j+1] == 0 and maze_input[i][j+1] == 0: # cell East
                    maze[i][j+1] = step + 1;

                stepped_pixels +=1


def path_maze( pop_maze, start):
    #nb start is not the start of the maze, but the start of the pathfinding
    #it is actually the end of the maze

    path = [];
    sy, sx = start;
    step = pop_maze[sy][sx]; # set path limit

    while step > 2:

        if sy>0 and pop_maze[sy-1][sx] == step-1: # cell North
            sy -= 1;

        elif sy>0 and sx<len(pop_maze)-1 and pop_maze[sy-1][sx+1] == step-1: # cell North East
            sx += 1
            sy -= 1

        elif sy>0 and sx>0 and pop_maze[sy-1][sx-1] == step-1: # cell North West
            sy -= 1
            sx -= 1

        elif sy<len(pop_maze)-1 and pop_maze[sy+1][sx] == step-1: # cell South
            sy += 1;

        elif sy<len(pop_maze)-1 and sx<len(pop_maze)-1 and pop_maze[sy+1][sx+1] == step-1: # cell South East
            sy += 1;
            sx += 1
        
        elif sy<len(pop_maze)-1 and sx>0 and pop_maze[sy+1][sx-1] == step-1: # cell South West
            sy += 1;
            sx -= 1

        elif sx>0 and pop_maze[sy][sx-1] == step-1: # cell West
            sx -= 1;
        
        elif sx<len(pop_maze)-1 and pop_maze[sy][sx+1] == step-1: # cell East
            sx += 1;

        path.append((sy, sx));
        step -= 1;

    return path;


