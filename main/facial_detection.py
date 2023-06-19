import face_recognition
import cv2
import numpy as np
import mysql.connector

def insert_attendance(names):
    update_query = "UPDATE student_details SET status = 'present' WHERE name=%s"
    if names=="Unknown":
        pass
    else:
        try:
            cursor.execute(update_query, (names,))
            connection.commit()
            print("Attendance updated successfully.")
        except Exception as e:
            print("Error occurred:", str(e))

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="attendance"
)

cursor = connection.cursor()
cursor.execute("use attendance")
cursor.execute("select face_encodings from student_details")
rows =cursor.fetchall()
ec = []
for row in rows:
    encoding_string = row[0]
    encoding = np.fromstring(encoding_string, dtype=np.float64)
    ec.append(encoding.tolist())

video_capture = cv2.VideoCapture(0)

# Creating arrays of known face encodings and their names
known_face_encodings = [
    ec[0],ec[1],ec[2],ec[3],ec[4],ec[5]
]
known_face_names = [
    "manushree","meghana","rupesh","karthik","sudheer","mohd afnan"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        print(face_names)

        for i in face_names:
            insert_attendance(i)


        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255,0,0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cursor.close()
connection.close()    

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
                
            
                