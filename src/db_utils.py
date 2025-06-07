import os
import logging
from pymongo import MongoClient
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FaceDatabase:
    def __init__(self):
        """Initialize MongoDB connection."""
        try:
            # Get MongoDB connection string from environment variable or use default
            mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://trungnhanforwork:Nhan280803%40@cluster0.qalmkcs.mongodb.net/cmt?retryWrites=true&w=majority&appName=Cluster0&tls=true')
            print(mongo_uri)
            self.client = MongoClient(mongo_uri)
            self.db = self.client['cmt']
            self.collection = self.db['face_embeddings']
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def save_embedding(self, student_id, embedding):
        """
        Save face embedding to database.
        
        Args:
            student_id (str): Student ID
            embedding (list): Face embedding vector
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if student already exists
            existing = self.collection.find_one({"student_id": student_id})
            
            if existing:
                # Update existing record
                result = self.collection.update_one(
                    {"student_id": student_id},
                    {"$set": {"embedding": embedding.tolist()}}
                )
                logger.info(f"Updated embedding for student {student_id}")
            else:
                # Insert new record
                result = self.collection.insert_one({
                    "student_id": student_id,
                    "embedding": embedding.tolist()
                })
                logger.info(f"Inserted new embedding for student {student_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error saving embedding: {e}")
            return False

    def get_all_embeddings(self):
        """
        Get all embeddings from database.
        
        Returns:
            dict: Dictionary mapping student_id to embedding
        """
        try:
            embeddings = {}
            for doc in self.collection.find():
                embeddings[doc["student_id"]] = np.array(doc["embedding"])
            
            logger.info(f"Retrieved {len(embeddings)} embeddings from database")
            return embeddings
        except Exception as e:
            logger.error(f"Error retrieving embeddings: {e}")
            return {}

    def delete_embedding(self, student_id):
        """
        Delete face embedding from database.
        
        Args:
            student_id (str): Student ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.collection.delete_one({"student_id": student_id})
            if result.deleted_count > 0:
                logger.info(f"Deleted embedding for student {student_id}")
                return True
            else:
                logger.warning(f"No embedding found for student {student_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting embedding: {e}")
            return False

    def close(self):
        """Close MongoDB connection."""
        try:
            self.client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
