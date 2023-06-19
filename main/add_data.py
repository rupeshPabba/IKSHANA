import face_recognition
import mysql.connector
import numpy as np

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysql123',
    database='attendance'
)
cursor = cnx.cursor()
names_input=str(input("enter the names you want to feed with commas seperated:-karthik,rupesh"))

known_face_names = [
    "manushree", "meghana", "rupesh", "karthik", "sudheer_reddy", "mohd_afnan"
]
data = []

for i, name in enumerate(known_face_names, start=1):
    image = face_recognition.load_image_file("/home/rupesh_pabba/rupeshpabba/face_recognition/known_people/" + name + ".jpeg")
    encoding = face_recognition.face_encodings(image)[0]
    encoding_string = encoding.tostring()
    data.append((i, name, encoding))

insert_query = "INSERT INTO student_details (roll_no, name, face_encodings,status) VALUES (%s, %s, %s,NULL)"
cursor.executemany(insert_query, data)

# Commit the changes to the database
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
