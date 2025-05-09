import base64
import logging
import numpy as np
import cv2
import face_recognition
from PIL import Image
import io
from .db_utils import FaceDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Export the register_face function
__all__ = ['register_face']

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

def register_face(student_id, image_base64):
    """
    Register a face with student ID.
    
    Args:
        student_id (str): Student ID
        image_base64 (str): Base64 encoded image
        
    Returns:
        tuple: (success, message)
    """
    db = None
    try:
        # Decode image
        image = decode_image(image_base64)
        
        # Extract embedding
        embedding = extract_embedding(image)
        
        # Save to database
        db = FaceDatabase()
        success = db.save_embedding(student_id, embedding)
        
        if success:
            return True, f"Successfully registered face for student {student_id}"
        else:
            return False, "Failed to save embedding to database"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        logger.error(f"Error in register_face: {e}")
        return False, f"Error registering face: {str(e)}"
    finally:
        if db:
            db.close()
