import cv2
import pytesseract
import playsound
from collections import Counter
import random
from playsound import playsound
from gtts import gTTS
import os

def name_generator():
    ran = random.randint(1,5000)
    ran = str(ran)
    return ran

def speak(detect):
    tts = gTTS(detect,lang="en")
    new_name = name_generator()
    new_name=  new_name+".mp3"
    tts.save(new_name)
    playsound(new_name)
    os.remove(new_name) 


# Set the path to the Tesseract OCR executable (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Initialize the camera
camera = cv2.VideoCapture(0)

# Open the text file in append mode
output_file = open('extracted_text.txt', 'a')

# Keep capturing frames from the camera
while True:
    # Read a frame from the camera
    _, frame = camera.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply image preprocessing
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    adaptive = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Perform text detection using contours
    contours, _ = cv2.findContours(adaptive, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour based on area
    #largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box coordinates
    x, y, w, h = cv2.boundingRect(contours)

    # Extract the region of interest (ROI)
    roi = adaptive[y:y+h, x:x+w]

    # Perform text extraction using pytesseract
    extracted_text = pytesseract.image_to_string(roi)

    # Append the extracted text to the output file
    output_file.write(extracted_text + '\n')

    # Display the extracted text
    print(extracted_text)

    # Display the original frame with the largest bounding box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('Text Extraction', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera, close windows, and close the output file
camera.release()
cv2.destroyAllWindows()
output_file.close()

# Read the extracted text file
with open('extracted_text.txt', 'r') as file:
    text_data = file.read().replace('\n', ' ')

# Split the text into individual words
words = text_data.split()

# Get the most frequent word using Counter
word_counter = Counter(words)
most_frequent_word = word_counter.most_common(1)[0][0]

# Play a sound for the most frequent word
speak(most_frequent_word)
