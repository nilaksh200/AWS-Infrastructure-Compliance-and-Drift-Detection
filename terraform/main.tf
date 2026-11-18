data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  # Dynamically construct globally unique name: <project>-<env>-<account_id>-<region>
  # Complies with AWS S3 naming rules: 3-63 characters, lowercase alphanumeric and hyphens.
  default_bucket_name = lower("${var.project_name}-${var.environment}-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}")
  bucket_name         = coalesce(var.bucket_name_override, local.default_bucket_name)
}

# 1. Dedicated S3 Bucket
resource "aws_s3_bucket" "audit_bucket" {
  bucket = local.bucket_name

  tags = merge(
    var.additional_tags,
    {
      Name    = local.bucket_name
      Purpose = "IDPS Compliance Audit Logs and Artifacts"
    }
  )

  lifecycle {
    prevent_destroy = false
  }
}

# 2. Block All Public Access (All 4 settings enabled)
resource "aws_s3_bucket_public_access_block" "audit_bucket" {
  bucket = aws_s3_bucket.audit_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 3. Server-Side Encryption Configuration (SSE-S3 AES-256 for zero extra KMS cost)
resource "aws_s3_bucket_server_side_encryption_configuration" "audit_bucket" {
  bucket = aws_s3_bucket.audit_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 4. Bucket Versioning (Enabled to preserve drift state history and audit trail)
resource "aws_s3_bucket_versioning" "audit_bucket" {
  bucket = aws_s3_bucket.audit_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}
