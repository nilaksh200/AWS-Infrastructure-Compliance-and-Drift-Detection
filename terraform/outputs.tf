output "bucket_name" {
  description = "The globally unique name of the S3 audit bucket."
  value       = aws_s3_bucket.audit_bucket.id
}

output "bucket_arn" {
  description = "The Amazon Resource Name (ARN) of the S3 audit bucket."
  value       = aws_s3_bucket.audit_bucket.arn
}

output "aws_region" {
  description = "The AWS region where the bucket is provisioned."
  value       = var.aws_region
}

output "server_side_encryption_algorithm" {
  description = "The default server-side encryption algorithm configured for the bucket."
  value       = try(tolist(aws_s3_bucket_server_side_encryption_configuration.audit_bucket.rule)[0].apply_server_side_encryption_by_default[0].sse_algorithm, "AES256")
}

output "versioning_status" {
  description = "The versioning state of the S3 bucket."
  value       = try(aws_s3_bucket_versioning.audit_bucket.versioning_configuration[0].status, "Enabled")
}
