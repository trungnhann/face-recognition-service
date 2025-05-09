# Face Recognition System for Student Identification

This system provides face recognition capabilities for student identification using DeepFace, MongoDB, and gRPC.

## Features

- **RegisterFace**: Register a student's face by storing their face embedding in MongoDB
- **IdentifyFace**: Identify a student by comparing their face embedding with stored embeddings

## Directory Structure

\`\`\`
face_recognition_system/
├── proto/
│   └── face.proto
├── src/
│   ├── register_face.py
│   ├── identify_face.py
│   └── db_utils.py
├── server/
│   └── server.py
├── client/
│   └── client.py
├── requirements.txt
└── README.md
\`\`\`

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/face_recognition_system.git
   cd face_recognition_system
   \`\`\`

2. Create a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Install MongoDB:
   - Follow the instructions at https://docs.mongodb.com/manual/installation/
   - Start MongoDB service

5. Generate gRPC code:
   \`\`\`bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/face.proto
   \`\`\`

## Usage

### Start the server:

\`\`\`bash
python server/server.py
\`\`\`

### Register a face:

\`\`\`bash
python client/client.py register --student_id "123456" --image "path/to/image.jpg"
\`\`\`

### Identify a face:

\`\`\`bash
python client/client.py identify --image "path/to/image.jpg"
\`\`\`

## Environment Variables

- `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `GRPC_PORT`: gRPC server port (default: `50051`)

## Dependencies

- DeepFace: For face detection and embedding extraction
- MongoDB: For storing face embeddings
- gRPC: For API communication
- OpenCV: For image processing
- NumPy: For numerical operations
- Pillow: For image handling
- SciPy: For distance calculations

## License

MIT
