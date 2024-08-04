# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import numpy as np
# from opencv_utils import load_image, detect_faces, extract_face_features, compare_faces, save_known_faces, load_known_faces, add_face
# import logging

# app = Flask(__name__)
# CORS(app)

# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# KNOWN_FACES_FILE = 'known_faces.pkl'

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Load known faces and names
# known_face_features, known_face_names = load_known_faces(KNOWN_FACES_FILE)

# # Ensure they are initialized if load_known_faces failed
# if known_face_features is None:
#     known_face_features = []
# if known_face_names is None:
#     known_face_names = []

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)

#     image = load_image(filepath)
#     faces = detect_faces(image)

#     logging.debug(f'Faces detected: {faces}')

#     if len(faces) == 0:
#         return jsonify({'message': 'No faces found'}), 400

#     face_features = extract_face_features(image, faces)

#     global known_face_features, known_face_names
#     known_face_features, known_face_names = add_face(known_face_features, known_face_names, face_features[0], filename)

#     save_known_faces(KNOWN_FACES_FILE, known_face_features, known_face_names)

#     return jsonify({'message': 'Face uploaded and encoded'}), 201

# @app.route('/recognize', methods=['POST'])
# def recognize_face():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)

#     image = load_image(filepath)
#     faces = detect_faces(image)

#     logging.debug(f'Faces detected: {faces}')

#     if len(faces) == 0:
#         return jsonify({'message': 'No faces found'}), 400

#     face_features = extract_face_features(image, faces)
#     logging.debug(f'Extracted features: {face_features}')

#     match, index = compare_faces(known_face_features, face_features[0])
#     logging.debug(f'Match found: {match}, Index: {index}')

#     if match:
#         return jsonify({'message': 'Face recognized', 'name': known_face_names[index]}), 200

#     return jsonify({'message': 'Face not recognized'}), 404

# if __name__ == '__main__':
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     app.run(debug=True)


import face_recognition
import cv2
import numpy as np

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
image1 = face_recognition.load_image_file("path")  # enter image 'path'
face_encoding1 = face_recognition.face_encodings(image1)[0]

# Load a second sample picture and learn how to recognize it.
image2 = face_recognition.load_image_file("path")  # enter image 'path'
face_encoding2 = face_recognition.face_encodings(image2)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    face_encoding1,
    face_encoding2
]

known_face_names = [
    "",  # enter face name
    ""   # enter face name
]

# Initialize some variables
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
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
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

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
