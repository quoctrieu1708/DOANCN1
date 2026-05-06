import face_recognition
import numpy as np

class FaceModel:
    @staticmethod
    def get_encodings(image_np: np.ndarray):
        """
        Takes a numpy array image and returns face locations and encodings.
        """
        face_locations = face_recognition.face_locations(image_np)
        if not face_locations:
            return [], []
        
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        return face_locations, face_encodings

    @staticmethod
    def compare_faces(known_encodings, face_encoding_to_check, tolerance=0.6):
        """
        Compare known encodings to a face encoding and return the best match index and distance.
        """
        if not known_encodings:
            return None, None
            
        face_distances = face_recognition.face_distance(known_encodings, face_encoding_to_check)
        if len(face_distances) == 0:
            return None, None
            
        best_match_index = np.argmin(face_distances)
        
        if face_distances[best_match_index] <= tolerance:
            return best_match_index, face_distances[best_match_index]
            
        return None, None
