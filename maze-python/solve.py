# zac
from copy import deepcopy

class MazeSolver:
    def __init__(self, maze):
        n_maze = deepcopy(maze);
        
        start, end = None, None;
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

        print("Scanning maze...");
        pop_maze = self._populate_maze(n_maze, start, end);
        print("Pathing through maze...");
        self.path = self._path_maze(pop_maze, end); # final path
        self.path.reverse();



    def _populate_maze(self, maze_in, start, end):
            
        maze = []
        for i in range(len(maze_in)):

            maze.append([])
            for j in range(len(maze_in[i])):
                maze[-1].append(0)

    
        s1, s2 = start;
        maze[s1][s2] = 1; # set starting point as "1" minimum path length
        e1, e2 = end;

        step = 0;
        while maze[e1][e2] == 0: # while end not pathfound to
            step += 1;
            if step % 1000 == 0:
                print(step)
            self._move(maze, maze_in, step);

        print("Returned maze")
        return maze;


    def _move(self, maze, maze_input, step):
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                
                if maze[i][j] == step: # if cell is within reach

                    # {guard clause} and {if we have not reached the cell yet} and {there is no wall}
                    # then: set cell to NEXT STEP
                    if i>0 and maze[i-1][j] == 0 and maze_input[i-1][j] == 0: # cell North
                        maze[i-1][j] = step + 1;

                    if i<len(maze)-1 and maze[i+1][j] == 0 and maze_input[i+1][j] == 0: # cell South
                        maze[i+1][j] = step + 1;

                    if j>0 and maze[i][j-1] == 0 and maze_input[i][j-1] == 0: # cell West
                        maze[i][j-1] = step + 1;
                    
                    if j<len(maze)-1 and maze[i][j+1] == 0 and maze_input[i][j+1] == 0: # cell East
                        maze[i][j+1] = step + 1;



    def _path_maze(self, pop_maze, start):
        #nb start is not the start of the maze, but the start of the pathfinding
        #it is actually the end of the maze

        path = [];
        s1, s2 = start;
        step = pop_maze[s1][s2]; # set path limit

        while step > 2:

            if s1>0 and pop_maze[s1-1][s2] == step-1: # cell North
                s1 -= 1;

            elif s1<len(pop_maze)-1 and pop_maze[s1+1][s2] == step-1: # cell South
                s1 += 1;

            elif s2>0 and pop_maze[s1][s2-1] == step-1: # cell West
                s2 -= 1;
            
            elif s2<len(pop_maze)-1 and pop_maze[s1][s2+1] == step-1: # cell East
                s2 += 1;

            path.append((s1, s2));
            step -= 1;

        return path;

    
