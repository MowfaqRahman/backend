#!/bin/bash

# EC2 Setup Script for Payment App Backend
# Run this script on your EC2 instance to set up the backend

set -e

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

# Clone repository (you'll need to replace with your actual repo URL)
echo "Cloning repository..."
read -p "Enter your backend GitHub repository URL: " REPO_URL
git clone $REPO_URL .

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
CORS_ORIGINS=http://localhost,http://your-frontend-domain.com

# Add other environment variables as needed
EOF

echo "Please edit .env file with your actual configuration:"
echo "nano .env"
read -p "Press enter when done editing .env file..."

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

# Check service status
echo "Checking service status..."
sudo systemctl status payment-backend

# Configure firewall
echo "Configuring firewall..."
sudo firewall-cmd --permanent --add-port=8000/tcp || true
sudo firewall-cmd --reload || true

echo ""
echo "=== Backend Setup Complete! ==="
echo "Backend is running on port 8000"
echo "Service status: sudo systemctl status payment-backend"
echo "View logs: sudo journalctl -u payment-backend -f"
echo ""
echo "Next steps:"
echo "1. Configure your EC2 security group to allow inbound traffic on port 8000"
echo "2. Set up GitHub secrets for CI/CD"
echo "3. Test the API: curl http://localhost:8000/health"
