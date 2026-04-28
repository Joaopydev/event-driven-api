import aioboto3
import boto3

def get_async_s3_client():
    session = aioboto3.Session()
    return session.client("s3")

sync_s3_client = boto3.client("s3")

