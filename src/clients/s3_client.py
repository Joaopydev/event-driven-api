import aioboto3

def get_s3_client():
    session = aioboto3.Session()
    return session.client("s3")