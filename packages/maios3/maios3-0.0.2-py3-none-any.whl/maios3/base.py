import asyncio
from typing import Optional

from aiobotocore.session import get_session


class AsyncS3Handler:
    """
    Async S3 handler
    """
    session = get_session()

    def __init__(
        self,
        service: str,
        aws_secret_key: str,
        aws_access_key: str,
        bucket_name: str,
        endpoint_url: Optional[str] = None,
        use_ssl: bool = True,
    ) -> None:
        self.service = service
        self.aws_secret__key = aws_secret_key
        self.aws_access_key = aws_access_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.use_ssl = use_ssl

    async def put_object(self, data: bytes, key: str, acl: str = "private"):
        async with self.session.create_client(
            self.service, aws_secret_access_key=self.aws_secret__key, aws_access_key_id=self.aws_access_key,
            endpoint_url=self.endpoint_url, use_ssl=self.use_ssl,
        ) as client:
            response = await client.put_object(Bucket=self.bucket_name, Key=key, Body=data, ACL=acl)
            return response

    async def delete_object(self, key: str):
        async with self.session.create_client(
            self.service, aws_secret_access_key=self.aws_secret__key, aws_access_key_id=self.aws_access_key,
            endpoint_url=self.endpoint_url, use_ssl=self.use_ssl,
        ) as client:
            response = await client.delete_object(Bucket=self.bucket_name, Key=key)
            return response
