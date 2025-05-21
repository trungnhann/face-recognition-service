#!/bin/bash
yum update -y

# Cài đặt các dependencies hệ thống
yum install -y docker git cmake gcc gcc-c++ libX11-devel libXext libSM libXrender libglib2.0-0 libgl1-mesa-glx

# Khởi động Docker
service docker start
usermod -a -G docker ec2-user

# Cài đặt Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Tạo thư mục cho ứng dụng
mkdir -p /home/ec2-user/face-recognition
cd /home/ec2-user/face-recognition

# Clone repository
git clone <your-repo-url> .

# Cấu hình Docker Compose
cat > docker-compose.yml << 'EOL'
version: '3.8'fa
services:
  app:
    build: .
    ports:
      - "50051:50051"
    environment:
      - MONGODB_URI=mongodb+srv://trungnhanforwork:Nhan280803%40@cluster0.qalmkcs.mongodb.net/cmt?retryWrites=true&w=majority&appName=Cluster0&tls=true
    restart: always
    # Thêm cấu hình để tiết kiệm tài nguyên
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
EOL

# Build và chạy container
docker-compose up -d --build

# Cài đặt CloudWatch Agent để monitor
yum install -y amazon-cloudwatch-agent
cat > /opt/aws/amazon-cloudwatch-agent/bin/config.json << 'EOL'
{
    "metrics": {
        "metrics_collected": {
            "mem": {
                "measurement": ["mem_used_percent"]
            },
            "swap": {
                "measurement": ["swap_used_percent"]
            }
        }
    }
}
EOL
systemctl start amazon-cloudwatch-agent
systemctl enable amazon-cloudwatch-agent 