from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from ..schemas import URLRequest, URLResponse, ShortUrlListResponse
from ..crud import (
    create_shortened_url, 
    upload_file, 
    get_url_by_short_id, 
    get_all_short_urls_for_user
)
import logging

router = APIRouter()

@router.post("/shorten/url/", response_model=URLResponse)
async def create_short_url(request: URLRequest):
    """Create a shortened URL."""
    try:
        short_id = create_shortened_url(
            username=request.username, 
            full_url=str(request.full_url)
        )
        return {"short_url": f"http://localhost:8000/{short_id}"}
    except Exception as e:
        logging.error(f"Error creating short URL: {e}")
        raise HTTPException(status_code=500, detail="Could not create short URL")

@router.post("/upload/", response_model=URLResponse)
async def upload_file_endpoint(
    username: str, 
    file: UploadFile = File(...)
):
    """Upload a file and create a shortened URL."""
    try:
        short_id = upload_file(
            username=username, 
            file=file.file, 
            filename=file.filename
        )
        return {"short_url": f"http://localhost:8000/{short_id}"}
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Could not upload file")

@router.get("/{short_id}")
async def redirect_to_url(short_id: str):
    """Redirect to the original URL or file."""
    try:
        item = get_url_by_short_id(short_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Short URL not found")
        
        if "full_url" in item:
            return RedirectResponse(url=item["full_url"], status_code=302)
        
        if "file_s3_key" in item:
            file_url = f"http://localhost:4566/shorten-files/{item['file_s3_key']}"
            return RedirectResponse(url=file_url, status_code=302)
        
        raise HTTPException(status_code=404, detail="Invalid short ID")
    
    except Exception as e:
        logging.error(f"Error redirecting short ID {short_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{username}/urls", response_model=ShortUrlListResponse)
async def list_user_short_urls(username: str):
    """Retrieve all short URLs for a specific user."""
    try:
        result = get_all_short_urls_for_user(username)
        return result
    except Exception as e:
        logging.error(f"Error retrieving short URLs for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve short URLs")
