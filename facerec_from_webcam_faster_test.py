import face_recognition
import cv2
import numpy as np
from datetime import datetime
import time
import os

# Python code to remove duplicate elements 
def Remove(duplicate): 
	final_list = [] 
	for num in duplicate: 
		if num not in final_list: 
			final_list.append(num) 
	return final_list 

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)
cap = cv2.VideoCapture('Titanic_Scene_First_Class_Dinner.mp4')

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

ret, frame = cap.read()

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc('M','P','E','G')

output_video = cv2.VideoWriter('output.avi', fourcc, 25, (frame.shape[1],frame.shape[0]))

image_unknown = np.zeros((frame.shape[0],frame.shape[1],3),np.uint8)

global cnt 
global aux_
global old
global string_IN
global string_OUT
global flag_IN
global flag_OUT
cnt = 0
aux_ = 0
old = 0
string_IN = []
string_OUT = []
flag_IN = True
flag_OUT = False
frame_number = 0
cnt = 0
dict_ = {}

#file = open("out.txt","w")
#file = open("FACE_OUT.txt","w")

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV2/Rose.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV2/Jack.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

india_image = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV2/Ruth.jpg")
india_face_encoding = face_recognition.face_encodings(india_image)[0]

image_4 = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV2/Caledon.jpg")
face_encoding_4 = face_recognition.face_encodings(image_4)[0]

#print(type(face_encoding_4))
#print()

# Create arrays of known face encodings and their names
known_face_encodings = [
	obama_face_encoding,
	biden_face_encoding,
	india_face_encoding,
	face_encoding_4
]

known_face_names = [
	"Rose",
	"Jack",
	"Ruth",
	"Caledon"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

frame_IN = np.zeros((480,640,3),np.uint8)

while True:
    # Grab a single frame of video
	ret, frame = cap.read()
	#print(frame.shape)   
	frame_number += 1
	flag_detection = False
	time_detection_face_diogenes = 0

    # Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
	if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "Desconhecido"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]

			face_names.append(name)
            #cv2.putText(frame, "face_detected", (0,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

	process_this_frame = not process_this_frame

    # Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):

		flag_detection = True
		
		#print(top, right, bottom, left)
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		
		if name == "Desconhecido":
			cnt += 1
			aux_top = max(0, top - 50)
			aux_bottom = min(bottom + 50,frame.shape[0])
			aux_left = max(0, left - 50)
			aux_right = min(right + 50,frame.shape[1])
			
			image_unknown = frame[aux_top:aux_bottom,aux_left:aux_right]
			path1 = '/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_UNKNOWN'
			cv2.imwrite(os.path.join(path1,"ID_" + str(frame_number) + "-" + str(cnt) + ".jpg"), image_unknown)
			path2 = '/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV'
			cv2.imwrite(os.path.join(path2,"ID_"+str(frame_number)+"-"+ str(cnt) + ".jpg"), image_unknown)			
			
			aux = "ID_" + str(frame_number) + "-" + str(cnt) + "-_-"			
			dict_[aux] = face_recognition.load_image_file("/home/default/Desktop/face_recognition_PDI/examples/DATA_SET_MV/"+"ID_"+str(frame_number)+"-"+ str(cnt) + ".jpg")

			aux2 = "ID_" + str(frame_number) + "-" + str(cnt) + "^_^"
			#print(type(dict_[aux]))
			try:			
				dict_[aux2] = face_recognition.face_encodings(dict_[aux])[0]
				known_face_encodings.append(dict_[aux2])
				known_face_names.append("ID_" + str(frame_number) + "-" + str(cnt))

			except:
				print(str(frame_number) + "-" + str(cnt))			
	
            # Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        
            # Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                 
#        if right > 310 and left < 330:
#            flag_detection = False

		font = cv2.FONT_HERSHEY_DUPLEX

		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	
	if flag_detection == False:
		reference = 0
		aux = 0
    
	font = cv2.FONT_HERSHEY_SIMPLEX
    
	current_time = str(datetime.now())
    
#	cv2.putText(frame, current_time, (0,20), font, 0.5, (255, 0, 0), 1)
    
#	frame_IN[0:480,0:310] = frame[0:480,0:310]
#	frame_IN[0:480,330:640] = frame[0:480,330:640]
	#small_frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
    # Display the resulting image
	#cv2.imshow('Video', frame)
	print("Writing frame {} / {}".format(frame_number, length))
	if frame_number > 5630:
		break
	output_video.write(frame)

	#print(cap.get(cv2.CAP_PROP_FPS))

    # Hit 'q' on the keyboard to quit!
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break

# Release handle to the webcamfont = cv2.FONT_HERSHEY_SIMPLEX

string_IN = Remove(string_IN)
string_OUT = Remove(string_OUT)

outF = open("FACE_IN.txt", "w")
for line in string_IN:
  # write line to output file
	outF.write(line)
outF.close()

outF = open("FACE_OUT.txt", "w")
for line in string_OUT:
  # write line to output file
	outF.write(line)
outF.close()

num_lines = 0
with open("FACE_OUT.txt", 'r') as f:
	for line in f:
		num_lines += 1

file = open("FACE_NUMB.txt","w")
file.write("Diogenes - " + str(num_lines) + "\n")
file.close()

cap.release()
output_video.release()
cv2.destroyAllWindows()
