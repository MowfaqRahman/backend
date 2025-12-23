#!/bin/bash

# EC2 Setup Script for Payment App Backend (Non-Interactive)
# Run this script on your EC2 instance to set up the backend

set -e

REPO_URL="https://github.com/MowfaqRahman/backend.git"

echo "=== Payment App Backend Setup ==="

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Python 3.11
echo "Installing Python 3.11..."
sudo yum install python3.11 python3.11-pip -y

# Install git
echo "Installing git..."
sudo yum install git -y

# Create application directory
echo "Creating application directory..."
mkdir -p ~/payment-app-backend
cd ~/payment-app-backend

# Clone repository
echo "Cloning repository from $REPO_URL..."
if [ -d ".git" ]; then
    echo "Repository already exists, pulling latest changes..."
    git pull
else
    git clone $REPO_URL .
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "Creating environment file..."
cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./sql_app.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost,http://13.48.123.186

# Add other environment variables as needed
EOF

echo ".env file created successfully"

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/payment-backend.service > /dev/null << EOF
[Unit]
Description=Payment App Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/payment-app-backend
Environment="PATH=$HOME/payment-app-backend/venv/bin"
ExecStart=$HOME/payment-app-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
echo "Starting backend service..."
sudo systemctl daemon-reload
sudo systemctl start payment-backend
sudo systemctl enable payment-backend

# Wait a moment for service to start
sleep 3

# Check service status
echo "Checking service status..."
sudo systemctl status payment-backend --no-pager

# Configure firewall
echo "Configuring firewall..."
sudo firewall-cmd --permanent --add-port=8000/tcp 2>/dev/null || true
sudo firewall-cmd --reload 2>/dev/null || true

echo ""
echo "=== Backend Setup Complete! ==="
echo "Backend is running on port 8000"
echo "Service status: sudo systemctl status payment-backend"
echo "View logs: sudo journalctl -u payment-backend -f"
echo ""
echo "Testing API..."
sleep 2
curl -s http://localhost:8000/health || echo "Health check endpoint not available"
echo ""
echo "Next steps:"
echo "1. Configure your EC2 security group to allow inbound traffic on port 8000"
echo "2. Set up GitHub secrets for CI/CD"
echo "3. Test the API: curl http://localhost:8000/health"
