import numpy as np
from fastapi import UploadFile
import json
from core.config import get_db_connection
from models.face_model import FaceModel
from utils.utils import load_image_as_numpy

async def get_face_encoding(file: UploadFile):
    contents = await file.read()
    image_np = load_image_as_numpy(contents)
    
    face_locations, face_encodings = FaceModel.get_encodings(image_np)
    
    if len(face_locations) == 0:
        raise ValueError("No face found in the image")
    
    if len(face_locations) > 1:
        raise ValueError("Multiple faces found. Please upload an image with a single face.")
        
    return json.dumps(face_encodings[0].tolist())

async def recognize_face(file: UploadFile):
    contents = await file.read()
    try:
        image_np = load_image_as_numpy(contents)
        face_locations, face_encodings = FaceModel.get_encodings(image_np)
        
        if len(face_locations) == 0:
            return {"name": "unknown", "user_id": None}
            
        uploaded_encoding = face_encodings[0]
    except Exception as e:
        print(f"Error processing image: {e}")
        return {"name": "unknown", "user_id": None}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, face_encoding FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    if not users:
        return {"name": "unknown", "user_id": None}

    known_encodings = []
    user_data = []

    for user in users:
        if user['face_encoding']:
            try:
                encoding_list = json.loads(user['face_encoding'])
                known_encodings.append(np.array(encoding_list))
                user_data.append({"id": user['id'], "name": user['name']})
            except Exception as e:
                continue

    if not known_encodings:
        return {"name": "unknown", "user_id": None}

    best_match_index, distance = FaceModel.compare_faces(known_encodings, uploaded_encoding)

    if best_match_index is not None:
        best_user = user_data[best_match_index]
        return {
            "user_id": best_user['id'],
            "name": best_user['name']
        }
    
    return {"name": "unknown", "user_id": None}
