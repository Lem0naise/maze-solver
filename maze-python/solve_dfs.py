from copy import deepcopy, copy
import cv2
import time
import numpy
import bfs


class MazeSolver_dfs:
    def __init__(self, maze, recogniser, dfs_opts, bfs_opts):

        self.start_time = time.time() # getting current time (used for calculating pathfinding time)

        self.height = len(maze)
        self.width = len(maze[0])

        self.recogniser = recogniser

        # display option vars

        self.show_dfs = dfs_opts['show_dfs']
        self.show_dfs_delay = dfs_opts['show_dfs_delay']
        self.dfs_line_colour = dfs_opts['dfs_line_colour']
        self.dfs_thickness = dfs_opts['dfs_thickness']
        self.hide_dfs_on_bfs_show = dfs_opts['hide_dfs_on_bfs_show']
        self.show_dfs_debug = dfs_opts['show_dfs_debug']

        self.show_bfs_cleanup = bfs_opts['show_bfs_cleanup']
        self.show_bfs_delay = bfs_opts['show_bfs_delay']
        self.bfs_line_colour = bfs_opts['bfs_line_colour']
        self.bfs_thickness = bfs_opts['bfs_thickness']
        self.show_bfs_debug = bfs_opts['show_bfs_debug'] # TODO

        n_maze = deepcopy(maze);
        
        # getting start & end coords
        self.start, self.end = None, None;
        for i in range(len(n_maze)):
            for j in range(len(n_maze[i])):

                if n_maze[i][j] == 255: # 255 -> 1
                    n_maze[i][j] = 1

                if n_maze[i][j] == 2: # if it is start
                    self.start = (i, j)
                    n_maze[i][j] = 1; 

                if n_maze[i][j] == 3: # if it is end
                    self.end = (i, j);
                    n_maze[i][j] = 1;

                if self.start and self.end:
                    break;
        
        maze_graph = self._list_to_graph(n_maze)

        print("Starting DFS...")
        path = self._traverse(maze_graph)
        print(f"DFS complete. Took {(time.time() - self.start_time)} seconds.")
        
        #print(path)
        if path != False:
            self._draw(path)
        else:
            print('Maze not possible.')
            input()

    def _list_to_graph(self, maze):
        graph = {}
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                edges = []
                
                # TODO add corner (i.e. North East, etc) checking (maybe not)

                if i+1 < len(maze) and maze[i+1][j] == 1: # North
                    edges.append(f'({i+1}, {j})')

                if j+1 < len(maze[i]) and maze[i][j+1] == 1: # East
                    edges.append(f'({i}, {j+1})')

                if i > 0 and maze[i-1][j] == 1: # South
                    edges.append(f'({i-1}, {j})')

                if j > 0 and maze[i][j-1] == 1: # West
                    edges.append(f'({i}, {j-1})')

                graph[f'({i}, {j})'] = edges # cant use tuple as dict key

        return graph

    def _str_to_tuple(self, str):
        return tuple([x.replace('(', '').replace(')', '').strip() for x in str.split(',')])

    def _traverse(self, maze_graph):

        node = f'({self.start[0]}, {self.start[1]})' # start at the start

        self.path_stack = [] # the 'stack' for the path
        visited = {} # ' hash table' for whether coord has been visited

        for i in list(maze_graph.keys()): # sets all visited values to false for each coord
            visited[i] = False

        end_str = f'({self.end[0]}, {self.end[1]})'

        while node != end_str: # while not at end

            if visited[node] == False:
                self.path_stack.append(node)
                visited[node] = True

                if self.show_dfs_debug:
                    node_t = self._str_to_tuple(node)
                    self.recogniser.colour_frame[int(node_t[0])][int(node_t[1])] = (0, 0, 255)

            filteredlist = [x for x in maze_graph[node] if visited[x] == False] # removing visited coords from adjacency list

            if len(filteredlist) != 0: # if pixel is white
                for i in range(len(maze_graph[node])): 
                    if visited[maze_graph[node][i]] == False:
                        node = maze_graph[node][i] # set node to first non-visited coord in adjacency list
                        break
                
            else: # go back to previous node
                if self.show_dfs_debug:
                    node_t = self._str_to_tuple(node)
                    self.recogniser.colour_frame[int(node_t[0])][int(node_t[1])] = (255, 255, 255)

                if len(self.path_stack) > 1:
                    self.path_stack.pop(-1) 
                    node = self.path_stack[-1]
                else:
                    self.path_stack = False
                    break


            if self.show_dfs_debug:
                cv2.imshow("frame", self.recogniser.colour_frame)
                cv2.waitKey(1)

        return self.path_stack
                
        
    def _draw(self, path): # TODO make more beautiful

        if self.hide_dfs_on_bfs_show:
            clean_frame = deepcopy(self.recogniser.colour_frame)

        if self.show_dfs:
            for node in path:

                y, x = [int(x) for x in self._str_to_tuple(node)]

                for offset_y in range((1-self.dfs_thickness//2)-1, (self.dfs_thickness//2)+1):
                    for offset_x in range((1-self.dfs_thickness//2)-1, (self.dfs_thickness//2)+1):

                        # if the cell is a wall in the binary frame 
                        sum = self.recogniser.frame[y+offset_y, x+offset_x]
                        if sum != 0: # if its not a wall in the binary frame
                            self.recogniser.colour_frame[y+offset_y][x+offset_x] = self.dfs_line_colour # setting the pixel the line colour

                if self.show_dfs_delay != 0:
                    cv2.imshow("frame", self.recogniser.colour_frame)
                    cv2.waitKey(self.show_dfs_delay)
                
            cv2.imshow("frame", self.recogniser.colour_frame)
            cv2.waitKey(1)
            

        if self.show_bfs_cleanup:
            print("Starting BFS...")
            self.start_time = time.time() 
            path = bfs.path_to_bfs(path, self.height, self.width) # run bfs on the path
            print(f"BFS complete. Took {(time.time() - self.start_time)} seconds.")

            if self.hide_dfs_on_bfs_show:
                self.recogniser.colour_frame = deepcopy(clean_frame)

            for node in path: # for the path
                
                y, x = node

                # line displaying (thickness etc)

                for offset_y in range((1-self.bfs_thickness//2)-1, (self.bfs_thickness//2)+1):
                    for offset_x in range((1-self.bfs_thickness//2)-1, (self.bfs_thickness//2)+1):

                        # if the cell is a wall in the binary frame 
                        sum = self.recogniser.frame[y+offset_y, x+offset_x]
                        if sum != 0: # if its not a wall in the binary frame
                            self.recogniser.colour_frame[y+offset_y][x+offset_x] = self.bfs_line_colour # setting the pixel the line colour

                if self.show_bfs_delay != 0:
                    cv2.imshow("frame", self.recogniser.colour_frame)
                    cv2.waitKey(self.show_bfs_delay)
            
            cv2.imshow("frame", self.recogniser.colour_frame)
            cv2.waitKey(1)

        print("Finished. Press enter to end program.")
        cv2.waitKey(0)
    