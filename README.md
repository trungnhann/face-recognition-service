# face-recognition-service

A Python microservice for face registration, identification, and deletion using gRPC and MongoDB.

## Features

- Register a face with a student ID
- Identify a face from an image
- Delete a face embedding by student ID
- Fast and easy integration via gRPC API

## Requirements

- Python 3.7+
- MongoDB
- pip

## Setup

```bash
# Clone the repository
git clone <https://github.com/trungnhann/face-recognition-service.git>
cd face-recognition

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Generate gRPC code (if you modify proto file)

```bash
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/face.proto
```

## Configuration

- MongoDB URI can be set via the `MONGO_URI` environment variable (default: `mongodb://localhost:27017/`).
- gRPC server port can be set via the `GRPC_PORT` environment variable (default: `50051`).

## Run the service

```bash
python server/server.py
```

## API

The service exposes the following gRPC methods:

- `RegisterFace`
- `IdentifyFace`
- `DeleteFace`

See `proto/face.proto` for request/response details.

## License

MIT
