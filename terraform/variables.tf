variable "aws_region" {
  description = "The AWS region where resources will be provisioned."
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-\\d{1}$", var.aws_region))
    error_message = "The aws_region variable must follow a valid AWS region naming format (e.g., ap-south-1, us-east-1)."
  }
}

variable "project_name" {
  description = "The project identifier used for resource naming and tagging."
  type        = string
  default     = "idps-compliance"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name)) && length(var.project_name) >= 3 && length(var.project_name) <= 24
    error_message = "The project_name must be 3-24 characters, containing lowercase alphanumeric characters and hyphens only."
  }
}

variable "environment" {
  description = "Target deployment environment (e.g., dev, test, staging, prod)."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "staging", "prod"], var.environment)
    error_message = "The environment variable must be one of: dev, test, staging, prod."
  }
}

variable "bucket_name_override" {
  description = "Optional explicit bucket name override. If null or empty, bucket name is dynamically constructed using project, environment, account ID, and region."
  type        = string
  default     = null
}

variable "additional_tags" {
  description = "Additional key-value tags to apply to the S3 bucket."
  type        = map(string)
  default     = {}
}
