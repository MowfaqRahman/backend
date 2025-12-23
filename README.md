# Payment App Backend

Python FastAPI backend for the Payment Collection Application.

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **ORM**: SQLAlchemy
- **Server**: Uvicorn

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <your-backend-repo-url>
cd payment-app-backend
```

2. Create a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
DATABASE_URL=sqlite:///./sql_app.db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost,http://localhost:3000
```

5. Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /customers` - Get all customers
- `POST /customers` - Create a new customer
- `PUT /customers/{id}` - Update a customer
- `DELETE /customers/{id}` - Delete a customer
- Additional endpoints as per your implementation

## Deployment to AWS EC2

### Initial Setup

1. **Launch an EC2 instance**:
   - AMI: Amazon Linux 2 or Ubuntu 20.04+
   - Instance type: t2.micro (or larger based on needs)
   - Security group: Allow inbound traffic on ports 22 (SSH) and 8000 (API)

2. **SSH into your EC2 instance**:
```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

3. **Run the setup script**:
```bash
# Copy the setup script to EC2
scp -i your-key.pem setup-ec2.sh ec2-user@your-ec2-ip:~

# SSH into EC2 and run the script
ssh -i your-key.pem ec2-user@your-ec2-ip
chmod +x setup-ec2.sh
./setup-ec2.sh
```

### GitHub Repository Setup

1. **Create a new GitHub repository** for the backend

2. **Add GitHub Secrets** (Settings → Secrets and variables → Actions):
   - `EC2_HOST`: Your EC2 instance public IP or domain
   - `EC2_USERNAME`: SSH username (usually `ec2-user` for Amazon Linux)
   - `EC2_SSH_KEY`: Your private SSH key content
   - `EC2_PORT`: SSH port (default: 22)

3. **Push your code**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-backend-repo-url>
git push -u origin main
```

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically:

1. ✅ Checkout code
2. ✅ Set up Python environment
3. ✅ Install dependencies
4. ✅ Run tests
5. ✅ Deploy to EC2 via SSH
6. ✅ Restart the backend service
7. ✅ Perform health check

Every push to the `main` branch triggers automatic deployment.

## Service Management on EC2

```bash
# Check service status
sudo systemctl status payment-backend

# View logs
sudo journalctl -u payment-backend -f

# Restart service
sudo systemctl restart payment-backend

# Stop service
sudo systemctl stop payment-backend

# Start service
sudo systemctl start payment-backend
```

## Environment Variables

Configure these in your `.env` file on EC2:

- `DATABASE_URL`: Database connection string
- `API_HOST`: Host to bind to (0.0.0.0 for all interfaces)
- `API_PORT`: Port to run on (default: 8000)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

## Production Recommendations

1. **Database**: Switch from SQLite to PostgreSQL:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

2. **Security**:
   - Use environment variables for sensitive data
   - Enable HTTPS with SSL certificate
   - Implement rate limiting
   - Add authentication/authorization

3. **Monitoring**:
   - Set up CloudWatch logs
   - Configure health check alerts
   - Monitor API performance

4. **Scaling**:
   - Use Application Load Balancer
   - Deploy multiple instances
   - Consider using ECS or EKS for container orchestration

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u payment-backend -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### Database connection issues
- Verify DATABASE_URL in .env file
- Check database permissions
- Ensure database service is running

### CORS errors
- Add frontend URL to CORS_ORIGINS
- Restart the service after changes

## License

[Your License]

## Contributors

[Your Name]
