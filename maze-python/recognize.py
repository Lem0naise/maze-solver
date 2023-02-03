import cv2

# NB
# opencv2 uses BGR colours, not RGB
# coordinates are in (y, x) format not (x, y)

# this is how you draw markers on the frame
#cv2.drawMarker(frame, (width//2, height//2), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=3, markerSize=50)


cap = cv2.VideoCapture(0)

cap.set(3, 16)
cap.set(4, 9)

SENSITIVITY = 40000
PIXEL_SKIP = 3 # skip every third pixel

# read first frame to get dimensions
ret, frame = cap.read()
height, width = frame.shape[:2]


while(True):
    
    # read current frame
    ret, frame = cap.read()
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV); #changing BGR into HSV colour
    light_green = (146, 191, 96);
    dark_green = (26, 53, 16);

    # creating a 1 to 0 mask with any colours that resemble green
    mask = cv2.inRange(frame, dark_green, light_green);
    
    frame = cv2.bitwise_and(frame, frame, mask=mask); # only enable green pixels

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); # image to greyscale

    # thresholding greyscale into b&w
    lower_thres = 70 # 70/255 minimum greenity
    (thresh, frame) = cv2.threshold(frame, lower_thres, 255, cv2.THRESH_BINARY);
    

    # iterate through every pixel 
    for y in range(0, height):
        for x in range(0, width):
            pass

    # displays frame
    cv2.imshow("frame", frame)
    
    # when q clicked, kill program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  
# After the loop release the cap(ture) object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()