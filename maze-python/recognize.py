import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 16)
cap.set(4, 9)

number = 20000
while(True):
      
    ret, frame = cap.read()

    height, width = frame.shape[:2]

    # (b, g, r) for some reason, and not (r, g, b)
    # this gets the pixel rgb values at coords (72, 34)
    (b, g, r) = frame[34, 72] 

    # my first attempt at making all 'white' pixels red
    for y in range(0, height, 3):
        for x in range(0, width, 3):
            (b, g, r) = frame[y, x] # (b,g,r)
            
            if r+g > 0:
                if (float(r) + float(g) + float(b) > 140*3) and ((float(r**2 + g**2 + b**2)/3.0) - (float(r + g + b)/3.0)**2) < number:

                    for i in range(y-1, y+1):
                        for j in range(x-1, x+1):
                            frame[i, j] = (0, 0, 255)
            
    
    # this is how you draw markers on the frame
    #cv2.drawMarker(frame, (width//2, height//2), color=(0, 0, 255), markerType=cv2.MARKER_CROSS, thickness=3, markerSize=50)
    
    # displays frame
    cv2.imshow('frame', frame)
    
    # when q clicked, kill program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('i'):
        number += 100
        print(number)

    if cv2.waitKey(1) & 0xFF == ord('k'):
        number -= 100
        print(number)
  
# After the loop release the cap(ture) object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()