from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


@dataclass
class CollectedS3State:
    bucket_name: str
    bucket_exists: bool = False
    bucket_error: Optional[Exception] = None

    public_access_block: Optional[Dict[str, Any]] = None
    public_access_block_error: Optional[Exception] = None

    encryption: Optional[Dict[str, Any]] = None
    encryption_error: Optional[Exception] = None

    versioning: Optional[Dict[str, Any]] = None
    versioning_error: Optional[Exception] = None

    tags: Optional[Dict[str, str]] = None
    tags_error: Optional[Exception] = None


class S3Collector:
    """
    Read-only AWS S3 collector.
    Performs strictly idempotent, read-only queries and captures raw configurations or errors.
    """

    def __init__(self, s3_client: Optional[Any] = None, region_name: str = "ap-south-1"):
        self.s3 = s3_client or boto3.client("s3", region_name=region_name)

    def collect(self, bucket_name: str) -> CollectedS3State:
        state = CollectedS3State(bucket_name=bucket_name)

        # 1. Bucket Existence Check
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            state.bucket_exists = True
        except Exception as e:
            state.bucket_exists = False
            state.bucket_error = e

        # If head_bucket returned a fatal missing bucket error (404 / NoSuchBucket),
        # we can still attempt sub-resource checks or let individual rules handle it.
        # Running each sub-query independently ensures partial checks work even if head_bucket fails.

        # 2. Public Access Block
        try:
            pab_resp = self.s3.get_public_access_block(Bucket=bucket_name)
            state.public_access_block = pab_resp.get("PublicAccessBlockConfiguration", {})
        except Exception as e:
            state.public_access_block_error = e

        # 3. Server-Side Encryption
        try:
            enc_resp = self.s3.get_bucket_encryption(Bucket=bucket_name)
            state.encryption = enc_resp.get("ServerSideEncryptionConfiguration", {})
        except Exception as e:
            state.encryption_error = e

        # 4. Versioning Status
        try:
            ver_resp = self.s3.get_bucket_versioning(Bucket=bucket_name)
            state.versioning = ver_resp
        except Exception as e:
            state.versioning_error = e

        # 5. Bucket Tagging
        try:
            tag_resp = self.s3.get_bucket_tagging(Bucket=bucket_name)
            tag_set = tag_resp.get("TagSet", [])
            state.tags = {item["Key"]: item["Value"] for item in tag_set if "Key" in item and "Value" in item}
        except ClientError as e:
            # If no tags exist on the bucket, AWS returns NoSuchTagSet
            code = e.response.get("Error", {}).get("Code")
            if code == "NoSuchTagSet":
                state.tags = {}
            else:
                state.tags_error = e
        except Exception as e:
            state.tags_error = e

        return state
