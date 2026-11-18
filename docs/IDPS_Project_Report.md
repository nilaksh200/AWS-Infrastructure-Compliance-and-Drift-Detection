# Project Report: Policy-Driven Infrastructure Compliance and Drift Detection

**Course:** IDPS  
**Prepared By:**  
- Nilaksh Pathak (23BCE199)  
- Deval Sindha (23BCE058)  

---

## 1. Project Overview

**Policy-Driven Infrastructure Compliance and Drift Detection** is an automated cloud governance and security monitoring system built with **Terraform**, **AWS**, and **Python**. The system defines a secure cloud storage baseline using Infrastructure as Code (IaC) and continuously verifies whether live cloud resources adhere to those codified standards or have drifted due to unauthorized modifications.

The application pairs a modular Python audit engine with an interactive **FastAPI** web dashboard. It enables cloud engineers and security auditors to run real-time, read-only health scans against AWS S3 buckets, detect configuration discrepancies (such as unencrypted buckets or removed public access blocks), compare live configurations with simulated drift scenarios in a side-by-side diff matrix, and export structured compliance audit reports.

---

## 2. Problem Statement & Motivation

### The Challenge
In modern cloud environments, teams define their target infrastructure using tools like Terraform. However, once deployed, cloud resources frequently undergo out-of-band manual changes—often called **"console clicks"**—made during debugging, urgent hotfixes, or operational troubleshooting. 

These manual adjustments lead to **configuration drift**:
- Accidental removal of public access protections, exposing sensitive data to the public internet.
- Modification or disabling of server-side encryption and versioning.
- Missing or altered mandatory governance tags, breaking organizational tracking.
- Outdated or misleading IaC state files that no longer match what is actually running in the cloud.

### Why This Project is Useful
Traditional enterprise tools (such as AWS Config or continuous third-party scanners) can be expensive, slow to update, and complex to configure for dedicated audit tasks. This project provides a **lightweight, immediate, and cost-effective solution**:
- **Zero Extra Cloud Costs:** Uses AWS-managed keys (`SSE-S3 AES-256`) and lightweight API calls with no recurring KMS key or event charges.
- **Instant Local Feedback:** Auditors can trigger live scans or run offline simulated audits with sub-second evaluation speeds.
- **Clear Actionable Reporting:** Pinpoints the exact property that drifted, showing expected values versus observed runtime values with clear explanations.

---

## 3. Key Features & Functionalities

- **Codified Terraform Baseline (`terraform/`):**
  - Dedicated audit storage bucket provisioned with dynamic naming (`idps-compliance-<env>-<account_id>-<region>`).
  - Strict 4-layer Public Access Block (`BlockPublicAcls`, `IgnorePublicAcls`, `BlockPublicPolicy`, `RestrictPublicBuckets`).
  - Mandatory Server-Side Encryption (`AES256`).
  - S3 Object Versioning enabled for tamper-evident change tracking.
  - Standardized governance tags (`Project`, `Environment`, `ManagedBy="Terraform"`).

- **Automated Telemetry Collection (`engine/collector.py`):**
  - Read-only queries executed via AWS SDK (`boto3`) without mutating cloud resources.
  - Independent collection across bucket existence, public access blocks, encryption, versioning, and tags.
  - Fault-tolerant error handling (e.g., handles missing tag sets or absent configurations without crashing).

- **Polymorphic Rule Evaluation Engine (`engine/evaluator.py`, `engine/rules/`):**
  - Evaluates 7 discrete security baselines simultaneously.
  - **Tri-State Audit System:** Distinctly marks rules as `COMPLIANT`, `NON_COMPLIANT` (configuration drift), or `ERROR` (network/access issues).

- **Interactive Web Dashboard & REST API (`dashboard/`):**
  - Built with **FastAPI** and served on `127.0.0.1:8000`.
  - **Live Scan Trigger:** One-click live AWS scan button with mutual exclusion locking (`asyncio.Lock`) to prevent race conditions.
  - **Scenario Comparison:** Tabbed interface allowing users to toggle between **Live AWS Telemetry**, a **Simulated Drift Scenario**, and a **Side-by-Side Diff Matrix**.
  - **Report Downloads:** Safe JSON report exporting with strict path-traversal security guards.

- **Dual-Mode CLI Support (`engine/main.py`):**
  - Supports live scanning as well as `--mock` and `--mock-drift` modes for testing and demonstration without active AWS credentials.

- **Automated Test Suite (`tests/`):**
  - Comprehensive suite of **44 automated tests** with 100% pass rate using `pytest` and `botocore.stub.Stubber`.

---

## 4. Tech Stack Used

| Layer | Technology | Purpose in Project |
| :--- | :--- | :--- |
| **Infrastructure as Code (IaC)** | **Terraform** (`>= 1.5.0`) & **AWS Provider** (`~> 5.0`) | Declares desired S3 bucket configuration, encryption, versioning, and public access blocks. |
| **Backend & Core Engine** | **Python** (`3.10+` / `3.14`) | Core evaluation logic, data models, and baseline hydration. |
| **Cloud SDK** | **Boto3** (`>= 1.34.0`) | Communicates with AWS S3 APIs to gather live resource metadata. |
| **API Framework** | **FastAPI** & **Uvicorn** | Asynchronous local REST API handling scans, comparisons, and asset serving. |
| **Frontend / UI** | **Vanilla HTML5, CSS3, ES6 JavaScript** | Single-page application dashboard with dark/light visual tokens, KPI metric cards, and responsive tables. |
| **Persistence / Artifacts** | **JSON** files (`reports/`) | Stores `live-compliance.json` and benchmark `simulated-drift.json`. |
| **Testing Harness** | **Pytest** (`>= 8.0.0`) | Automated unit tests, API tests, mock stubbing, and error simulation. |

---

## 5. How the System Works (Workflow)

### Operational Workflow
1. **Infrastructure Provisioning:** Terraform codifies the baseline S3 bucket with strict security defaults. Terraform outputs the provisioned bucket name, ARN, encryption algorithm, and region.
2. **Baseline Ingestion:** The compliance engine loads the desired state by running `terraform output -json` (with fallback to default schema if offline).
3. **Telemetry Collection:** When a scan is triggered (from the web UI or CLI), the `S3Collector` performs read-only calls (`head_bucket`, `get_public_access_block`, `get_bucket_encryption`, `get_bucket_versioning`, `get_bucket_tagging`).
4. **Rule Evaluation:** The `ComplianceEvaluator` runs the 7 policy rules against the collected data and categorizes each check as `COMPLIANT`, `NON_COMPLIANT`, or `ERROR`.
5. **Storage & Serialization:** Results are aggregated into a `ComplianceReport` object and saved to `reports/live-compliance.json`.
6. **Dashboard Visualization:** The web dashboard updates KPI cards (Total, Compliant, Drift, Errors), displays the policy table, and allows side-by-side comparison with the simulated drift scenario.

### Workflow Architecture
- **IaC Baseline (Terraform):** `main.tf`, `variables.tf`, `outputs.tf` define and output expected resource attributes.
- **Collection Layer (`S3Collector`):** Queries AWS S3 live endpoints over TLS using read-only Boto3 methods.
- **Evaluation Layer (`ComplianceEvaluator`):** Iterates over 7 atomic rules, comparing expected vs. observed configurations.
- **API & UI Layer (FastAPI & Dashboard):** Serves real-time telemetry, runs asynchronous threadpool scans, and renders diff matrices.

---

## 6. Setup & How to Run

### 6.1 Prerequisites
- **Python:** Version `3.10` or higher (verified on Python `3.14.2`).
- **Terraform:** Version `1.5.0` or higher.
- **AWS CLI & Credentials:** Configured with read permissions on AWS S3 (`aws configure`).

---

### 6.2 Execution Steps

#### Step 1: Open Terminal & Navigate to Directory
```powershell
cd "c:\Users\Nilaksh\Desktop\aidps assignment"
```

#### Step 2: Set Up Virtual Environment & Install Dependencies
```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
pip install fastapi uvicorn
```

#### Step 3: Validate Terraform Configurations
```powershell
cd terraform
terraform init -backend=false
terraform validate
terraform plan
cd ..
```

#### Step 4: Run CLI Compliance Audit (Fast / Offline Demos)
```powershell
# Run compliant baseline mock scan
python -m engine.main --mock

# Run simulated drift scan (shows detected drift in terminal)
python -m engine.main --mock-drift

# Run live scan against live AWS infrastructure
python -m engine.main --format terminal
```

#### Step 5: Launch the Interactive Web Dashboard
```powershell
uvicorn dashboard.app:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser and navigate to:  
**`http://127.0.0.1:8000`**

- Click **⚡ Run Live AWS Scan** to evaluate your live AWS environment.
- Click **Drift Delta Comparison** to view the live state side-by-side with the drift benchmark.
- Click **📥 Download** to export reports in structured JSON.

#### Step 6: Run Automated Tests
```powershell
pytest -v
```
*(Runs all 44 test cases covering baseline loading, mock AWS stubbing, rule evaluations, error handling, and API endpoints).*

---

## 7. Conclusion

This project implements a practical, policy-driven compliance and drift detection system that bridges Infrastructure as Code with runtime cloud reality. By pairing declarative Terraform baselines with an asynchronous Python evaluation engine, the system delivers sub-second drift detection, clear tri-state audit classification, and zero-cost S3 security monitoring. The project successfully achieves its engineering goals with 44 passing automated tests, providing a robust, extensible tool for modern cloud security audits.
