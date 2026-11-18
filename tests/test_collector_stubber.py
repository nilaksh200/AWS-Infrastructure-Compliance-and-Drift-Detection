import boto3
from botocore.stub import Stubber

from engine.collector import S3Collector


def test_collector_success_with_stubber():
    client = boto3.client("s3", region_name="ap-south-1")
    stubber = Stubber(client)
    bucket = "test-bucket"

    stubber.add_response("head_bucket", {}, {"Bucket": bucket})
    stubber.add_response(
        "get_public_access_block",
        {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            }
        },
        {"Bucket": bucket},
    )
    stubber.add_response(
        "get_bucket_encryption",
        {
            "ServerSideEncryptionConfiguration": {
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256"
                        }
                    }
                ]
            }
        },
        {"Bucket": bucket},
    )
    stubber.add_response(
        "get_bucket_versioning",
        {"Status": "Enabled"},
        {"Bucket": bucket},
    )
    stubber.add_response(
        "get_bucket_tagging",
        {
            "TagSet": [
                {"Key": "Project", "Value": "idps-compliance"},
                {"Key": "Environment", "Value": "dev"},
            ]
        },
        {"Bucket": bucket},
    )

    stubber.activate()
    try:
        collector = S3Collector(s3_client=client)
        state = collector.collect(bucket)

        assert state.bucket_exists is True
        assert state.public_access_block["BlockPublicAcls"] is True
        assert state.encryption["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] == "AES256"
        assert state.versioning["Status"] == "Enabled"
        assert state.tags["Project"] == "idps-compliance"
        assert state.bucket_error is None
    finally:
        stubber.deactivate()


def test_collector_no_such_tag_set_returns_empty_tags():
    client = boto3.client("s3", region_name="ap-south-1")
    stubber = Stubber(client)
    bucket = "test-bucket"

    stubber.add_response("head_bucket", {}, {"Bucket": bucket})
    stubber.add_response("get_public_access_block", {"PublicAccessBlockConfiguration": {}}, {"Bucket": bucket})
    stubber.add_response(
        "get_bucket_encryption",
        {
            "ServerSideEncryptionConfiguration": {
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256"
                        }
                    }
                ]
            }
        },
        {"Bucket": bucket},
    )
    stubber.add_response("get_bucket_versioning", {}, {"Bucket": bucket})
    stubber.add_client_error(
        "get_bucket_tagging",
        service_error_code="NoSuchTagSet",
        service_message="The TagSet does not exist",
        expected_params={"Bucket": bucket},
    )

    stubber.activate()
    try:
        collector = S3Collector(s3_client=client)
        state = collector.collect(bucket)

        assert state.tags == {}
        assert state.tags_error is None
    finally:
        stubber.deactivate()
