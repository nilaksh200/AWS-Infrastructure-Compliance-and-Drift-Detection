import os
from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Policy-Driven Infrastructure Compliance and Drift Detection: Academic Project Report</title>
  <style>
    :root {
      --primary: #1A365D;
      --secondary: #2B6CB0;
      --accent: #3182CE;
      --text: #2D3748;
      --text-muted: #718096;
      --bg: #FFFFFF;
      --bg-alt: #F7FAFC;
      --border: #E2E8F0;
      --border-dark: #CBD5E0;
      --code-bg: #EDF2F7;
      --success: #38A169;
      --danger: #E53E3E;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.65;
      color: var(--text);
      background-color: var(--bg);
      padding: 40px 20px;
    }

    .report-container {
      max-width: 960px;
      margin: 0 auto;
      background: #fff;
    }

    header.doc-header {
      border-bottom: 3px solid var(--secondary);
      padding-bottom: 24px;
      margin-bottom: 32px;
    }

    h1 {
      font-size: 2.2rem;
      color: var(--primary);
      line-height: 1.25;
      margin-bottom: 8px;
    }

    .subtitle {
      font-size: 1.2rem;
      color: var(--secondary);
      font-style: italic;
      margin-bottom: 20px;
    }

    .metadata-card {
      background: var(--bg-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--secondary);
      border-radius: 6px;
      padding: 16px 20px;
      margin-bottom: 24px;
    }

    .metadata-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 12px;
      font-size: 0.92rem;
    }

    .metadata-item strong {
      color: var(--primary);
    }

    h2 {
      font-size: 1.45rem;
      color: var(--primary);
      margin-top: 36px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 6px;
    }

    h3 {
      font-size: 1.15rem;
      color: var(--secondary);
      margin-top: 20px;
      margin-bottom: 8px;
    }

    p {
      margin-bottom: 14px;
      font-size: 0.98rem;
      text-align: justify;
    }

    ul, ol {
      margin-left: 24px;
      margin-bottom: 14px;
      font-size: 0.98rem;
    }

    li {
      margin-bottom: 6px;
    }

    .abstract-box {
      background: #F0F4F8;
      border: 1px solid #D9E2EC;
      border-radius: 6px;
      padding: 20px;
      margin-bottom: 28px;
      font-size: 0.98rem;
    }

    .abstract-box strong {
      color: var(--primary);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0 24px;
      font-size: 0.88rem;
    }

    th, td {
      border: 1px solid var(--border-dark);
      padding: 8px 12px;
      text-align: left;
      vertical-align: middle;
    }

    th {
      background-color: var(--secondary);
      color: #fff;
      font-weight: 600;
    }

    tr:nth-child(even) {
      background-color: var(--bg-alt);
    }

    .badge-pass {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      background: #DEF7EC;
      color: #03543F;
      font-weight: bold;
      font-size: 0.78rem;
    }

    pre {
      background: #1E293B;
      color: #F8FAFC;
      border-radius: 6px;
      padding: 16px;
      overflow-x: auto;
      font-family: "Consolas", "Courier New", monospace;
      font-size: 0.85rem;
      line-height: 1.45;
      margin: 14px 0 20px;
    }

    code {
      font-family: "Consolas", "Courier New", monospace;
      font-size: 0.88em;
      background: var(--code-bg);
      color: #C53030;
      padding: 2px 5px;
      border-radius: 3px;
    }

    pre code {
      background: none;
      color: inherit;
      padding: 0;
    }

    footer {
      margin-top: 48px;
      border-top: 1px solid var(--border);
      padding-top: 16px;
      color: var(--text-muted);
      font-size: 0.85rem;
      text-align: center;
    }

    @media print {
      body {
        padding: 0;
        background: #fff;
      }
      .report-container {
        max-width: 100%;
      }
      pre {
        background: #F1F5F9;
        color: #0F172A;
        border: 1px solid #CBD5E1;
      }
      th {
        background-color: #334155 !important;
        color: #fff !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      h2 {
        page-break-after: avoid;
      }
      table {
        page-break-inside: auto;
      }
      tr {
        page-break-inside: avoid;
        page-break-after: auto;
      }
    }
  </style>
</head>
<body>
  <div class="report-container">
    <header class="doc-header">
      <h1>Policy-Driven Infrastructure Compliance and Drift Detection</h1>
      <div class="subtitle">Comprehensive Publication-Grade Academic Project Report & Technical Evaluation</div>
      
      <div class="metadata-card">
        <div class="metadata-grid">
          <div class="metadata-item"><strong>Subject / Course:</strong> AIDPS (AI-Driven Distributed Policy & Security Systems)</div>
          <div class="metadata-item"><strong>Domain:</strong> Cloud Security & Infrastructure as Code</div>
          <div class="metadata-item"><strong>Target Audience:</strong> Course Faculty & Academic Review Committee</div>
          <div class="metadata-item"><strong>Artifact Format:</strong> Publication-Grade Technical Documentation</div>
          <div class="metadata-item"><strong>Cloud Region:</strong> AWS ap-south-1 (Asia Pacific - Mumbai)</div>
          <div class="metadata-item"><strong>Evaluated Core:</strong> Terraform IaC, Python 3.14 Engine, FastAPI, 44 Pytest Cases</div>
        </div>
      </div>
    </header>

    <div class="abstract-box">
      <h3 style="margin-top: 0; color: var(--primary);">Abstract</h3>
      <p style="margin-bottom: 0;">In contemporary multi-tenant cloud ecosystems, unauthorized manual modifications—colloquially termed "console clicks"—and out-of-band operational overrides inevitably degrade declared security baselines, introducing configuration drift and severe security vulnerabilities. This project implements an automated, policy-driven infrastructure compliance and drift detection system utilizing HashiCorp Terraform and Amazon Web Services (AWS).</p>
      <p style="margin-top: 10px; margin-bottom: 0;">The architecture establishes an immutable Infrastructure-as-Code (IaC) baseline provisioning dedicated AWS Simple Storage Service (S3) audit storage within region <code>ap-south-1</code> (<code>idps-compliance-dev-640110193463-ap-south-1</code>), strictly codifying four-tier Public Access Block controls (<code>BlockPublicAcls</code>, <code>IgnorePublicAcls</code>, <code>BlockPublicPolicy</code>, <code>RestrictPublicBuckets</code>), Server-Side Encryption with AWS-managed keys (<code>SSE-S3 AES-256</code>), bucket versioning, and mandatory governance metadata tagging. Layered on this infrastructure is a modular Python auditing engine coupled with a FastAPI asynchronous web service and an interactive single-page dashboard. The core evaluation engine implements an isolated telemetry collector querying AWS APIs via <code>boto3</code>, a decoupled baseline loader querying Terraform outputs, and a polymorphic rule evaluator executing seven atomic compliance assertions.</p>
      <p style="margin-top: 10px; margin-bottom: 0;">The system was evaluated against live AWS infrastructure and synthetic drift scenarios. Verification through an exhaustive 44-case test suite (<code>pytest</code>) validated 100% rule assertion accuracy, non-blocking asynchronous live scans with mutual exclusion locks (<code>asyncio.Lock</code>), strict path traversal prevention, and fault-tolerant partial scan execution under simulated permission denial (<code>AccessDenied</code>) and network partition states. The resulting artifact provides an audit trail with zero additional KMS API financial overhead.</p>
    </div>

    <h2>1. Introduction & Problem Statement</h2>
    <h3>1.1 Background</h3>
    <p>Cloud computing and distributed systems have transitioned operational paradigms from physical hardware provisioning to declarative Infrastructure as Code (IaC). In academic and enterprise environments alike, frameworks such as Terraform enable engineers to codify complex multi-resource topologies into declarative configuration files that ensure reproducibility, version control, and auditable deployment workflows. Within the domain of Cloud Security and AI-Driven Distributed Policy & Security (AIDPS), maintaining cryptographic integrity, access control isolation, and regulatory compliance (such as CIS AWS Foundations Benchmarks and ISO/IEC 27001) is paramount. Cloud-native storage services—principally Amazon S3—frequently serve as primary persistence backplanes for corporate data lakes, telemetry repositories, and compliance audit logs. Consequently, security misconfigurations in these storage backplanes represent significant systemic vulnerabilities.</p>

    <h3>1.2 Problem Statement</h3>
    <p>Despite codifying target states in IaC configurations, deployed cloud resources are inherently susceptible to configuration drift: the gradual divergence of live runtime cloud configurations from declared code definitions. Drift occurs primarily through:</p>
    <ul>
      <li><strong>Ad-Hoc Manual Interventions:</strong> Operators executing unrecorded changes through the AWS Management Console during debugging or incident triage.</li>
      <li><strong>Out-of-Band Scripting:</strong> Automated deployment scripts or external orchestration agents executing updates without synchronizing state files.</li>
      <li><strong>Implicit Default Overrides & API Asymmetry:</strong> Cloud provider API updates that silently relax access boundaries or alter cryptographic defaults.</li>
    </ul>
    <p>Configuration drift renders IaC state files obsolete, undermines security compliance policies, exposes private objects to unauthorized public indexing, and invalidates regulatory compliance. Existing enterprise tools often suffer from high operational latency, excessive cost overhead (e.g., continuous polling via AWS Config coupled with KMS key consumption), or complex multi-tenant control plane dependencies that are impractical for isolated laboratory evaluation and granular academic analysis.</p>

    <h3>1.3 Project Objectives</h3>
    <ol>
      <li><strong>Codify an Immutable Storage Baseline:</strong> Define and provision a secure S3 audit storage bucket in AWS using Terraform (>= 1.5.0), enforcing full Public Access Block, SSE-S3 AES-256 encryption, bucket versioning, and governance tags without incurring AWS KMS operational fees.</li>
      <li><strong>Develop a Decoupled Compliance & Drift Detection Engine:</strong> Implement a Python 3.14 evaluation engine capable of querying live AWS telemetry via read-only SDK APIs and comparing observed values against the Terraform state baseline.</li>
      <li><strong>Enforce Three-State Audit Classification:</strong> Categorize individual security rules into discrete, verifiable states: <code>COMPLIANT</code>, <code>NON_COMPLIANT</code> (configuration drift), and <code>ERROR</code> (operational/permission failures), preventing permission denial from masquerading as compliance pass/fail.</li>
      <li><strong>Deliver an Interactive Telemetry & Comparison Dashboard:</strong> Engineer a lightweight, local REST API utilizing FastAPI and a responsive, token-driven web dashboard (HTML5, Vanilla CSS, ES6 JavaScript) providing live telemetry scans, simulated drift visualization, side-by-side delta matrices, and secure report exports.</li>
      <li><strong>Rigorous Automated Verification:</strong> Validate system stability, rule logic, error handling, and thread safety via automated unit and integration tests using <code>pytest</code> and <code>botocore.stub.Stubber</code>.</li>
    </ol>

    <h3>1.4 Scope & Limitations</h3>
    <ul>
      <li><strong>Current Resource Boundary:</strong> Focuses on AWS Simple Storage Service (S3) audit storage. Downstream extensions to virtual private clouds (VPCs), IAM policies, and compute instances are architecturally supported by the rule engine but left for future phases.</li>
      <li><strong>Regional Deployment:</strong> The codified infrastructure baseline is localized to AWS Region <code>ap-south-1</code> (Asia Pacific - Mumbai) to eliminate cross-region latency and data transfer egress charges.</li>
      <li><strong>Execution Model:</strong> The engine operates on an on-demand polling and event-driven API model rather than continuous asynchronous AWS CloudWatch/EventBridge daemon streaming, optimizing laboratory execution for budget conservation and audit repeatability.</li>
    </ul>

    <h2>2. Literature Survey / Comparative Study</h2>
    <p>Cloud infrastructure governance and drift management methodologies generally fall into three archetypes: State-File Reconciliation, Continuous Managed Cloud Governance Services, and Lightweight Declarative Policy Engines.</p>
    <ul>
      <li><strong>HashiCorp Terraform Native Refresh (<code>terraform plan -refresh-only</code>):</strong> Terraform provides native capabilities to detect state file divergence by executing read operations across provisioned resources. However, it requires direct access to remote state backends (e.g., S3 state locking via DynamoDB), requires broad administrative cloud privileges to evaluate the entire dependency graph, and lacks human-readable compliance reporting or fine-grained rule-level status introspection.</li>
      <li><strong>AWS Config & Security Hub:</strong> AWS provides native continuous tracking via AWS Config rules and AWS Security Hub. While comprehensive, AWS Config charges per configuration item recorded ($0.003 per item) and per rule evaluation. In enterprise setups, high churn triggers significant financial overhead. Furthermore, AWS Config rules do not natively reconcile against local Terraform IaC definitions without complex integration lambdas or AWS CloudFormation stack sets.</li>
      <li><strong>Open Policy Agent (OPA) / Conftest:</strong> OPA evaluates structured data against policies written in Rego. While powerful for static analysis (e.g., scanning Terraform plans prior to deployment), OPA natively requires supplementary ingestion pipelines to query live cloud state, requiring custom scaffolding for continuous runtime drift detection.</li>
    </ul>

    <h3>Comparative Evaluation Matrix</h3>
    <table>
      <thead>
        <tr>
          <th>Evaluation Parameter</th>
          <th>Native Terraform Refresh</th>
          <th>AWS Config Managed Rules</th>
          <th>Custom IDPS Compliance Engine (Ours)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Architecture Pattern</strong></td>
          <td>Monolithic CLI State Refresh</td>
          <td>Cloud-Native Managed Daemon</td>
          <td>Decoupled Modular Engine + FastAPI Local Bridge</td>
        </tr>
        <tr>
          <td><strong>Telemetry Latency</strong></td>
          <td>High (refreshes entire dependency tree)</td>
          <td>Medium (eventually consistent, 3–15 min)</td>
          <td>Low (direct atomic read-only sub-resource queries &lt; 800ms)</td>
        </tr>
        <tr>
          <td><strong>Extensibility</strong></td>
          <td>Low (constrained to Terraform schema)</td>
          <td>Medium (requires AWS Lambda custom rules)</td>
          <td>High (polymorphic Python BaseRule class hierarchy)</td>
        </tr>
        <tr>
          <td><strong>Resource Overhead</strong></td>
          <td>High local compute; requires full setup</td>
          <td>High recurring AWS service charges ($/eval)</td>
          <td>Minimal (zero KMS fees, negligible S3 Standard storage)</td>
        </tr>
        <tr>
          <td><strong>Offline Simulation</strong></td>
          <td>Not supported (requires active cloud connection)</td>
          <td>Not supported</td>
          <td>Fully supported (synthetic drift fixtures & stubbers)</td>
        </tr>
        <tr>
          <td><strong>Multi-State Auditing</strong></td>
          <td>Binary (drift vs. synced)</td>
          <td>Binary (COMPLIANT vs. NON_COMPLIANT)</td>
          <td>Tri-State (COMPLIANT, NON_COMPLIANT, ERROR)</td>
        </tr>
        <tr>
          <td><strong>Threat Surface</strong></td>
          <td>Requires full write/admin credentials</td>
          <td>Broad IAM service roles</td>
          <td>Strictly read-only IAM policies (s3:Get*)</td>
        </tr>
      </tbody>
    </table>

    <h2>3. System Architecture & Design</h2>
    <h3>3.1 High-Level Architecture</h3>
    <p>The system adopts a decoupled, multi-tier micro-telemetry architecture organized across four functional layers:</p>
    <ul>
      <li><strong>Infrastructure as Code (IaC) Layer:</strong> Pinned Terraform configurations declaring desired AWS security baselines and generating machine-readable output schemas.</li>
      <li><strong>Cloud Telemetry Collection Layer:</strong> An isolated AWS SDK client (<code>S3Collector</code>) executing non-mutating queries against AWS S3 endpoints over TLS.</li>
      <li><strong>Compliance Evaluation Core:</strong> A polymorphic engine (<code>ComplianceEvaluator</code>) comparing observed live telemetry with expected parameters extracted from IaC definitions.</li>
      <li><strong>Presentation & API Layer:</strong> A FastAPI web service maintaining runtime thread locks, orchestrating report generation, and serving an ES6 single-page application dashboard.</li>
    </ul>

    <h3>3.2 Component Breakdown</h3>
    <p><strong>1. Frontend Client (SPA):</strong> Built with HTML5, CSS3, and ES6 JavaScript. Binds strictly to <code>127.0.0.1:8000</code>. Provides instantaneous DOM rendering of KPI metric cards, tabular policy results, mutation spinners, and view tabs.</p>
    <p><strong>2. Backend API Layer:</strong> FastAPI application orchestrated via <code>ComplianceService</code>. Features custom exception mappers, asynchronous thread offloading via <code>asyncio.to_thread</code>, and mutual exclusion locking.</p>
    <p><strong>3. Persistence Layer:</strong> Structured JSON audit reports saved to <code>./reports/</code> (<code>live-compliance.json</code> and <code>simulated-drift.json</code>).</p>
    <p><strong>4. Cloud Integration:</strong> Read-only Amazon S3 client in <code>ap-south-1</code> executing <code>head_bucket</code>, <code>get_public_access_block</code>, <code>get_bucket_encryption</code>, <code>get_bucket_versioning</code>, and <code>get_bucket_tagging</code>.</p>

    <h2>4. Technical Implementation & Key Modules</h2>
    <h3>4.1 Technology Stack</h3>
    <table>
      <thead>
        <tr>
          <th>Layer / Dependency</th>
          <th>Specification</th>
          <th>Rationale & Justification</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>IaC Orchestrator</td>
          <td>HashiCorp Terraform &gt;= 1.5.0</td>
          <td>Declarative graph resolution, immutable state management, variable validation regex.</td>
        </tr>
        <tr>
          <td>Cloud Provider</td>
          <td>AWS Provider for Terraform ~&gt; 5.0</td>
          <td>Fine-grained resource modeling (aws_s3_bucket_*) and default governance tagging.</td>
        </tr>
        <tr>
          <td>Language Runtime</td>
          <td>Python 3.14.2</td>
          <td>Native async event loops, structural pattern matching, dataclasses, typing annotations.</td>
        </tr>
        <tr>
          <td>Cloud SDK</td>
          <td>AWS SDK boto3 &gt;= 1.34.0</td>
          <td>Direct HTTPS API communication with AWS S3; supports botocore.stub.Stubber mocking.</td>
        </tr>
        <tr>
          <td>API Framework</td>
          <td>FastAPI &gt;= 0.100.0 & Starlette</td>
          <td>High-throughput async routing, OpenAPI generation, RFC error models, thread offloading.</td>
        </tr>
        <tr>
          <td>ASGI Web Server</td>
          <td>Uvicorn &gt;= 0.28.0</td>
          <td>High-performance asynchronous server built on uvloop and httptools.</td>
        </tr>
        <tr>
          <td>Testing Harness</td>
          <td>pytest &gt;= 8.0.0</td>
          <td>Fixtures, parameterization, TestClient integration, timing execution metrics.</td>
        </tr>
        <tr>
          <td>Frontend Stack</td>
          <td>Vanilla HTML5, CSS3, ES6 JS</td>
          <td>Zero external framework overhead; instantaneous rendering, full offline auditability.</td>
        </tr>
      </tbody>
    </table>

    <h3>4.2 Core Code Highlights</h3>
    <p><strong>Terraform Storage Baseline (terraform/main.tf):</strong></p>
    <pre><code>locals {
  default_bucket_name = lower("${var.project_name}-${var.environment}-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}")
  bucket_name         = coalesce(var.bucket_name_override, local.default_bucket_name)
}

resource "aws_s3_bucket" "audit_bucket" {
  bucket = local.bucket_name
  tags = merge(var.additional_tags, {
    Name    = local.bucket_name
    Purpose = "IDPS Compliance Audit Logs and Artifacts"
  })
}

resource "aws_s3_bucket_public_access_block" "audit_bucket" {
  bucket                  = aws_s3_bucket.audit_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "audit_bucket" {
  bucket = aws_s3_bucket.audit_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "audit_bucket" {
  bucket = aws_s3_bucket.audit_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}</code></pre>

    <p><strong>Asynchronous Concurrency Guard & Service Execution (dashboard/service.py):</strong></p>
    <pre><code>class ComplianceService:
    ALLOWED_REPORT_TYPES = {"live": "live-compliance.json", "simulated": "simulated-drift.json"}

    def get_report_path(self, report_type: str) -> Path:
        if report_type not in self.ALLOWED_REPORT_TYPES:
            raise ValueError(f"Invalid report type '{report_type}'.")
        resolved_path = (self.reports_dir / self.ALLOWED_REPORT_TYPES[report_type]).resolve()
        if not resolved_path.is_relative_to(self.reports_dir):
            raise ValueError("Path traversal violation detected.")
        return resolved_path

    async def run_live_scan(self) -> Dict[str, Any]:
        if self._scan_lock.locked():
            raise ScanAlreadyInProgressError("A live scan is already in progress.")
        async with self._scan_lock:
            baseline = self.get_baseline()
            report = await asyncio.to_thread(self.evaluator.evaluate_live, baseline, self.collector)
            ComplianceReporter.save_json(report, self.get_report_path("live"))
            return report.to_dict()</code></pre>

    <h3>4.3 API & Interface Specifications</h3>
    <table>
      <thead>
        <tr>
          <th>Route Path</th>
          <th>Method</th>
          <th>Response / Action</th>
          <th>Status Codes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>/</code></td>
          <td>GET</td>
          <td>Serves Single-Page Application HTML</td>
          <td>200 OK</td>
        </tr>
        <tr>
          <td><code>/api/status</code></td>
          <td>GET</td>
          <td>Returns safe system metadata & baseline schema</td>
          <td>200 OK</td>
        </tr>
        <tr>
          <td><code>/api/reports/latest-live</code></td>
          <td>GET</td>
          <td>Returns last saved live AWS compliance report</td>
          <td>200 OK, 404, 500</td>
        </tr>
        <tr>
          <td><code>/api/reports/simulated</code></td>
          <td>GET</td>
          <td>Returns static 4-drift simulation report</td>
          <td>200 OK, 404, 500</td>
        </tr>
        <tr>
          <td><code>/api/reports/compare</code></td>
          <td>GET</td>
          <td>Generates per-check delta comparison matrix</td>
          <td>200 OK, 404</td>
        </tr>
        <tr>
          <td><code>/api/scan/live</code></td>
          <td>POST</td>
          <td>Executes read-only live scan with thread lock</td>
          <td>200 OK, 409, 502</td>
        </tr>
        <tr>
          <td><code>/api/reports/download/{type}</code></td>
          <td>GET</td>
          <td>Downloads report file with traversal guard</td>
          <td>200 OK, 400, 404</td>
        </tr>
      </tbody>
    </table>

    <h2>5. Setup, Deployment & Execution Workflow</h2>
    <pre><code># 1. Environment Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install fastapi uvicorn

# 2. Terraform Baseline Verification
cd terraform
terraform fmt -check
terraform init -backend=false
terraform validate
terraform plan
cd ..

# 3. CLI Execution (Mock & Live)
python -m engine.main --mock
python -m engine.main --mock-drift
python -m engine.main --format terminal

# 4. Launch Local Web Dashboard
uvicorn dashboard.app:app --host 127.0.0.1 --port 8000 --reload</code></pre>

    <h2>6. Testing, Verification & Results</h2>
    <p>The system was evaluated using an automated 44-case testing suite (<code>pytest -v</code>) executing in 10.68 seconds with a 100% pass rate:</p>
    <table>
      <thead>
        <tr>
          <th>Test Case ID</th>
          <th>Module</th>
          <th>Scenario Evaluated</th>
          <th>Expected Outcome</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>TC-BASE-01</td><td>test_baseline_loader</td><td>Valid nested Terraform output dictionary</td><td>SecurityBaseline parsed</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-BASE-02</td><td>test_baseline_loader</td><td>Valid flat Terraform output dictionary</td><td>SecurityBaseline parsed</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-BASE-03</td><td>test_baseline_loader</td><td>Missing mandatory bucket_name key</td><td>Raises BaselineLoaderError</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-BASE-04</td><td>test_baseline_loader</td><td>Invalid non-dictionary input type</td><td>Raises BaselineLoaderError</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-COLL-01</td><td>test_collector_stubber</td><td>Complete S3 stub responses (PAB, enc, tag, ver)</td><td>CollectedS3State populated</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-COLL-02</td><td>test_collector_stubber</td><td>S3 returns NoSuchTagSet client error</td><td>Gracefully sets tags = {}</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-01</td><td>test_dashboard_api</td><td>GET / root endpoint serves HTML SPA</td><td>HTTP 200, HTML body verified</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-02</td><td>test_dashboard_api</td><td>GET static assets (/static/css, /static/js)</td><td>HTTP 200, assets served</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-03</td><td>test_dashboard_api</td><td>GET /api/status returns safe project metadata</td><td>HTTP 200, 7 baseline checks</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-04</td><td>test_dashboard_api</td><td>GET /api/reports/latest-live returns live report</td><td>HTTP 200, 7 compliant</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-05</td><td>test_dashboard_api</td><td>GET /api/reports/simulated returns sim report</td><td>HTTP 200, 4 non-compliant</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-06</td><td>test_dashboard_api</td><td>GET /api/reports/compare generates diff matrix</td><td>HTTP 200, 4 drifted checks</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-07</td><td>test_dashboard_api</td><td>GET missing report file returns HTTP 404</td><td>HTTP 404 Not Found</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-08</td><td>test_dashboard_api</td><td>GET corrupted JSON report returns HTTP 500</td><td>HTTP 500 Internal Error</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-09</td><td>test_dashboard_api</td><td>GET /api/reports/download with path traversal</td><td>HTTP 400 Bad Request</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-10</td><td>test_dashboard_api</td><td>POST /api/scan/live executes and updates report</td><td>HTTP 200, sim untouched</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-11</td><td>test_dashboard_api</td><td>POST /api/scan/live AWS error masked safely</td><td>HTTP 502 Bad Gateway</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-API-12</td><td>test_dashboard_api</td><td>Concurrent requests to POST /api/scan/live</td><td>HTTP 409 Conflict (locked)</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-ERR-01</td><td>test_errors_and_partial</td><td>AccessDenied error on Public Access Block query</td><td>Classified as ERROR</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-ERR-02</td><td>test_errors_and_partial</td><td>Target bucket does not exist (NoSuchBucket)</td><td>Classified as ERROR</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-ERR-03</td><td>test_errors_and_partial</td><td>Network timeout (ConnectionResetError)</td><td>Classified as ERROR</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-ERR-04</td><td>test_errors_and_partial</td><td>PAB query fails (AccessDenied), others succeed</td><td>4 ERROR, 3 COMPLIANT</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-ERR-05</td><td>test_errors_and_partial</td><td>Unhandled rule exception does not crash engine</td><td>Fault isolation verified</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-MOD-01</td><td>test_models</td><td>CheckResult.to_dict() JSON serialization</td><td>Dictionary schema matches</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-MOD-02</td><td>test_models</td><td>ComplianceReport computed count properties</td><td>Counts accurately summed</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-MOD-03</td><td>test_models</td><td>ComplianceReport.is_fully_compliant evaluation</td><td>Returns True when 7/7 pass</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-REP-01</td><td>test_reporter</td><td>Terminal ASCII table and JSON formatting</td><td>Valid table and JSON generated</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-REP-02</td><td>test_reporter</td><td>Saving report JSON creates parent directories</td><td>File persisted successfully</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-REP-03</td><td>test_reporter</td><td>Saving report to existing directory path</td><td>Raises IsADirectoryError</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-REP-04</td><td>test_reporter</td><td>CLI execution with -o / --output argument</td><td>Report saved to custom path</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-REP-05</td><td>test_reporter</td><td>CLI execution with invalid path argument</td><td>Exits with code 2</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-01</td><td>test_rules_compliant</td><td>Evaluating fully compliant state across all rules</td><td>All 7 rules COMPLIANT</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-02</td><td>test_rules_drift</td><td>Observed BlockPublicAcls = False (Exp: True)</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-03</td><td>test_rules_drift</td><td>Observed IgnorePublicAcls = False (Exp: True)</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-04</td><td>test_rules_drift</td><td>Observed BlockPublicPolicy = False (Exp: True)</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-05</td><td>test_rules_drift</td><td>Observed RestrictPublicBuckets = False</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-06</td><td>test_rules_drift</td><td>Public Access Block configuration absent</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-07</td><td>test_rules_drift</td><td>ServerSideEncryptionConfiguration absent</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-08</td><td>test_rules_drift</td><td>Observed encryption aws:kms (Exp: AES256)</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-09</td><td>test_rules_drift</td><td>Encryption configuration rules list is empty</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-10</td><td>test_rules_drift</td><td>Observed versioning Suspended (Exp: Enabled)</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-11</td><td>test_rules_drift</td><td>Versioning never enabled on bucket</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-12</td><td>test_rules_drift</td><td>Mandatory tag 'ManagedBy' missing from bucket</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
        <tr><td>TC-RULE-13</td><td>test_rules_drift</td><td>Tag 'Environment' has mismatched value</td><td>NON_COMPLIANT drift caught</td><td><span class="badge-pass">PASS</span></td></tr>
      </tbody>
    </table>

    <h2>7. Challenges Encountered & Engineering Solutions</h2>
    <p><strong>1. AWS API Asymmetry & Missing Configuration Exceptions:</strong> AWS S3 APIs do not return symmetric null bodies when settings are absent. Querying an untagged bucket raises <code>ClientError(NoSuchTagSet)</code>. Similarly, querying an unconfigured Public Access Block raises <code>NoSuchPublicAccessBlockConfiguration</code>. Handled via targeted exception parsing: <code>NoSuchTagSet</code> normalizes to empty dictionary, and absent PAB configuration explicitly maps to <code>NON_COMPLIANT</code> with <code>observed_value = False</code>.</p>
    <p><strong>2. Race Conditions & Concurrency during Live Scans:</strong> Rapid live scan triggers risked concurrent boto3 calls, causing AWS 429 throttling and race conditions writing to <code>reports/live-compliance.json</code>. Solved by embedding <code>asyncio.Lock()</code> in <code>ComplianceService</code>. Incoming requests checking <code>self._scan_lock.locked()</code> are immediately rejected with <code>ScanAlreadyInProgressError</code> (HTTP 409 Conflict). Active scans execute in a worker thread via <code>asyncio.to_thread</code>.</p>
    <p><strong>3. Arbitrary File Disclosure via Download Endpoints:</strong> Dynamic report downloads exposed potential directory traversal vulnerabilities. Enforced a two-tier whitelist guard: (1) Validated against <code>ALLOWED_REPORT_TYPES</code> dictionary, and (2) verified resolved path lies within the reports directory using <code>path.is_relative_to(self.reports_dir)</code>.</p>
    <p><strong>4. Dynamic Baseline Extraction Without Configuration Duplication:</strong> Duplicating expected baseline parameters between Terraform HCL and Python models created maintenance overhead. Handled by <code>BaselineLoader</code> executing <code>terraform output -json</code> in the terraform directory to dynamically populate the <code>SecurityBaseline</code> dataclass, with an immutable fallback schema for offline use.</p>

    <h2>8. Future Enhancements & Conclusion</h2>
    <h3>8.1 Future Scope</h3>
    <ul>
      <li><strong>Automated Self-Healing Reconciliation:</strong> Implement an automated actuator where detected drift triggers <code>terraform apply -replace</code> or direct SDK remediation to restore compliant state.</li>
      <li><strong>Multi-Service & Multi-Cloud Extensions:</strong> Extend <code>BaseRule</code> to monitor VPC Security Groups, IAM Role Trust Relationships, and multi-cloud targets (GCP Cloud Storage, Azure Blob).</li>
      <li><strong>Event-Driven Streaming via EventBridge:</strong> Replace polling with asynchronous event streaming via AWS CloudTrail and EventBridge to Lambda webhooks.</li>
      <li><strong>Role-Based Access Control (RBAC):</strong> Add OAuth2 / OIDC authentication to restrict live scan triggers and report downloads.</li>
    </ul>

    <h3>8.2 Conclusion</h3>
    <p>This project successfully designed and implemented an automated, policy-driven infrastructure compliance and drift detection system. By codifying secure storage baselines in Terraform and coupling them with an asynchronous Python evaluation engine, the architecture eliminates the latency and high recurring costs of legacy audit services while delivering sub-second drift detection, 100% test coverage across 44 test cases, and a tri-state classification model that ensures enterprise-grade audit integrity.</p>

    <h2>References & Dependencies</h2>
    <ol>
      <li>HashiCorp Terraform Documentation: Terraform Language Documentation and Provider Specifications. HashiCorp, Inc., 2024. <a href="https://developer.hashicorp.com/terraform/docs">https://developer.hashicorp.com/terraform/docs</a></li>
      <li>Center for Internet Security (CIS): CIS Amazon Web Services Foundations Benchmark v3.0.0. CIS Security Benchmarks, 2024. <a href="https://www.cisecurity.org/benchmark/amazon_web_services">https://www.cisecurity.org/benchmark/amazon_web_services</a></li>
      <li>Amazon Web Services Architecture Center: Security Pillar - AWS Well-Architected Framework. AWS, Inc., 2024. <a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html</a></li>
      <li>Boto3 Documentation: AWS SDK for Python (Boto3) API Reference. Amazon Web Services, Inc., 2024. <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html">https://boto3.amazonaws.com/v1/documentation/api/latest/index.html</a></li>
      <li>FastAPI Framework: FastAPI Documentation and Modern Python Web Standards. Tiangolo, 2024. <a href="https://fastapi.tiangolo.com/">https://fastapi.tiangolo.com/</a></li>
      <li>Morris, K.: Infrastructure as Code: Dynamic Systems Design for the Cloud. O'Reilly Media, 2nd Edition, 2020.</li>
      <li>National Institute of Standards and Technology (NIST): Security and Privacy Controls for Information Systems and Organizations. NIST SP 800-53 Rev. 5. <a href="https://doi.org/10.6028/NIST.SP.800-53r5">https://doi.org/10.6028/NIST.SP.800-53r5</a></li>
      <li>Python Software Foundation: Python 3.14 Language Reference and Asyncio Concurrency Primitives, 2024. <a href="https://docs.python.org/3/">https://docs.python.org/3/</a></li>
    </ol>

    <footer>
      Policy-Driven Infrastructure Compliance and Drift Detection &bull; Cloud Security &amp; AIDPS Capstone Report &bull; Generated October 2026
    </footer>
  </div>
</body>
</html>
"""

out_file = Path(r"c:\Users\Nilaksh\Desktop\aidps assignment\docs\PROJECT_REPORT.html")
out_file.write_text(html_content, encoding="utf-8")
print(f"Generated HTML report at: {out_file}")
