import boto3
import logging

# Custom log format with timestamp and log level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# AWS LocalStack setup
AWS_REGION = "us-east-1"
DYNAMODB_ENDPOINT_URL = "http://localhost:4566"
S3_ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "shorten-files"

# Initialize LocalStack resources
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url=DYNAMODB_ENDPOINT_URL)
s3_client = boto3.client("s3", region_name=AWS_REGION, endpoint_url=S3_ENDPOINT_URL)

def create_tables():
    """Creates DynamoDB tables with necessary indexes"""
    try:
        # Users Table
        dynamodb.create_table(
            TableName="Users",
            KeySchema=[{"AttributeName": "username", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "username", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Shortened URLs Table with Global Secondary Index
        dynamodb.create_table(
            TableName="ShortenedUrls",
            KeySchema=[
                {"AttributeName": "short_id", "KeyType": "HASH"},
                {"AttributeName": "username", "KeyType": "RANGE"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "short_id", "AttributeType": "S"},
                {"AttributeName": "username", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'username-index',
                    'KeySchema': [
                        {'AttributeName': 'username', 'KeyType': 'HASH'},
                        {'AttributeName': 'short_id', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Create S3 Bucket
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        
        logging.info("DynamoDB tables and S3 bucket created successfully")

    except Exception as e:
        logging.error(f"Error creating tables: {e}")
        raise

# Initialize tables when the module is imported
create_tables()
