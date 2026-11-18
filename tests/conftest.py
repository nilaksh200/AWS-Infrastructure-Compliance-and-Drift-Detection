import pytest
from botocore.exceptions import ClientError

from engine.collector import CollectedS3State
from engine.models import SecurityBaseline


@pytest.fixture
def baseline() -> SecurityBaseline:
    return SecurityBaseline(
        bucket_name="idps-compliance-dev-640110193463-ap-south-1",
        bucket_arn="arn:aws:s3:::idps-compliance-dev-640110193463-ap-south-1",
        aws_region="ap-south-1",
        server_side_encryption_algorithm="AES256",
        versioning_status="Enabled",
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True,
        required_tags={
            "Project": "idps-compliance",
            "Environment": "dev",
            "ManagedBy": "Terraform",
        },
    )


@pytest.fixture
def compliant_state(baseline: SecurityBaseline) -> CollectedS3State:
    return CollectedS3State(
        bucket_name=baseline.bucket_name,
        bucket_exists=True,
        public_access_block={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
        encryption={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        },
        versioning={"Status": "Enabled"},
        tags={
            "Project": "idps-compliance",
            "Environment": "dev",
            "ManagedBy": "Terraform",
        },
    )


def make_client_error(code: str, message: str = "Mocked error", status_code: int = 400) -> ClientError:
    return ClientError(
        {
            "Error": {
                "Code": code,
                "Message": message,
            },
            "ResponseMetadata": {"HTTPStatusCode": status_code},
        },
        "TestOperation",
    )
