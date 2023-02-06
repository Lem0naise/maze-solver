from solve import MazeSolver;
from recognize import Recogniser;
from time import sleep;
import json
import webbrowser

# Runtime Parameters (N.B. Makes significantly slower)
show_debug = False
show_loading = False

# Solution Display Options (Does not affect speed as much)
line_thickness = 4
line_colour = (222, 98, 91)
entity = True # idk what to call this
delay = 50 # ms, time between path frames, when entity = False set to 1, when entity = True set to 50 or otherwise


recogniser = Recogniser();
print('finished with recogniser')
frame = recogniser.frame;
while frame.any() == None:
    frame = recogniser.frame;
maze = frame;

height = len(maze)
width = len(maze[0])

solver = MazeSolver(maze, recogniser, show_debug, show_loading, line_thickness, line_colour, entity, delay);


# sending maze & path to server
def write_json():
    height, width = len(maze), len(maze[0]);
    write_dic = {
        "path": solver.path,
        "hw": [height, width],
        "maze":maze,
    }
    # open link in web browser
    pw = "password"
    webbrowser.open('http://localhost:3000?password=' + pw + '&maze='+ json.dumps(write_dic))

#write_json();