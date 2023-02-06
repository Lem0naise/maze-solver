# zac
from copy import deepcopy
import cv2
import time
import numpy
from PIL import Image
from random import randint

class MazeSolver:
    def __init__(self, maze, recogniser, show_debug, show_loading):

        self.start_time = time.time() # timing

        self.PREDICTED_PERCENTAGE_OF_MAZE_STEPPED = 0.6 # what percentage of the maze will be 'stepped through' (turn blue in debug mode) before end is found, used for loading bar

        self.recogniser = recogniser
        self.debug = show_debug
        self.loading = show_loading

        n_maze = deepcopy(maze);
        
        start, end = None, None;
        print("Finding start and end.")
        for i in range(len(n_maze)):
            for j in range(len(n_maze[i])):

                # set any 255 to 1
                if n_maze[i][j] == 255:
                    n_maze[i][j] = 1

                if n_maze[i][j] == 2: # if it is start
                    start = (i, j)
                    n_maze[i][j] = 0; # set start to 0
                if n_maze[i][j] == 3: # if it is end
                    end = (i, j);
                    n_maze[i][j] = 0; # set end to 0

                if start and end:
                    break;
        
        print("Found start and end.")

        print("Populating maze...")
        pop_maze = self._populate_maze(n_maze, start, end); # TODO Stuck here
        print("Populated maze.")

        print("Pathing through maze...");
        self.path = self._path_maze(pop_maze, end); # final path
        print("Pathed through maze.");

        self.path.reverse();
    
        self._draw(self.recogniser.colour_frame, self.path) # draw on the image


    def _draw(self, frame, path):

        delay = 2

        for i in range(len(path)):


            # three blocks around
            # TODO will index error
            
            distance = 12
    
            # if the cell is a wall in the binary frame 
            sum = 0
            for j in self.recogniser.frame[path[i][0], path[i][1]]:
                sum+=j
            
            if sum != 0: # if its not a wall in the binary frame
                frame[path[i][0], path[i][1]] = (255, 0, 0) # setting the path pixels to blue
    
            

            if i%delay == 0:
                cv2.imshow("frame", frame) # showing the frame
                cv2.waitKey(1) # required wait statement 

        cv2.waitKey(0)


    def _populate_maze(self, maze_in, start, end):

        self.stepped_pixels = 0
            
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
        
        ey, ex = end; # TODO doesn't even change anything if i switch x and y

        maze_in[ey][ex] = 0 # set the end to 0

        step = 1; # distance from start

        height = len(maze)
        width = len(maze[0])

        # TODO SOMETIMES GET STUCK IN THIS WHILE LOOP WHILE END IS BELOW START
        
        prev_prog = 0
        while maze[ey][ex] == 0: # while end not pathfound to (while still is an empty cell)

            self._move(maze, maze_in, step, height, width)
            step += 1; # increment distance
        
            # TODO debug print
            if step % 2000 == 0:
                print(step)

            # loading bar
            if step % 25 == 0 and self.loading:

                prog = self.stepped_pixels / ((abs(ey - sy) * abs(ex - sx)) * self.PREDICTED_PERCENTAGE_OF_MAZE_STEPPED) 
                if prog >= 1: prog = 1

                for i in range(int(prev_prog*width), int(width * prog)):
                    for j in range(1, 4):
                        self.recogniser.frame[height-j, i] = (0,0,255)
                
                prev_prog = prog



            if step >= (height*width /2): # if have gone past the realm of possibility
                print("Maze not possible.")
                exit()

        
        print("Maze population took %s seconds." % (time.time() - self.start_time))

        return maze;


    def _move(self, maze, maze_input, step, height, width): # maze is the populating maze, and maze_input is the actual image
        
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

                    self.stepped_pixels +=1

                    # TODO SHOW WHILE POPULATING
                    if self.debug:
                        self.recogniser.frame[i, j] = (255, 0, 0) # setting the checked pixels to blue (mostly debug for now)

                    if (self.debug or self.loading) and j%10 == 0: # show every 10 frames 
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

    
