
# Importing needed library
import cv2
# Defining lower bounds and upper bounds of founded Mask
min_blue, min_green, min_red = 21, 222, 70
max_blue, max_green, max_red = 176, 255, 255
v = cv2.__version__.split('.')[0]
# Defining object for reading video from camera
camera = cv2.VideoCapture(0)
# Defining loop for catching frames
while True:
    # Capture frame-by-frame from camera
    _, frame_BGR = camera.read()

    # Converting current frame to HSV
    frame_HSV = cv2.cvtColor(frame_BGR, cv2.COLOR_BGR2HSV)

    # Implementing Mask with founded colours from Track Bars to HSV Image
    mask = cv2.inRange(frame_HSV,
                       (min_blue, min_green, min_red),
                       (max_blue, max_green, max_red))

    
    cv2.namedWindow('Binary frame with Mask', cv2.WINDOW_NORMAL)
    cv2.imshow('Binary frame with Mask', mask)

    

    # Checking if OpenCV version 3 is used
    if v == '3':
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    

    # Checking if OpenCV version 4 is used
    else:
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Finding the biggest Contour by sorting from biggest to smallest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Extracting Coordinates of the biggest Contour if any was found
    if contours:
        
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])

        # Drawing Bounding Box on the current BGR frame
        cv2.rectangle(frame_BGR, (x_min - 15, y_min - 15),
                      (x_min + box_width + 15, y_min + box_height + 15),
                      (0, 255, 0), 3)

        # Preparing text for the Label
        label = 'blue object'

        # Putting text with Label on the current BGR frame
        cv2.putText(frame_BGR, label, (x_min - 5, y_min - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    
    cv2.namedWindow('Detected Object', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected Object', frame_BGR)

    # Breaking the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Destroying all opened windows
cv2.destroyAllWindows()




