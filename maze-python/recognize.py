import cv2
import time

HEIGHT = 200
WIDTH = 200
# NB
# opencv2 uses BGR colours, not RGB
# coordinates are in (y, x) format not (x, y)

# this is how you draw markers on the frame
#cv2.drawMarker(frame, (width//2, height//2), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=3, markerSize=50)

class Recogniser:


    def start_end(self, event,x,y,flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN and self.waiting: # if waiting for start and end

            if self.start == []: # if start is not yet defined, set start

                self.start = [y, x]                

                print("Start colour:", end="")
                print(self.frame[self.start[0]][self.start[1]])

                self.frame[self.start[0]][self.start[1]] = 2 # set start

            elif self.end == []: # set end if start done and end not done

                self.end = [y, x]

                print("End colour:", end="")
                print(self.frame[self.end[0]][self.end[1]])
                
                self.frame[self.end[0]][self.end[1]] = 3 # set end



    def __init__(self):

        self.waiting = False


        self.start = []
        self.end = []

        cap = cv2.VideoCapture(0)

        cv2.namedWindow("frame")

        cv2.setMouseCallback("frame", self.start_end)

        cap.set(3, 16) # setting width 
        cap.set(4, 9) # and height

        # read first frame to get dimensions
        ret, self.frame = cap.read()
        first_frame = self.frame
    
        while(True):
            # read current self.frame
            ret, self.frame = cap.read()
            self.frame = cv2.resize(self.frame, (HEIGHT, WIDTH))
            self.colour_frame = self.frame

            # white thresholds
            white = (255, 255, 255);
            dark_white = (160, 160, 160);

            # creating a 1 to 0 mask with any colours that resemble green
            mask = cv2.inRange(self.frame, dark_white, white);
            self.frame = cv2.bitwise_and(self.frame, self.frame, mask=mask); # only enable green pixels
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY); # image to greyscale


            # thresholding greyscale into b&w
            lower_thres = 160 # 70/255 minimum whiteity
            (thresh, self.frame) = cv2.threshold(self.frame, lower_thres, 255, cv2.THRESH_BINARY);

            # iterate through every pixel 
            """
            for y in range(0, height):
                for x in range(0, width):
                    pass
            """

            # displays self.frame
            cv2.imshow("frame", self.colour_frame)
            

            # click q to select start and end
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.waiting = True
                time.sleep(1)
                cv2.waitKey(0); # wait for q to be pressed again
                break


      
        cap.release()
        #cv2.destroyAllWindows()
        #cv2.namedWindow("bob")
        
       

        # After the loop release the cap(ture) object
        

        # Destroy all the windows
        #cv2.destroyAllWindows()

        return


