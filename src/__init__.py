# This file makes the src directory a Python package
# It allows imports like: from src import register_face, identify_face

# Import main functions to make them available at the package level
from .register_face import register_face
from .identify_face import identify_face
from .delete_face import delete_face
from .db_utils import FaceDatabase

__all__ = ['register_face', 'identify_face', 'delete_face', 'FaceDatabase']