# Setup and Installation Guide

This guide will help you set up the development environment for the MBA USP-ESALQ TCC Project.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or later
- Docker and Docker Compose
- Git

## Development Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/app-tcc-mba-uspesalq.git
cd app-tcc-mba-uspesalq
```

### 2. Set Up Python Virtual Environment

#### Create and activate a virtual environment:

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.\.venv\Scripts\activate
```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=app_tcc_mba

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Observability
PROMETHEUS_PORT=9090
```

### 4. Docker Setup (Alternative)

#### Build and start the Docker containers:

```bash
docker-compose up -d
```

This will set up:
- A MySQL database
- The API service
- Prometheus for monitoring

## Running the Application

### Without Docker

Start the application:

```bash
# Set PYTHONPATH to include the project root
export PYTHONPATH=$PWD  # Linux/macOS
$env:PYTHONPATH = $PWD  # Windows PowerShell

# Run the API
python src/infrastructure/api/main.py
```

### With Docker

```bash
docker-compose up api
```

The API will be available at http://localhost:8000

## Database Setup

### Initialize the Database

```bash
# Using Docker
docker-compose up -d db
docker exec -it app-tcc-mba-uspesalq_db_1 mysql -uroot -ppassword -e "CREATE DATABASE IF NOT EXISTS app_tcc_mba;"

# Manual Setup
mysql -uroot -ppassword -e "CREATE DATABASE IF NOT EXISTS app_tcc_mba;"
```

### Run Migrations

The application will automatically run migrations on startup. To manually run migrations:

```bash
python scripts/run_migrations.py
```

## Verification

To verify your setup is working correctly:

1. Access the API documentation at http://localhost:8000/docs
2. Check Prometheus at http://localhost:9090

## Troubleshooting

### Common Issues

#### Database Connection Errors

- Verify database credentials in the `.env` file
- Ensure the database container is running: `docker ps`
- Check database logs: `docker logs app-tcc-mba-uspesalq_db_1`

#### API Startup Issues

- Check if required ports are already in use
- Verify PYTHONPATH is set correctly
- Check for errors in the application logs

#### Docker Issues

- Run `docker-compose down -v` and then `docker-compose up -d` to reset containers
- Verify Docker daemon is running