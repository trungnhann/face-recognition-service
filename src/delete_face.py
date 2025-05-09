import logging
from .db_utils import FaceDatabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Export the delete_face function
__all__ = ['delete_face']

def delete_face(student_id):
    """
    Delete face embedding by student ID.
    
    Args:
        student_id (str): Student ID
        
    Returns:
        tuple: (success, message)
    """
    db = None
    try:
        # Delete from database
        db = FaceDatabase()
        success = db.delete_embedding(student_id)
        
        if success:
            return True, f"Successfully deleted face for student {student_id}"
        else:
            return False, f"Failed to delete face for student {student_id}"
    except Exception as e:
        logger.error(f"Error in delete_face: {e}")
        return False, f"Error deleting face: {str(e)}"
    finally:
        if db:
            db.close() 