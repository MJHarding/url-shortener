from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import shortcode, user

app = FastAPI(
    title="URL Shortener API",
    description="A FastAPI-based URL shortening service with file upload capabilities",
    version="0.1.0",
    contact={
        "name": "API Support",
        "email": "support@urlshortener.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(shortcode.router, tags=["URL Shortening"])
app.include_router(user.router, prefix="/user", tags=["User"])

# Optional: Add a health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint to verify the application is running.
    
    Returns:
    - status: Current status of the application
    """
    return {"status": "healthy"}
