import logging
import grpc
import time
from concurrent import futures
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import generated gRPC code
from proto import face_pb2, face_pb2_grpc

# Import face recognition functions
from src import register_face, identify_face, delete_face

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FaceRecognitionServicer(face_pb2_grpc.FaceRecognitionServicer):
    """Implementation of FaceRecognition service."""
    
    def RegisterFace(self, request, context):
        """
        Register a face with student ID.
        
        Args:
            request: RegisterRequest containing student_id and image_base64
            context: gRPC context
            
        Returns:
            RegisterResponse
        """
        logger.info(f"Received register request for student {request.student_id}")
        
        try:
            success, message = register_face(request.student_id, request.image_base64)
            
            return face_pb2.RegisterResponse(
                success=success,
                message=message
            )
        except Exception as e:
            logger.error(f"Error in RegisterFace: {e}")
            return face_pb2.RegisterResponse(
                success=False,
                message=f"Server error: {str(e)}"
            )
    
    def IdentifyFace(self, request, context):
        """
        Identify a face and return student ID.
        
        Args:
            request: IdentifyRequest containing image_base64
            context: gRPC context
            
        Returns:
            IdentifyResponse
        """
        logger.info("Received identify face request")
        
        try:
            student_id, confidence, success, message = identify_face(request.image_base64)
            
            if success:
                logger.info(f"Successfully identified face - Student ID: {student_id}, Confidence: {confidence:.2f}")
            else:
                logger.warning(f"Failed to identify face - Message: {message}")
            
            return face_pb2.IdentifyResponse(
                student_id=student_id,
                confidence=float(confidence),
                success=success,
                message=message
            )
        except Exception as e:
            logger.error(f"Error in IdentifyFace: {e}")
            return face_pb2.IdentifyResponse(
                student_id="unknown",
                confidence=0.0,
                success=False,
                message=f"Server error: {str(e)}"
            )

    def DeleteFace(self, request, context):
        """
        Delete face embedding by student ID.
        
        Args:
            request: DeleteFaceRequest containing student_id
            context: gRPC context
            
        Returns:
            DeleteFaceResponse
        """
        logger.info(f"Received delete request for student {request.student_id}")
        
        try:
            success, message = delete_face(request.student_id)
            
            return face_pb2.DeleteFaceResponse(
                success=success,
                message=message
            )
        except Exception as e:
            logger.error(f"Error in DeleteFace: {e}")
            return face_pb2.DeleteFaceResponse(
                success=False,
                message=f"Server error: {str(e)}"
            )

def serve():
    """Start gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    face_pb2_grpc.add_FaceRecognitionServicer_to_server(
        FaceRecognitionServicer(), server
    )
    
    # Get port from environment variable or use default
    port = os.environ.get('GRPC_PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    
    server.start()
    logger.info(f"Server started on port {port}")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)
        logger.info("Server stopped")

if __name__ == '__main__':
    serve()
