from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class URLRequest(BaseModel):
    username: str
    full_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

class FileUploadRequest(BaseModel):
    username: str

class ShortUrlRedirect(BaseModel):
    redirect_to: Optional[str] = None
    file_url: Optional[str] = None

class ShortUrlItem(BaseModel):
    short_id: str = Field(..., description="Unique short identifier")
    username: str = Field(..., description="Username who created the short URL")
    full_url: Optional[str] = Field(None, description="Original full URL")
    file_s3_key: Optional[str] = Field(None, description="S3 key for uploaded file")
    created_at: Optional[str] = Field(None, description="Timestamp of URL creation")

    class Config:
        schema_extra = {
            "example": {
                "short_id": "abc123",
                "username": "johndoe",
                "full_url": "https://example.com",
                "created_at": "2025-02-15T17:30:00Z"
            }
        }

class ShortUrlListResponse(BaseModel):
    urls: List[ShortUrlItem]
    total_count: int = Field(..., description="Total number of short URLs")

    class Config:
        schema_extra = {
            "example": {
                "urls": [
                    {
                        "short_id": "abc123",
                        "username": "johndoe",
                        "full_url": "https://example.com"
                    },
                    {
                        "short_id": "def456",
                        "username": "johndoe",
                        "file_s3_key": "johndoe/file-upload.txt"
                    }
                ],
                "total_count": 2
            }
        }
