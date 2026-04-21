import os
import logging
from dotenv import load_dotenv

from botocore.exceptions import ClientError
from ..clients.s3_client import s3_client


load_dotenv()


class StorageService:

    @classmethod
    def get_presigned_url(cls, file_key: str, content_type: str, expires_in: int = 600):
        # Generate pre-signed URL
        try:
            presigned_url = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": os.getenv("BUCKET_NAME"),
                    "Key": file_key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )
            return presigned_url
        except ClientError as e:
            logging.error(f"Error generating presigned URL: {e}")
            raise RuntimeError() from e
    
    @classmethod
    def get_object_from_bucket(cls, key: str):
        try:
            return s3_client.get_object(
                Bucket=os.getenv("BUCKET_NAME"),
                Key=key
            )
        except ClientError as e:
            logging.error(f"Failed to fetch object in s3: {e}")
            raise RuntimeError() from e
        
    @classmethod
    def read_object_content(cls, key: str):
        obj = cls.get_object_from_bucket(key)
        return obj["Body"].read()