# zac
from copy import deepcopy
import cv2
import time
import numpy
from PIL import Image

class MazeSolver:
    def __init__(self, maze, recogniser):
        self.recogniser = recogniser

        n_maze = deepcopy(maze);
        
        start, end = None, None;
        print("Finding start and end.")
        for i in range(len(n_maze)):
            for j in range(len(n_maze[i])):

                # set any 255 to 1
                if n_maze[i][j] == 255:
                    n_maze[i][j] = 1

                if n_maze[i][j] == 2:
                    start = (i, j)
                    n_maze[i][j] = 0;
                if n_maze[i][j] == 3:
                    end = (i, j);
                    n_maze[i][j] = 0;

                if start and end:
                    break;
        print("Found start and end.")

        print("Populating maze...")
        pop_maze = self._populate_maze(n_maze, start, end); # TODO Stuck here
        print("Populated maze.")

        print("Pathing through maze...");
        self.path = self._path_maze(pop_maze, end); # final path
        print("Pathed through maze.");
        print(self.path)

        self.path.reverse();



    def _populate_maze(self, maze_in, start, end):
            
        # turn frame from black and white into rgb
        self.recogniser.frame = cv2.cvtColor(self.recogniser.frame, cv2.COLOR_GRAY2RGB)
        
        # invert image
        maze_in  = numpy.where((maze_in==0)|(maze_in==1), maze_in^1, maze_in)

        # numpy.zeros()
        maze = []
        for i in range(len(maze_in)):
            maze.append([])
            for j in range(len(maze_in[i])):
                maze[-1].append(0)


        sy, sx = start;
        maze[sy][sx] = 1; # set starting point as "1" minimum path length
        ey, ex = end;

        step = 1; # distance from start

        # TODO stuck in this while loop
        # TODO the blueness is not going anywhere below the end

        height = len(maze)
        width = len(maze[0])

        while maze[ey][ex] == 0: # while end not pathfound to (while still is an empty cell)

            self._move(maze, maze_in, step, height, width);
            step += 1; # increment distance

        return maze;


    def _move(self, maze, maze_input, step, height, width): # maze is the populating maze, and maze_input is the actual image
        
        # go through whole maze to find cells which match the current step
        for i in range(len(maze)):
            for j in range(len(maze[i])):
    
                if maze[i][j] == step: # if cell is within reach (match the current distance / step)
                    
                    # {guard clause} and {if we have not reached the cell yet} and {there is no wall}
                    # then: set cell to NEXT STEP
                    if i>0 and maze[i-1][j] == 0 and maze_input[i-1][j] == 0: # cell North
                        maze[i-1][j] = step + 1;

                    if i<height-1 and maze[i+1][j] == 0 and maze_input[i+1][j] == 0: # cell South
                        maze[i+1][j] = step + 1;

                    if j>0 and maze[i][j-1] == 0 and maze_input[i][j-1] == 0: # cell West
                        maze[i][j-1] = step + 1;
                    
                    if j<width-1 and maze[i][j+1] == 0 and maze_input[i][j+1] == 0: # cell East
                        maze[i][j+1] = step + 1;


                    self.recogniser.frame[i, j] = (255, 0, 0) # setting the checked pixels to blue (mostly debug for now)

                    if j%5 == 0: # show every 5 frames
                        cv2.imshow("frame", self.recogniser.frame) # showing the frame
                        cv2.waitKey(1) # required wait statement



    def _path_maze(self, pop_maze, start):
        #nb start is not the start of the maze, but the start of the pathfinding
        #it is actually the end of the maze

        path = [];
        sy, sx = start;
        step = pop_maze[sy][sx]; # set path limit

        while step > 2:

            if sy>0 and pop_maze[sy-1][sx] == step-1: # cell North
                sy -= 1;

            elif sy<len(pop_maze)-1 and pop_maze[sy+1][sx] == step-1: # cell South
                sy += 1;

            elif sx>0 and pop_maze[sy][sx-1] == step-1: # cell West
                sx -= 1;
            
            elif sx<len(pop_maze)-1 and pop_maze[sy][sx+1] == step-1: # cell East
                sx += 1;

            path.append((sy, sx));
            step -= 1;

        return path;

    
