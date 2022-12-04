


import cv2


def do_nothing(x):
    pass




v = cv2.__version__.split('.')[0]

camera = cv2.VideoCapture(0)


while True:
    _, frame_BGR = camera.read()

    frame_HSV = cv2.cvtColor(frame_BGR, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('min_blue', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('min_green', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('min_red', 'Track Bars', 0, 255, do_nothing)

    cv2.createTrackbar('max_blue', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('max_green', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('max_red', 'Track Bars', 0, 255, do_nothing)

    min_blue = cv2.getTrackbarPos('min_blue', 'Track Bars')
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')

    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')


        
   
    mask = cv2.inRange(frame_HSV,
                       (min_blue, min_green, min_red),
                       (max_blue, max_green, max_red))

   
    min_green = cv2.getTrackbarPos('min_green', 'Track Bars')
    min_red = cv2.getTrackbarPos('min_red', 'Track Bars')

    max_blue = cv2.getTrackbarPos('max_blue', 'Track Bars')
    max_green = cv2.getTrackbarPos('max_green', 'Track Bars')
    max_red = cv2.getTrackbarPos('max_red', 'Track Bars')

    
    if v == '3':
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    
    else:
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])

        cv2.rectangle(frame_BGR, (x_min - 15, y_min - 15),
                      (x_min + box_width + 15, y_min + box_height + 15),
                      (255, 0, 0), 3)

        label = 'Detected Object'

        cv2.putText(frame_BGR, label, (x_min - 5, y_min - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    
    cv2.namedWindow('Detected Object', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected Object', frame_BGR)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()


