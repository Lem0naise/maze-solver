from solve import MazeSolver;
from recognize import Recogniser;
from time import sleep;
import json
import webbrowser
show_debug = True


recogniser = Recogniser();
print('finished with recogniser')
frame = recogniser.frame;
while frame.any() == None:
    frame = recogniser.frame;
maze = frame;

height = len(maze)
width = len(maze[0])

solver = MazeSolver(maze, recogniser, show_debug);


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