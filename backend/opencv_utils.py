import cv2
import os
import pickle
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

def load_image(filepath):
    return cv2.imread(filepath)

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

# def extract_face_features(image, faces):
#     face_encodings = []
#     for (x, y, w, h) in faces:
#         face = image[y:y+h, x:x+w]
#         gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
#         resized = cv2.resize(gray, (128, 128))  # Standardize to a fixed size
#         flattened = resized.flatten()  # Flatten to a 1D array
#         face_encodings.append(flattened)
#     return face_encodings

def extract_face_features(image, faces, size=(128, 128)):
    """Extract and encode face features from detected faces in an image."""
    face_encodings = []
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, size)  # Resize to a fixed size
        flattened = resized.flatten()  # Flatten to a 1D array
        # Normalize the feature vector
        normalized = flattened / np.linalg.norm(flattened)
        face_encodings.append(normalized)
    return face_encodings



# def compare_faces(known_faces, face_to_check, threshold=1000):
#     logging.debug("Inside Comparing faces")
#     face_to_check = np.array(face_to_check)
#     if face_to_check.ndim == 1:
#         face_to_check = face_to_check.reshape(1, -1)

#     for i, known_face in enumerate(known_faces):
#         known_face = np.array(known_face)
#         if known_face.ndim == 1:
#             known_face = known_face.reshape(1, -1)

#         # Ensure dimensions match
#         if known_face.shape[1] != face_to_check.shape[1]:
#             print(f"Dimension mismatch: known_face {known_face.shape[1]}, face_to_check {face_to_check.shape[1]}")
#             continue

#         try:
#             # Compute Euclidean distance
#             distances = np.linalg.norm(known_face - face_to_check, axis=1)
#             result = np.min(distances)
#         except ValueError as e:
#             print(f"Error comparing faces: {e}")
#             continue

#         if result < threshold:
#             return True, i
#     return False, -1

def compare_faces(known_faces, face_to_check, threshold=1000):
    """Compare a face against known faces and return if it matches."""
    face_to_check = np.array(face_to_check)
    if face_to_check.ndim == 1:
        face_to_check = face_to_check.reshape(1, -1)

    for i, known_face in enumerate(known_faces):
        known_face = np.array(known_face)
        if known_face.ndim == 1:
            known_face = known_face.reshape(1, -1)

        # Ensure dimensions match
        if known_face.shape[1] != face_to_check.shape[1]:
            print(f"Dimension mismatch: known_face {known_face.shape[1]}, face_to_check {face_to_check.shape[1]}")
            continue

        try:
            # Compute Euclidean distance
            distances = np.linalg.norm(known_face - face_to_check, axis=1)
            result = np.min(distances)
            print(f"Distance: {result}")
        except ValueError as e:
            print(f"Error comparing faces: {e}")
            continue

        if result < threshold:
            return True, i
    return False, -1


def save_known_faces(filename, known_faces, known_names):
    with open(filename, 'wb') as f:
        pickle.dump((known_faces, known_names), f)

def load_known_faces(filename):
    if not os.path.exists(filename):
        return [], []
    with open(filename, 'rb') as f:
        known_faces, known_names = pickle.load(f)
        return list(known_faces), list(known_names)  # Ensure they are lists

def add_face(known_faces, known_names, face, name):
    known_faces.append(face)
    known_names.append(name)
    return known_faces, known_names
