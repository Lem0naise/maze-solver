from copy import deepcopy, copy
import cv2
import time
import numpy


class MazeSolver:
    def __init__(self, maze, recogniser, show_debug, show_loading, thickness, line, line_colour, entity, entity_colour, delay):

        self.start_time = time.time() # getting current time (used for calculating pathfinding time)

        self.recogniser = recogniser

        # display option vars
        self.debug = show_debug

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

        path = self._traverse(maze_graph)
        print("Traversing took % seconds." % (time.time() - self.start_time))
        
        #print(path)
        self._draw(path)

    def _list_to_graph(self, maze):
        graph = {}
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                edges = []
                
                # TODO add corner (i.e. North East, etc) checking

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

                if self.debug:
                    node_t = self._str_to_tuple(node)
                    self.recogniser.colour_frame[int(node_t[0])][int(node_t[1])] = (0, 0, 255)

            filteredlist = [x for x in maze_graph[node] if visited[x] == False] # removing visited coords from adjacency list

            if len(filteredlist) != 0: # if pixel is white
                for i in range(len(maze_graph[node])): 
                    if visited[maze_graph[node][i]] == False:
                        node = maze_graph[node][i] # set node to first non-visited coord in adjacency list
                        break
                
            else: # go back to previous node
                self.path_stack.pop(-1) 
                node = self.path_stack[-1]

                if self.debug:
                    node_t = self._str_to_tuple(node)
                    self.recogniser.colour_frame[int(node_t[0])][int(node_t[1])] = (255, 255, 255)

            if self.debug:
                cv2.imshow("frame", self.recogniser.colour_frame)
                cv2.waitKey(1)

        return self.path_stack
                
        
    def _draw(self, path): # TODO make more beautiful
        for node in path:
            node = self._str_to_tuple(node)
            self.recogniser.colour_frame[int(node[0])][int(node[1])] = (0, 0, 255)

            cv2.imshow("frame", self.recogniser.colour_frame)
            cv2.waitKey(1)

        input()