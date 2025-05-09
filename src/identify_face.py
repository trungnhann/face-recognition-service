import base64
import logging
import numpy as np
import cv2
import face_recognition
from PIL import Image
import io
from scipy.spatial.distance import euclidean
from .db_utils import FaceDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Threshold for face recognition
SIMILARITY_THRESHOLD = 0.6  # Adjust based on your requirements

def decode_image(base64_string):
    """
    Decode base64 string to image.
    
    Args:
        base64_string (str): Base64 encoded image
        
    Returns:
        numpy.ndarray: Decoded image
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64 string
        img_data = base64.b64decode(base64_string)
        
        # Convert to image
        img = Image.open(io.BytesIO(img_data))
        
        # Convert to numpy array (for OpenCV and face_recognition)
        return np.array(img)
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        raise

def extract_embedding(image):
    """
    Extract face embedding from image.
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        numpy.ndarray: Face embedding vector
    """
    try:
        # Convert to RGB if needed (face_recognition requires RGB)
        if image.shape[2] == 4:  # If RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif len(image.shape) == 2:  # If grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Detect face locations
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            logger.warning("No face detected in the image")
            raise ValueError("No face detected in the image")
        
        # Get face encodings (embeddings)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if not face_encodings:
            logger.warning("Could not extract face encoding")
            raise ValueError("Could not extract face encoding")
        
        # Return the first face encoding
        return np.array(face_encodings[0])
    except Exception as e:
        logger.error(f"Error extracting embedding: {e}")
        raise

def identify_face(image_base64):
    """
    Identify a face and return student ID.
    
    Args:
        image_base64 (str): Base64 encoded image
        
    Returns:
        tuple: (student_id, confidence, success, message)
    """
    db = None
    try:
        # Decode image
        image = decode_image(image_base64)
        
        # Extract embedding
        query_embedding = extract_embedding(image)
        
        # Get all embeddings from database
        db = FaceDatabase()
        all_embeddings = db.get_all_embeddings()
        
        if not all_embeddings:
            return "unknown", 0.0, False, "No registered faces in database"
        
        # Find the closest match
        min_distance = float('inf')
        best_match = "unknown"
        
        for student_id, embedding in all_embeddings.items():
            # face_recognition uses different distance metric, so we'll use euclidean here
            distance = euclidean(query_embedding, embedding)
            if distance < min_distance:
                min_distance = distance
                best_match = student_id
        
        # Convert distance to similarity score (0-1 range, higher is better)
        # For face_recognition, typical threshold is around 0.6
        similarity = 1.0 / (1.0 + min_distance)
        
        # Check if the match is good enough
        if similarity >= SIMILARITY_THRESHOLD:
            return best_match, similarity, True, "Face identified successfully"
        else:
            return "unknown", similarity, False, "No matching face found"
    except ValueError as ve:
        return "unknown", 0.0, False, str(ve)
    except Exception as e:
        logger.error(f"Error in identify_face: {e}")
        return "unknown", 0.0, False, f"Error identifying face: {str(e)}"
    finally:
        if db:
            db.close()

# Export the identify_face function
__all__ = ['identify_face']
