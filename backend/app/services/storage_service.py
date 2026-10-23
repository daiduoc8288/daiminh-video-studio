"""Storage service for S3/MinIO"""

import boto3
import os
from typing import Optional
from app.config import settings


class StorageService:
    """S3-compatible storage service"""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket = settings.S3_BUCKET

    def generate_presigned_url(
        self,
        object_name: str,
        expiration: int = 3600,
        method: str = "put_object",
    ) -> str:
        """Generate presigned URL for upload"""
        try:
            url = self.s3_client.generate_presigned_url(
                method,
                Params={"Bucket": self.bucket, "Key": object_name},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def upload_file(self, file_path: str, object_name: str) -> bool:
        """Upload file to S3"""
        try:
            self.s3_client.upload_file(file_path, self.bucket, object_name)
            return True
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def download_file(self, object_name: str, file_path: str) -> bool:
        """Download file from S3"""
        try:
            self.s3_client.download_file(self.bucket, object_name, file_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")

    def delete_file(self, object_name: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=object_name)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")

    def list_files(self, prefix: str = "") -> list:
        """List files in S3"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix,
            )
            if "Contents" not in response:
                return []
            return [obj["Key"] for obj in response["Contents"]]
        except Exception as e:
            raise Exception(f"Failed to list files: {str(e)}")

    def get_file_url(self, object_name: str) -> str:
        """Get public URL for file"""
        return f"{settings.S3_ENDPOINT_URL}/{self.bucket}/{object_name}"


# Singleton instance
storage_service = StorageService()
