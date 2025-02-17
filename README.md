# URL Shortener API

## Overview
A FastAPI-based URL shortening service with file upload capabilities, integrated with AWS LocalStack for local development.

## Features
- Shorten URLs
- Upload and share files
- User registration (placeholder)
- Health check endpoint

## Prerequisites
- Python 3.8+
- LocalStack
- Docker (optional, for LocalStack)

## Installation

1. Clone the repository

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start LocalStack
```bash
localstack start
```

## Running the Application

### Development Server
```bash
uvicorn app.main:app --reload

OR 

cd url-shortener/app && fastapi run main.py
```

### API Documentation
Access Swagger UI at: `http://localhost:8000/docs`
Access ReDoc at: `http://localhost:8000/redoc`

## API Endpoints

### URL Shortening
- `POST /shorten/url/`: Create a shortened URL
- `POST /upload/`: Upload a file and get a short link
- `GET /{short_id}`: Redirect to original URL or file

### System
- `GET /health`: Health check endpoint

## Configuration
- AWS LocalStack is used for local development
- Configuration is managed in `app/core/__init__.py`

## Testing
(Add testing instructions)

## Deployment
(Add deployment instructions)

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



Project Link: [https://github.com/yourusername/url-shortener](https://github.com/yourusername/url-shortener)
