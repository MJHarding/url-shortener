import uuid
import logging
from botocore.exceptions import ClientError
from .core import dynamodb, s3_client, BUCKET_NAME
from typing import Dict
from datetime import datetime

def generate_short_id():
    """Generate a unique short ID."""
    return uuid.uuid4().hex[:6]

def create_shortened_url(username: str, full_url: str) -> str:
    """Create a shortened URL in DynamoDB."""
    table = dynamodb.Table("ShortenedUrls")
    short_id = generate_short_id()
    created_at = datetime.utcnow().isoformat()
    
    try:
        table.put_item(
            Item={
                "short_id": short_id,
                "username": username,
                "full_url": full_url,
                "created_at": created_at
            }
        )
        logging.info(f"Created short URL for {full_url}")
        return short_id
    except ClientError as e:
        logging.error(f"Error creating short URL: {e}")
        raise

def upload_file(username: str, file, filename: str) -> str:
    """Upload a file to S3 and create a shortened URL."""
    table = dynamodb.Table("ShortenedUrls")
    short_id = generate_short_id()
    created_at = datetime.utcnow().isoformat()
    
    try:
        # Generate unique file key
        file_key = f"{username}/{uuid.uuid4().hex}-{filename}"
        
        # Upload to S3
        s3_client.upload_fileobj(file, BUCKET_NAME, file_key)
        
        # Store in DynamoDB
        table.put_item(
            Item={
                "short_id": short_id,
                "username": username,
                "file_s3_key": file_key,
                "created_at": created_at
            }
        )
        
        logging.info(f"Uploaded file {filename} for user {username}")
        return short_id
    except ClientError as e:
        logging.error(f"Error uploading file: {e}")
        raise

def get_url_by_short_id(short_id: str):
    """Retrieve URL information by short ID."""
    table = dynamodb.Table("ShortenedUrls")
    
    try:
        # Scan the table to find the item with the matching short_id
        response = table.scan(
            FilterExpression='short_id = :short_id',
            ExpressionAttributeValues={
                ':short_id': short_id
            }
        )
        
        items = response.get('Items', [])
        
        if not items:
            return None
        
        # Return the first matching item
        return items[0]
    except ClientError as e:
        logging.error(f"Error retrieving short URL: {e}")
        raise

def get_all_short_urls_for_user(username: str) -> Dict:
    """Retrieve all short URLs for a specific username."""
    table = dynamodb.Table("ShortenedUrls")
    
    try:
        response = table.query(
            IndexName='username-index',
            KeyConditionExpression='username = :username',
            ExpressionAttributeValues={
                ':username': username
            }
        )
        
        items = response.get('Items', [])
        return {
            'urls': items,
            'total_count': len(items)
        }
    except ClientError as e:
        logging.error(f"Error retrieving short URLs for user {username}: {e}")
        raise
