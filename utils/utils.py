import io
from PIL import Image
import numpy as np

def load_image_as_numpy(contents: bytes) -> np.ndarray:
    """
    Converts raw image bytes to a numpy array for face_recognition
    """
    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        return np.array(image)
    except Exception as e:
        raise ValueError(f"Failed to process image: {e}")
