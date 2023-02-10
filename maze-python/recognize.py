import cv2

# NB
# opencv2 uses BGR colours, not RGB
# coordinates are in (y, x) format not (x, y)

# this is how you draw markers on the frame
# cv2.drawMarker(frame, (width//2, height//2), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=3, markerSize=50)

# this is how you set the rgb value of a pixel in the frame
# frame[y, x] = (b,g,r)

class Recogniser:

    def start_end(self, event,x,y,flags,param): # function to set start & end coords based on clicks on frame
        
        if event == cv2.EVENT_LBUTTONDOWN and self.waiting: # if button pressed & waiting for start and end

            if self.start == []: # if start is not yet defined, set start
                
                if self.frame[y][x] == 255:
                    self.start = [y, x]                

                    print(f"Set start: ({y},{x}) {self.frame[self.start[0]][self.start[1]]}")
                    cv2.drawMarker(self.colour_frame, (x, y), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=1, markerSize=3)
                    cv2.imshow("frame", self.colour_frame)

                    self.frame[self.start[0]][self.start[1]] = 2 # set start
                
                else:
                    print("Start selection failed. Please select a white pixel.")

            elif self.end == []: # set end if start defined and end not yet defined

                if self.frame[y][x] == 255:
                    self.end = [y, x]

                    print(f"Set end: ({y},{x}) {self.frame[self.end[0]][self.end[1]]}")
                    cv2.drawMarker(self.colour_frame, (x, y), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=1, markerSize=3)
                    cv2.imshow("frame", self.colour_frame)
                    
                    self.frame[self.end[0]][self.end[1]] = 3 # set end

                    print("Press any key to start maze traversal.")

                else:
                    print("End selection failed. Please select a white pixel.")

    def __init__(self, resolution, CAMERA):

        self.width, self.height = resolution
        self.waiting = False

        self.start = []
        self.end = []

        cap = cv2.VideoCapture(CAMERA) # capture object

        cv2.namedWindow("frame")

        cv2.setMouseCallback("frame", self.start_end) # click listener

        cap.set(3, 16) # setting width 
        cap.set(4, 9) # and height

        print("Click 'Q' to freeze.")
        while(True):
            # read current self.frame
            ret, self.frame = cap.read()
            self.frame = cv2.resize(self.frame, (self.height, self.width))
            self.colour_frame = self.frame # save the coloured frame before doing anything else to it

            # white thresholds
            white = (255, 255, 255);
            dark_white = (100, 100, 100);

            # creating a 1 to 0 mask with any colours that resemble white
            mask = cv2.inRange(self.frame, dark_white, white);
            self.frame = cv2.bitwise_and(self.frame, self.frame, mask=mask); # only enable green pixels
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY); # image to greyscale

            # thresholding greyscale into b&w
            lower_thres = 150 # 70/255 minimum whiteity
            (thresh, self.frame) = cv2.threshold(self.frame, lower_thres, 255, cv2.THRESH_BINARY);

            # displays original coloured frame
            cv2.imshow("frame", self.colour_frame)
            
            # click q to select start and end
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Frozen!")
                self.waiting = True
                print("Select the start & end of the maze.")
                cv2.waitKey(0); # wait for any key to be pressed
                break
        

        # After the loop release the cap(ture) object
        cap.release() 
        return


