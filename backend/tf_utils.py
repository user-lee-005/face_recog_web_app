import cv2
import os
import pickle
import numpy as np

def load_image(filepath):
    return cv2.imread(filepath)

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def extract_face_features(image, faces):
    face_encodings = []
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (128, 128))  # Standardize to a fixed size
        flattened = resized.flatten()  # Flatten to a 1D array
        face_encodings.append(flattened)
    return face_encodings


def compare_faces(known_faces, face_to_check):
    for i, known_face in enumerate(known_faces):
        # Log dimensions for debugging
        print(f"Comparing face {i} with dimensions {known_face.shape} to input face with dimensions {face_to_check.shape}")
        try:
            result = np.linalg.norm(known_face - face_to_check)
        except ValueError as e:
            print(f"Error comparing faces: {e}")
            continue
        
        if result < 1000:  # threshold for similarity (adjust this as needed)
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
