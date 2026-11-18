import pytest

from engine.baseline_loader import BaselineLoader, BaselineLoaderError


def test_baseline_loader_valid_nested_dict():
    raw_outputs = {
        "bucket_name": {"value": "test-audit-bucket"},
        "bucket_arn": {"value": "arn:aws:s3:::test-audit-bucket"},
        "aws_region": {"value": "ap-south-1"},
        "server_side_encryption_algorithm": {"value": "AES256"},
        "versioning_status": {"value": "Enabled"},
    }
    baseline = BaselineLoader.from_dict(raw_outputs)
    assert baseline.bucket_name == "test-audit-bucket"
    assert baseline.bucket_arn == "arn:aws:s3:::test-audit-bucket"
    assert baseline.aws_region == "ap-south-1"
    assert baseline.server_side_encryption_algorithm == "AES256"
    assert baseline.versioning_status == "Enabled"
    assert baseline.block_public_acls is True
    assert "Project" in baseline.required_tags


def test_baseline_loader_valid_flat_dict():
    raw = {
        "bucket_name": "flat-bucket-name",
        "aws_region": "us-east-1",
    }
    baseline = BaselineLoader.from_dict(raw)
    assert baseline.bucket_name == "flat-bucket-name"
    assert baseline.bucket_arn == "arn:aws:s3:::flat-bucket-name"
    assert baseline.server_side_encryption_algorithm == "AES256"
    assert baseline.versioning_status == "Enabled"


def test_baseline_loader_missing_bucket_name():
    with pytest.raises(BaselineLoaderError, match="Missing or invalid 'bucket_name'"):
        BaselineLoader.from_dict({"aws_region": {"value": "ap-south-1"}})


def test_baseline_loader_invalid_type():
    with pytest.raises(BaselineLoaderError, match="Expected dict"):
        BaselineLoader.from_dict("not-a-dict")  # type: ignore
