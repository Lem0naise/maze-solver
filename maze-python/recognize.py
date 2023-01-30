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

DEV_SENSITIVITY = 60;
# predefined green
G_B = 120
G_G = 210
G_R = 160

# read first frame to get dimensions
ret, frame = cap.read()
height, width = frame.shape[:2]


while(True):
    
    # read current frame
    ret, frame = cap.read()
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV); #changing BGR into HSV colour
    light_green = (146, 191, 96);
    dark_green = (26, 53, 16);

    # creating a 1,0 mask with any colours that resemble green
    mask = cv2.inRange(frame, dark_green, light_green);
    
    frame = cv2.bitwise_and(frame, frame, mask=mask); # only enable green pixels

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
    
    # iterate through pixels
    #for y in range(0, height):
    #    for x in range(0, width):

    #        h[y, x] = 0;
    #        #s[y, x] = 0;
    #        v[y, x] = 0;

    
    # merge colours back down into frame
    #frame = cv2.merge([h, s, v])


    lower_thres = 50
    higher_thres = 150

    # finding edges
    #edge = cv2.Canny(s, lower_thres, higher_thres)
    #contours, hier = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)

    # displays frame
    cv2.imshow("frame", frame)
    
    # when q clicked, kill program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('i'):
        DEV_SENSITIVITY += 10
        print(DEV_SENSITIVITY)

    if cv2.waitKey(1) & 0xFF == ord('k'):
        DEV_SENSITIVITY -= 10
        print(DEV_SENSITIVITY)
  
# After the loop release the cap(ture) object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()