#tinker cad
# Importing needed libraries
from playsound import playsound
from gtts import gTTS
import numpy as np
import cv2
import time
import os
import imutils
import subprocess
import pyglet
import random


def name_generator():
    ran = random.randint(1,5000)
    ran = str(ran)
    return ran


def TalkBack(case_ans):
    print("in ...................................")
    tts = gTTS(text=case_ans + "is detected",lang="en")
    new_name = name_generator()
    new_name= r"C:\\Users\dell\\OneDrive\Desktop\\RUPESH PABBA\\YOLO-3-OpenCV\\yolov3(part1)\\audio\\"+new_name+".mp3"
    tts.save(new_name)
    try:  
        print("saving...............................")
        playsound(new_name)
        print("saying................................")
        
        #os.remove(new_name) 
    except:
        print("i cant")


camera = cv2.VideoCapture(0)

h, w = None, None


with open(r'C:\Users\dell\OneDrive\Desktop\RUPESH PABBA\YOLO-3-OpenCV\yolo-coco-data/coco.names') as f:
    print(type(f))
    labels = [line.strip() for line in f]


network = cv2.dnn.readNetFromDarknet(r'C:\Users\dell\OneDrive\Desktop\RUPESH PABBA\YOLO-3-OpenCV\yolo-coco-data\yolov3.cfg',
                                     r'C:\Users\dell\OneDrive\Desktop\RUPESH PABBA\YOLO-3-OpenCV\yolo-coco-data\yolov3.weights')

layers_names_all = network.getLayerNames()

layers_names_output = \
    [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]


probability_minimum = 0.5

threshold = 0.3

colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

# # Check point
# print()
# print(type(colours))  # <class 'numpy.ndarray'>
# print(colours.shape)  # (80, 3)
# print(colours[0])  # [172  10 127]

"""
End of:
Loading YOLO v3 network
"""


"""
Start of:
Reading frames in the loop
"""

# Defining loop for catching frames
while True:
    # Capturing frame-by-frame from camera
    _, frame = camera.read()

    # Getting spatial dimensions of the frame
    # we do it only once from the very beginning
    # all other frames have the same dimension
    if w is None or h is None:
        # Slicing from tuple only first two elements
        h, w = frame.shape[:2]

    """
    Start of:
    Getting blob from current frame
    """

    # Getting blob from current frame
    # The 'cv2.dnn.blobFromImage' function returns 4-dimensional blob from current
    # frame after mean subtraction, normalizing, and RB channels swapping
    # Resulted shape has number of frames, number of channels, width and height
    # E.G.:
    # blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size, mean, swapRB=True)
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)

    """
    End of:
    Getting blob from current frame
    """

    """
    Start of:
    Implementing Forward pass
    """

    # Implementing forward pass with our blob and only through output layers
    # Calculating at the same time, needed time for forward pass
    network.setInput(blob)  # setting blob as input to the network
    start = time.time()
    output_from_network = network.forward(layers_names_output)
    end = time.time()

    # Showing spent time for single current frame
    print('Current frame took {:.5f} seconds'.format(end - start))

    """
    End of:
    Implementing Forward pass
    """

    """
    Start of:
    Getting bounding boxes
    """

    # Preparing lists for detected bounding boxes,
    # obtained confidences and class's number
    bounding_boxes = []
    confidences = []
    class_numbers = []

    # Going through all output layers after feed forward pass
    for result in output_from_network:
        # Going through all detections from current output layer
        for detected_objects in result:
            # Getting 80 classes' probabilities for current detected object
            scores = detected_objects[5:]
            # Getting index of the class with the maximum value of probability
            class_current = np.argmax(scores)
            # Getting value of probability for defined class
            confidence_current = scores[class_current]

            # # Check point
            # # Every 'detected_objects' numpy array has first 4 numbers with
            # # bounding box coordinates and rest 80 with probabilities
            # # for every class
            # print(detected_objects.shape)  # (85,)

            # Eliminating weak predictions with minimum probability
            if confidence_current > probability_minimum:

                box_current = detected_objects[0:4] * np.array([w, h, w, h])

                x_center, y_center, box_width, box_height = box_current
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes.append([x_min, y_min,
                                       int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                class_numbers.append(class_current)

    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences,
                               probability_minimum, threshold)

    texts = []
    if len(results) > 0:
        for i in results.flatten():

            x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
            box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

            colour_box_current = colours[class_numbers[i]].tolist()

            cv2.rectangle(frame, (x_min, y_min),
                          (x_min + box_width, y_min + box_height),
                          colour_box_current, 2)

            text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])],
                                                   confidences[i])

            cv2.putText(frame, text_box_current, (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)

            texts.append(labels[class_numbers[i]])

            print(texts)
            x = texts
            #print(len(x)!=0)
        #try:
            #for x in x:
            # if x:
            #     description = ','.join(x)
            #     tts = gTTS(text=x, lang='en')
            #     filename = "tts.mp3"
            #     tts.save(filename)
            #     audio = pyglet.media.load(filename, streaming=False)
            #     pyglet.options['audio'] = (
            #     'openal', 'pulse', 'directsound', 'silent')
            #     audio.play()
            #     time.sleep(audio.duration)

        #except:
        #    print("not wroking")
        for i in x:
            TalkBack(i)
        

    

    
    cv2.namedWindow('YOLO v3 Real Time Detections', cv2.WINDOW_NORMAL)
    cv2.imshow('YOLO v3 Real Time Detections', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    


camera.release()
cv2.destroyAllWindows()
os.remove('tts.mp3')
