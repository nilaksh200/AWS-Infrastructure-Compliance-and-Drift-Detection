# Policy-Driven Infrastructure Compliance and Drift Detection

A cloud-native infrastructure and security monitoring project built with **Terraform** and **AWS**. This project demonstrates how to enforce security baselines, detect configuration drift between live cloud environments and Infrastructure-as-Code (IaC) definitions, and maintain an immutable audit trail for college demonstration and real-world compliance.

---

## 📌 Project Overview & Roadmap

### Project Purpose
In modern cloud operations, unauthorized manual changes ("console clicks") and configuration drift weaken the security posture of an organization. This project establishes an automated pipeline to:
1. **Define Infrastructure as Code (IaC)** using pinned, secure Terraform configurations.
2. **Enforce Policy-Driven Compliance** ensuring all provisioned cloud resources adhere strictly to security baselines (such as CIS benchmarks and AWS security best practices).
3. **Detect and Report Configuration Drift** when live AWS resources diverge from the codified Terraform state.
4. **Provide a Unified Monitoring Interface** via an API backend and web dashboard for security auditing and drift visualization.

### Implementation Phases
* **Phase 1 (Current):** Terraform Infrastructure Foundation — Codified baseline S3 audit storage with strict security configurations (Block Public Access, SSE-S3 encryption, versioning, mandatory tagging).
* **Phase 2:** AWS Config & Policy Baseline — Codifying security compliance rules and automated policy checks.
* **Phase 3:** Automated Drift Detection Engine — Event-driven and scheduled drift detection comparing live state against declared IaC state.
* **Phase 4:** API Backend & Compliance Dashboard — FastAPI service and interactive dashboard for auditing, metrics, and alerts.

---

## 🏛️ Phase 1 Architecture: Infrastructure Foundation

Phase 1 establishes the storage foundation for compliance logs, drift reports, and state tracking.

```
+-----------------------------------------------------------------------+
|                              AWS Cloud                                |
|                                                                       |
|   +---------------------------------------------------------------+   |
|   | AWS Region: ap-south-1 (Configurable)                         |   |
|   |                                                               |   |
|   |   +-------------------------------------------------------+   |   |
|   |   | Dedicated S3 Audit Bucket                             |   |   |
|   |   | Name: idps-compliance-<env>-<account_id>-<region>     |   |   |
|   |   |                                                       |   |   |
|   |   |   * Block Public Access (All 4 flags enabled)         |   |   |
|   |   |   * Encryption: SSE-S3 (AES-256)                      |   |   |
|   |   |   * Object Versioning: Enabled                        |   |   |
|   |   |   * Tags: Project, Environment, ManagedBy="Terraform" |   |   |
|   |   +-------------------------------------------------------+   |   |
|   +---------------------------------------------------------------+   |
+-----------------------------------------------------------------------+
```

### Security Defaults Implemented
- **S3 Block Public Access**: All 4 flags (`block_public_acls`, `block_public_policy`, `ignore_public_acls`, `restrict_public_buckets`) are strictly enabled to prevent inadvertent data exposure.
- **Server-Side Encryption**: Configured with `AES256` (SSE-S3). This ensures all stored objects are encrypted at rest with zero additional AWS Key Management Service (KMS) API charges.
- **Object Versioning**: Enabled to protect against accidental deletions and to preserve a verifiable historical audit trail for drift detection.
- **Consistent Governance Tagging**: Standardized `Project`, `Environment`, and `ManagedBy` tags applied to every resource via provider-level default tags and explicit resource tags.

---

## 📂 Repository Structure

```
.
├── .gitignore                      # Excludes local state, secrets, and terraform cache
├── README.md                       # Project documentation and architectural guide
└── terraform/                      # Infrastructure-as-Code directory
    ├── versions.tf                 # Terraform and AWS provider version constraints
    ├── providers.tf                # AWS provider configuration and default tags
    ├── variables.tf                # Input variables, types, defaults, and validations
    ├── main.tf                     # S3 bucket, encryption, versioning, and public access blocks
    ├── outputs.tf                  # Non-sensitive outputs (bucket ID, ARN, encryption, region)
    └── terraform.tfvars.example    # Configuration template for local customization
```

---

## ⚙️ Prerequisites

Before working with the Terraform configurations, ensure you have the following tools installed and configured:

1. **Terraform CLI**: `v1.5.0` or newer.
   ```bash
   terraform -version
   ```
2. **AWS CLI**: Version 2 with active credentials configured.
   ```bash
   aws --version
   aws sts get-caller-identity
   ```
3. **AWS Permissions**: The authenticated IAM principal must possess permissions to manage S3 buckets within the target AWS account and region.

---

## 🔍 Validation and Local Review

Phase 1 is strictly restricted to local validation. No cloud infrastructure is modified during these steps.

Navigate to the `terraform/` directory:
```bash
cd terraform
```

### 1. Code Formatting
Ensure all Terraform configuration files conform to canonical style guidelines:
```bash
terraform fmt -check -recursive
```
*(If formatting issues are reported, run `terraform fmt` to automatically fix them).*

### 2. Provider Initialization (Local Backend)
Initialize the required provider plugins without binding to a remote backend:
```bash
terraform init -backend=false
```

### 3. Syntax and Schema Validation
Validate the internal syntax, resource schemas, and variable references:
```bash
terraform validate
```

---

## 🚀 Safe Provisioning and Destruction Workflow

> **IMPORTANT**: In Phase 1, **do NOT** run `terraform apply`. The commands below are documented for subsequent phases once formally approved.

### Safe Deployment Steps
1. **Prepare Variable Values**:
   Copy `terraform.tfvars.example` to `terraform.tfvars` and adjust values as needed:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Generate and Inspect Execution Plan**:
   Always save the speculative plan to an output file to review the exact changes before applying:
   ```bash
   terraform plan -out=tfplan
   ```
   Inspect the planned changes:
   ```bash
   terraform show tfplan
   ```

3. **Apply the Verified Plan**:
   Apply only the reviewed plan file. **Never use `-auto-approve`**:
   ```bash
   terraform apply tfplan
   ```

4. **Verify Provisioned Outputs**:
   Confirm that outputs match expectations:
   ```bash
   terraform output
   ```

### Safe Destruction Steps
When tearing down the infrastructure after demonstrations:
1. Ensure the S3 bucket is empty (versioned buckets must have all object versions and delete markers deleted before destruction).
2. Generate a destruction plan:
   ```bash
   terraform plan -destroy -out=destroy.tfplan
   ```
3. Apply the destruction plan:
   ```bash
   terraform apply destroy.tfplan
   ```

---

## 💰 Expected Costs & AWS Limitations

### Cost Breakdown
This configuration is specifically tailored for minimal cost in educational and test environments:
* **S3 Storage (Standard)**: ~$0.023 per GB/month in `ap-south-1`. Within the AWS Free Tier, users receive 5 GB of standard storage for the first 12 months.
* **Encryption (SSE-S3)**: **$0.00**. Using AWS-managed S3 keys (`AES256`) incurs no KMS request or customer-managed key charges.
* **Block Public Access**: **$0.00**.
* **Versioning Overhead**: Only charges for stored delta versions. For initial testing, storage usage is under a few megabytes.
* **Total Estimated Phase 1 Cost**: **$0.00 / month** (under AWS Free Tier) or < **$0.05 / month** for baseline testing without Free Tier.

### AWS Constraints & Boundaries
* **Bucket Naming**: S3 bucket names are globally unique across all AWS accounts worldwide. The bucket name is constrained between 3 and 63 characters and must only contain lowercase alphanumeric characters and hyphens.
* **Eventual Consistency**: Changes to bucket configurations (such as public access blocks) are strongly consistent, but downstream metrics and inventory configurations may experience minor propagation delays.
* **Regional Boundaries**: The baseline defaults to `ap-south-1` (Mumbai). Cross-region access should be avoided to prevent egress charges.
