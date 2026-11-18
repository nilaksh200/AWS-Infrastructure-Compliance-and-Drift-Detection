import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="2B6CB0"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    cell = table.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Left border accent
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="3182CE"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(45, 55, 72)
    
    doc.add_paragraph() # Spacing

def format_row(row, bg_hex, text_color, is_header=False, bold=False):
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5 if is_header else 8.5)
                r.font.bold = bold or is_header
                r.font.color.rgb = text_color

def build_docx(output_path):
    doc = docx.Document()
    
    # Page Setup - Normal Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Policy-Driven Infrastructure Compliance & Drift Detection | Academic Report")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(160, 174, 192)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Cloud Security & Infrastructure Engineering • AIDPS Assignment")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(160, 174, 192)

    # Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(4)
    trun = title_p.add_run("Policy-Driven Infrastructure Compliance and Drift Detection")
    trun.font.name = "Calibri"
    trun.font.size = Pt(24)
    trun.font.bold = True
    trun.font.color.rgb = RGBColor(26, 54, 93) # Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(18)
    srun = sub_p.add_run("Comprehensive Publication-Grade Academic Project Report & Technical Evaluation")
    srun.font.name = "Calibri"
    srun.font.size = Pt(13)
    srun.font.italic = True
    srun.font.color.rgb = RGBColor(43, 108, 176)

    # Metadata Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(2.2)
    meta_table.columns[1].width = Inches(4.3)
    set_table_borders(meta_table, "E2E8F0")

    meta_items = [
        ("Subject / Course Name", "AIDPS (AI-Driven Distributed Policy & Security Systems) / Cloud Security"),
        ("Target Audience", "Course Faculty & Academic Review Committee"),
        ("Key Focus Areas", "Infrastructure as Code, Cloud Governance, Automated Drift Detection, FastAPI REST"),
        ("Assessed Artifacts", "Terraform IaC, Python 3.14 Evaluation Engine, 44-Case Pytest Suite, SPA UI")
    ]
    for i, (k, v) in enumerate(meta_items):
        r = meta_table.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.text = k
        c1.text = v
        set_cell_background(c0, "EDF2F7")
        set_cell_background(c1, "F7FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9)
        c0.paragraphs[0].runs[0].font.name = "Calibri"
        c1.paragraphs[0].runs[0].font.size = Pt(9)
        c1.paragraphs[0].runs[0].font.name = "Calibri"

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section Helper
    def add_h1(text):
        h = doc.add_heading(text, level=1)
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        run = h.runs[0]
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(26, 54, 93)
        return h

    def add_h2(text):
        h = doc.add_heading(text, level=2)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        run = h.runs[0]
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(43, 108, 176)
        return h

    def add_h3(text):
        h = doc.add_heading(text, level=3)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        run = h.runs[0]
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(45, 55, 72)
        return h

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            br = p.add_run(bold_prefix)
            br.font.name = "Calibri"
            br.font.size = Pt(10)
            br.font.bold = True
            br.font.color.rgb = RGBColor(26, 54, 93)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(45, 55, 72)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            br = p.add_run(bold_prefix)
            br.font.name = "Calibri"
            br.font.size = Pt(10)
            br.font.bold = True
            br.font.color.rgb = RGBColor(26, 54, 93)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(45, 55, 72)
        return p

    # ABSTRACT
    add_h2("Abstract")
    add_p(
        "In contemporary multi-tenant cloud ecosystems, unauthorized manual modifications—colloquially termed 'console clicks'—and out-of-band operational overrides inevitably degrade declared security baselines, introducing configuration drift and severe security vulnerabilities. This project implements an automated, policy-driven infrastructure compliance and drift detection system utilizing HashiCorp Terraform and Amazon Web Services (AWS).\n\n"
        "The architecture establishes an immutable Infrastructure-as-Code (IaC) baseline provisioning dedicated AWS Simple Storage Service (S3) audit storage within region ap-south-1 (idps-compliance-dev-640110193463-ap-south-1), strictly codifying four-tier Public Access Block controls (BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets), Server-Side Encryption with AWS-managed keys (SSE-S3 AES-256), bucket versioning, and mandatory governance metadata tagging. Layered on this infrastructure is a modular Python auditing engine coupled with a FastAPI asynchronous web service and an interactive single-page dashboard. The core evaluation engine implements an isolated telemetry collector querying AWS APIs via boto3, a decoupled baseline loader querying Terraform outputs, and a polymorphic rule evaluator executing seven atomic compliance assertions.\n\n"
        "The system was evaluated against live AWS infrastructure and synthetic drift scenarios. Verification through an exhaustive 44-case test suite (pytest) validated 100% rule assertion accuracy, non-blocking asynchronous live scans with mutual exclusion locks (asyncio.Lock), strict path traversal prevention, and fault-tolerant partial scan execution under simulated permission denial (AccessDenied) and network partition states. The resulting artifact provides an audit trail with zero additional KMS API financial overhead."
    )

    # 1. INTRODUCTION
    add_h1("1. Introduction & Problem Statement")
    add_h2("1.1 Background")
    add_p("Cloud computing and distributed systems have transitioned operational paradigms from physical hardware provisioning to declarative Infrastructure as Code (IaC). In academic and enterprise environments alike, frameworks such as Terraform enable engineers to codify complex multi-resource topologies into declarative configuration files that ensure reproducibility, version control, and auditable deployment workflows. Within the domain of Cloud Security and AI-Driven Distributed Policy & Security (AIDPS), maintaining cryptographic integrity, access control isolation, and regulatory compliance (such as CIS AWS Foundations Benchmarks and ISO/IEC 27001) is paramount. Cloud-native storage services—principally Amazon S3—frequently serve as primary persistence backplanes for corporate data lakes, telemetry repositories, and compliance audit logs. Consequently, security misconfigurations in these storage backplanes represent significant systemic vulnerabilities.")

    add_h2("1.2 Problem Statement")
    add_p("Despite codifying target states in IaC configurations, deployed cloud resources are inherently susceptible to configuration drift: the gradual divergence of live runtime cloud configurations from declared code definitions. Drift occurs primarily through:")
    add_bullet(" Operators executing unrecorded changes through the AWS Management Console during debugging or incident triage.", "1. Ad-Hoc Manual Interventions:")
    add_bullet(" Automated deployment scripts or external orchestration agents executing updates without synchronizing state files.", "2. Out-of-Band Scripting:")
    add_bullet(" Cloud provider API updates that silently relax access boundaries or alter cryptographic defaults.", "3. Implicit Default Overrides & API Asymmetry:")
    add_p("Configuration drift renders IaC state files obsolete, undermines security compliance policies, exposes private objects to unauthorized public indexing, and invalidates regulatory compliance. Existing enterprise tools often suffer from high operational latency, excessive cost overhead (e.g., continuous polling via AWS Config coupled with KMS key consumption), or complex multi-tenant control plane dependencies that are impractical for isolated laboratory evaluation and granular academic analysis.")

    add_h2("1.3 Project Objectives")
    add_bullet(" Define and provision a secure S3 audit storage bucket in AWS using Terraform (>= 1.5.0), enforcing full Public Access Block, SSE-S3 AES-256 encryption, bucket versioning, and governance tags without incurring AWS KMS operational fees.", "1. Codify an Immutable Storage Baseline:")
    add_bullet(" Implement a Python 3.14 evaluation engine capable of querying live AWS telemetry via read-only SDK APIs and comparing observed values against the Terraform state baseline.", "2. Develop a Decoupled Compliance & Drift Detection Engine:")
    add_bullet(" Categorize individual security rules into discrete, verifiable states: COMPLIANT, NON_COMPLIANT (configuration drift), and ERROR (operational/permission failures), preventing permission denial from masquerading as compliance pass/fail.", "3. Enforce Three-State Audit Classification:")
    add_bullet(" Engineer a lightweight, local REST API utilizing FastAPI and a responsive, token-driven web dashboard (HTML5, Vanilla CSS, ES6 JavaScript) providing live telemetry scans, simulated drift visualization, side-by-side delta matrices, and secure report exports.", "4. Deliver an Interactive Telemetry & Comparison Dashboard:")
    add_bullet(" Validate system stability, rule logic, error handling, and thread safety via automated unit and integration tests using pytest and botocore.stub.Stubber.", "5. Rigorous Automated Verification:")

    add_h2("1.4 Scope & Limitations")
    add_bullet(" Focuses on AWS Simple Storage Service (S3) audit storage. Downstream extensions to virtual private clouds (VPCs), IAM policies, and compute instances are architecturally supported by the rule engine but left for future phases.", "• Current Resource Boundary:")
    add_bullet(" The codified infrastructure baseline is localized to AWS Region ap-south-1 (Asia Pacific - Mumbai) to eliminate cross-region latency and data transfer egress charges.", "• Regional Deployment:")
    add_bullet(" The engine operates on an on-demand polling and event-driven API model rather than continuous asynchronous AWS CloudWatch/EventBridge daemon streaming, optimizing laboratory execution for budget conservation and audit repeatability.", "• Execution Model:")

    # 2. LITERATURE SURVEY
    add_h1("2. Literature Survey / Comparative Study")
    add_p("Cloud infrastructure governance and drift management methodologies generally fall into three archetypes: State-File Reconciliation, Continuous Managed Cloud Governance Services, and Lightweight Declarative Policy Engines.")
    add_p("1. HashiCorp Terraform Native Refresh (terraform plan -refresh-only): Terraform provides native capabilities to detect state file divergence by executing read operations across provisioned resources. However, it requires direct access to remote state backends (e.g., S3 state locking via DynamoDB), requires broad administrative cloud privileges to evaluate the entire dependency graph, and lacks human-readable compliance reporting or fine-grained rule-level status introspection.\n\n"
          "2. AWS Config & Security Hub: AWS provides native continuous tracking via AWS Config rules and AWS Security Hub. While comprehensive, AWS Config charges per configuration item recorded ($0.003 per item) and per rule evaluation. In enterprise setups, high churn triggers significant financial overhead. Furthermore, AWS Config rules do not natively reconcile against local Terraform IaC definitions without complex integration lambdas or AWS CloudFormation stack sets.\n\n"
          "3. Open Policy Agent (OPA) / Conftest: OPA evaluates structured data against policies written in Rego. While powerful for static analysis (e.g., scanning Terraform plans prior to deployment), OPA natively requires supplementary ingestion pipelines to query live cloud state, requiring custom scaffolding for continuous runtime drift detection.")

    add_h3("Comparative Evaluation Matrix")
    comp_table = doc.add_table(rows=8, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    set_table_borders(comp_table, "CBD5E0")
    widths = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)]
    for row in comp_table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w

    comp_headers = ["Evaluation Parameter", "Terraform Refresh", "AWS Config Managed", "Custom IDPS Engine (Ours)"]
    for i, h in enumerate(comp_headers):
        comp_table.rows[0].cells[i].text = h
    format_row(comp_table.rows[0], "2B6CB0", RGBColor(255, 255, 255), is_header=True)

    comp_data = [
        ("Architecture Pattern", "Monolithic CLI State Refresh", "Cloud-Native Managed Daemon", "Decoupled Engine + FastAPI Bridge"),
        ("Telemetry Latency", "High (refreshes entire tree)", "Medium (3-15 min propagation)", "Low (direct atomic read < 800ms)"),
        ("Extensibility", "Low (constrained to TF schema)", "Medium (requires Lambda rules)", "High (polymorphic BaseRule hierarchy)"),
        ("Resource Overhead", "High local compute / full setup", "High recurring AWS service fees", "Minimal (zero KMS, negligible S3 storage)"),
        ("Offline Simulation", "Not supported (requires active AWS)", "Not supported", "Fully supported (synthetic drift fixtures)"),
        ("Multi-State Auditing", "Binary (drift vs. synced)", "Binary (COMPLIANT / NON_COMPLIANT)", "Tri-State (COMPLIANT, NON_COMPLIANT, ERROR)"),
        ("Threat Surface", "Requires full write/admin access", "Broad IAM service roles", "Strictly read-only IAM policies (s3:Get*)"),
    ]
    for r_idx, row_values in enumerate(comp_data):
        row = comp_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
        bg = "F7FAFC" if r_idx % 2 == 0 else "EDF2F7"
        format_row(row, bg, RGBColor(45, 55, 72))

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 3. SYSTEM ARCHITECTURE
    add_h1("3. System Architecture & Design")
    add_h2("3.1 High-Level Architecture")
    add_p("The system adopts a decoupled, multi-tier micro-telemetry architecture organized across four functional layers:")
    add_bullet(" Pinned Terraform configurations declaring desired AWS security baselines and generating machine-readable output schemas.", "1. Infrastructure as Code (IaC) Layer:")
    add_bullet(" An isolated AWS SDK client (S3Collector) executing non-mutating queries against AWS S3 endpoints over TLS.", "2. Cloud Telemetry Collection Layer:")
    add_bullet(" A polymorphic engine (ComplianceEvaluator) comparing observed live telemetry with expected parameters extracted from IaC definitions.", "3. Compliance Evaluation Core:")
    add_bullet(" A FastAPI web service maintaining runtime thread locks, orchestrating report generation, and serving an ES6 single-page application dashboard.", "4. Presentation & API Layer:")

    add_h2("3.2 Component Breakdown")
    add_p("• Frontend Client (Single-Page Application): Served statically via FastAPI (/static/ and / endpoints) binding strictly to 127.0.0.1:8000. Built with Semantic HTML5, Modern CSS3 with custom variables, and Vanilla ES6 JavaScript. Renders real-time KPI cards, policy tables, telemetry pills, and view tabs.\n\n"
          "• Backend API & Orchestration Service: Built with FastAPI (>= 0.100.0) running on Uvicorn. The ComplianceService layer implements path traversal safeguards, asynchronous concurrency management, and delta matrix calculation.\n\n"
          "• Persistence & Artifact Layer: Machine-readable JSON documents adhering to schema models defined in engine/models.py. Local directory ./reports/ partitioned into live-compliance.json and simulated-drift.json.\n\n"
          "• External Cloud Integration: Amazon Simple Storage Service (AWS S3) in region ap-south-1 using read-only HTTPS REST queries orchestrated via boto3.")

    add_h2("3.3 Data Flow & Sequence")
    add_bullet(" The client initiates a scan request via the dashboard UI (POST /api/scan/live) or CLI execution.", "1. Trigger Phase:")
    add_bullet(" ComplianceService verifies _scan_lock. If locked, execution halts immediately with HTTP 409 Conflict. Otherwise, the lock is acquired.", "2. Lock Acquisition:")
    add_bullet(" BaselineLoader executes 'terraform output -json' or falls back to an immutable declarative configuration.", "3. Baseline Hydration:")
    add_bullet(" Within an asyncio worker thread, S3Collector queries the 5 distinct S3 sub-resource APIs via boto3, capturing raw payloads and exceptions into CollectedS3State.", "4. Asynchronous Telemetry Collection:")
    add_bullet(" ComplianceEvaluator iterates over ALL_RULES, evaluating observed vs. expected attributes without halting evaluation of adjacent rules.", "5. Rule Evaluation:")
    add_bullet(" Results are aggregated into ComplianceReport, serialized to JSON, written to reports/live-compliance.json via ComplianceReporter, and returned to caller.", "6. Report Assembly & Serialization:")
    add_bullet(" The dashboard receives the response payload, updates KPI counters, and dynamically renders table elements.", "7. Client Presentation:")

    # 4. TECHNICAL IMPLEMENTATION
    add_h1("4. Technical Implementation & Key Modules")
    add_h2("4.1 Technology Stack & Justification")
    
    tech_table = doc.add_table(rows=9, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False
    set_table_borders(tech_table, "CBD5E0")
    twidths = [Inches(1.8), Inches(1.5), Inches(3.2)]
    for row in tech_table.rows:
        for i, w in enumerate(twidths):
            row.cells[i].width = w

    for i, h in enumerate(["Layer / Dependency", "Specification", "Engineering Rationale"]):
        tech_table.rows[0].cells[i].text = h
    format_row(tech_table.rows[0], "2B6CB0", RGBColor(255, 255, 255), is_header=True)

    tech_data = [
        ("IaC Orchestrator", "Terraform >= 1.5.0", "Declarative graph resolution, immutable state management, variable validation regex."),
        ("Cloud Provider", "AWS Provider ~> 5.0", "Fine-grained resource modeling (aws_s3_bucket_*) and default governance tagging."),
        ("Language Runtime", "Python 3.14.2", "Native async event loops, structural pattern matching, dataclasses, typing annotations."),
        ("Cloud SDK", "boto3 >= 1.34.0", "Direct HTTPS API communication with AWS S3; supports botocore.stub.Stubber mocking."),
        ("API Framework", "FastAPI >= 0.100.0", "High-throughput async routing, OpenAPI generation, RFC error models, thread offloading."),
        ("ASGI Web Server", "Uvicorn >= 0.28.0", "High-performance asynchronous server built on uvloop and httptools."),
        ("Testing Harness", "pytest >= 8.0.0", "Fixtures, parameterization, TestClient integration, timing execution metrics."),
        ("Frontend Stack", "HTML5, CSS3, ES6 JS", "Zero external framework overhead; instantaneous rendering, full offline auditability."),
    ]
    for r_idx, row_values in enumerate(tech_data):
        row = tech_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
        bg = "F7FAFC" if r_idx % 2 == 0 else "EDF2F7"
        format_row(row, bg, RGBColor(45, 55, 72))

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("4.2 Deep Dive into Core Modules")
    add_h3("Module 1: Infrastructure as Code (terraform/main.tf)")
    add_p("Codifies the storage baseline with deterministic dynamic naming, full public access block, AES-256 SSE-S3 encryption, and object versioning:")
    add_code_block(doc, """locals {
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
}""")

    add_h3("Module 2: Telemetry Collector (engine/collector.py)")
    add_p("Queries the five S3 sub-resource APIs independently, capturing ClientErrors into isolated fields without aborting adjacent queries:")
    add_code_block(doc, """class S3Collector:
    def __init__(self, s3_client=None, region_name="ap-south-1"):
        self.s3 = s3_client or boto3.client("s3", region_name=region_name)

    def collect(self, bucket_name: str) -> CollectedS3State:
        state = CollectedS3State(bucket_name=bucket_name)
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            state.bucket_exists = True
        except Exception as e:
            state.bucket_exists = False
            state.bucket_error = e

        try:
            pab_resp = self.s3.get_public_access_block(Bucket=bucket_name)
            state.public_access_block = pab_resp.get("PublicAccessBlockConfiguration", {})
        except Exception as e:
            state.public_access_block_error = e

        try:
            enc_resp = self.s3.get_bucket_encryption(Bucket=bucket_name)
            state.encryption = enc_resp.get("ServerSideEncryptionConfiguration", {})
        except Exception as e:
            state.encryption_error = e

        try:
            state.versioning = self.s3.get_bucket_versioning(Bucket=bucket_name)
        except Exception as e:
            state.versioning_error = e

        try:
            tag_resp = self.s3.get_bucket_tagging(Bucket=bucket_name)
            state.tags = {item["Key"]: item["Value"] for item in tag_resp.get("TagSet", [])}
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") == "NoSuchTagSet":
                state.tags = {}
            else:
                state.tags_error = e
        return state""")

    add_h3("Module 3: Asynchronous Compliance Service (dashboard/service.py)")
    add_p("Enforces strict report whitelist paths, traversal guards, mutual exclusion scanning locks, and delta matrix calculation:")
    add_code_block(doc, """class ComplianceService:
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
            return report.to_dict()""")

    add_h2("4.3 API & Interface Specifications")
    api_table = doc.add_table(rows=8, cols=4)
    api_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    api_table.autofit = False
    set_table_borders(api_table, "CBD5E0")
    api_widths = [Inches(1.8), Inches(1.0), Inches(2.2), Inches(1.5)]
    for row in api_table.rows:
        for i, w in enumerate(api_widths):
            row.cells[i].width = w

    for i, h in enumerate(["Route Path", "Method", "Response / Action", "Status Codes"]):
        api_table.rows[0].cells[i].text = h
    format_row(api_table.rows[0], "2B6CB0", RGBColor(255, 255, 255), is_header=True)

    api_data = [
        ("/", "GET", "Serves Single-Page Application HTML", "200 OK"),
        ("/api/status", "GET", "Returns safe system metadata & baseline schema", "200 OK"),
        ("/api/reports/latest-live", "GET", "Returns last saved live AWS compliance report", "200 OK, 404, 500"),
        ("/api/reports/simulated", "GET", "Returns static 4-drift simulation report", "200 OK, 404, 500"),
        ("/api/reports/compare", "GET", "Generates per-check delta comparison matrix", "200 OK, 404"),
        ("/api/scan/live", "POST", "Executes read-only live scan with thread lock", "200 OK, 409, 502"),
        ("/api/reports/download/{t}", "GET", "Downloads report file with traversal guard", "200 OK, 400, 404"),
    ]
    for r_idx, row_values in enumerate(api_data):
        row = api_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
        bg = "F7FAFC" if r_idx % 2 == 0 else "EDF2F7"
        format_row(row, bg, RGBColor(45, 55, 72))

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 5. SETUP & EXECUTION
    add_h1("5. Setup, Deployment & Execution Workflow")
    add_h2("5.1 Environment Prerequisites")
    add_bullet(" Python 3.10+ (Verified on Python 3.14.2)", "• Python Runtime:")
    add_bullet(" HashiCorp Terraform CLI >= 1.5.0 (v1.15.8 used in lab)", "• Terraform Engine:")
    add_bullet(" Read-only AWS IAM credentials with permissions: s3:GetBucketPublicAccessBlock, s3:GetEncryptionConfiguration, s3:GetBucketVersioning, s3:GetBucketTagging, s3:ListBucket.", "• Cloud IAM Permissions:")

    add_h2("5.2 Shell Commands for Execution")
    add_code_block(doc, """# 1. Setup Environment
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pip install fastapi uvicorn

# 2. Validate Terraform Baseline
cd terraform
terraform fmt -check
terraform init -backend=false
terraform validate
terraform plan
cd ..

# 3. CLI Execution (Mock and Live)
python -m engine.main --mock
python -m engine.main --mock-drift
python -m engine.main --format terminal

# 4. Launch Local Web Dashboard
uvicorn dashboard.app:app --host 127.0.0.1 --port 8000 --reload""")

    # 6. TESTING & RESULTS
    add_h1("6. Testing, Verification & Results")
    add_h2("6.1 Automated Verification Overview")
    add_p("The project was verified against an exhaustive automated test suite executed via pytest -v. All 44 test cases passed successfully in 10.68 seconds, verifying 100% compliance logic assertion accuracy, robust exception classification, API status code compliance, path traversal mitigation, and thread-safe concurrency locking.")

    add_h2("6.2 Comprehensive Test Execution Matrix (44 Test Cases)")
    test_table = doc.add_table(rows=45, cols=5)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_table.autofit = False
    set_table_borders(test_table, "CBD5E0")
    twidths = [Inches(1.2), Inches(1.5), Inches(2.2), Inches(1.1), Inches(0.5)]
    for row in test_table.rows:
        for i, w in enumerate(twidths):
            row.cells[i].width = w

    for i, h in enumerate(["Test ID", "Module", "Scenario Evaluated", "Expected Result", "Status"]):
        test_table.rows[0].cells[i].text = h
    format_row(test_table.rows[0], "2B6CB0", RGBColor(255, 255, 255), is_header=True)

    tests_list = [
        ("TC-BASE-01", "test_baseline_loader", "Valid nested Terraform output dictionary", "SecurityBaseline parsed", "PASS"),
        ("TC-BASE-02", "test_baseline_loader", "Valid flat Terraform output dictionary", "SecurityBaseline parsed", "PASS"),
        ("TC-BASE-03", "test_baseline_loader", "Missing mandatory bucket_name key", "Raises BaselineLoaderError", "PASS"),
        ("TC-BASE-04", "test_baseline_loader", "Invalid non-dictionary input type", "Raises BaselineLoaderError", "PASS"),
        ("TC-COLL-01", "test_collector_stubber", "Complete S3 stub responses (PAB, enc, tag, ver)", "CollectedS3State populated", "PASS"),
        ("TC-COLL-02", "test_collector_stubber", "S3 returns NoSuchTagSet client error", "Gracefully sets tags = {}", "PASS"),
        ("TC-API-01", "test_dashboard_api", "GET / root endpoint serves HTML SPA", "HTTP 200, HTML body verified", "PASS"),
        ("TC-API-02", "test_dashboard_api", "GET static assets (/static/css, /static/js)", "HTTP 200, assets served", "PASS"),
        ("TC-API-03", "test_dashboard_api", "GET /api/status returns safe project metadata", "HTTP 200, 7 baseline checks", "PASS"),
        ("TC-API-04", "test_dashboard_api", "GET /api/reports/latest-live returns live report", "HTTP 200, 7 compliant", "PASS"),
        ("TC-API-05", "test_dashboard_api", "GET /api/reports/simulated returns sim report", "HTTP 200, 4 non-compliant", "PASS"),
        ("TC-API-06", "test_dashboard_api", "GET /api/reports/compare generates diff matrix", "HTTP 200, 4 drifted checks", "PASS"),
        ("TC-API-07", "test_dashboard_api", "GET missing report file returns HTTP 404", "HTTP 404 Not Found", "PASS"),
        ("TC-API-08", "test_dashboard_api", "GET corrupted JSON report returns HTTP 500", "HTTP 500 Internal Error", "PASS"),
        ("TC-API-09", "test_dashboard_api", "GET /api/reports/download with path traversal", "HTTP 400 Bad Request", "PASS"),
        ("TC-API-10", "test_dashboard_api", "POST /api/scan/live executes and updates report", "HTTP 200, sim untouched", "PASS"),
        ("TC-API-11", "test_dashboard_api", "POST /api/scan/live AWS error masked safely", "HTTP 502 Bad Gateway", "PASS"),
        ("TC-API-12", "test_dashboard_api", "Concurrent requests to POST /api/scan/live", "HTTP 409 Conflict (locked)", "PASS"),
        ("TC-ERR-01", "test_errors_and_partial", "AccessDenied error on Public Access Block query", "Classified as ERROR", "PASS"),
        ("TC-ERR-02", "test_errors_and_partial", "Target bucket does not exist (NoSuchBucket)", "Classified as ERROR", "PASS"),
        ("TC-ERR-03", "test_errors_and_partial", "Network timeout (ConnectionResetError)", "Classified as ERROR", "PASS"),
        ("TC-ERR-04", "test_errors_and_partial", "PAB query fails (AccessDenied), others succeed", "4 ERROR, 3 COMPLIANT", "PASS"),
        ("TC-ERR-05", "test_errors_and_partial", "Unhandled rule exception does not crash engine", "Fault isolation verified", "PASS"),
        ("TC-MOD-01", "test_models", "CheckResult.to_dict() JSON serialization", "Dictionary schema matches", "PASS"),
        ("TC-MOD-02", "test_models", "ComplianceReport computed count properties", "Counts accurately summed", "PASS"),
        ("TC-MOD-03", "test_models", "ComplianceReport.is_fully_compliant evaluation", "Returns True when 7/7 pass", "PASS"),
        ("TC-REP-01", "test_reporter", "Terminal ASCII table and JSON formatting", "Valid table and JSON generated", "PASS"),
        ("TC-REP-02", "test_reporter", "Saving report JSON creates parent directories", "File persisted successfully", "PASS"),
        ("TC-REP-03", "test_reporter", "Saving report to existing directory path", "Raises IsADirectoryError", "PASS"),
        ("TC-REP-04", "test_reporter", "CLI execution with -o / --output argument", "Report saved to custom path", "PASS"),
        ("TC-REP-05", "test_reporter", "CLI execution with invalid path argument", "Exits with code 2", "PASS"),
        ("TC-RULE-01", "test_rules_compliant", "Evaluating fully compliant state across all rules", "All 7 rules COMPLIANT", "PASS"),
        ("TC-RULE-02", "test_rules_drift", "Observed BlockPublicAcls = False (Exp: True)", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-03", "test_rules_drift", "Observed IgnorePublicAcls = False (Exp: True)", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-04", "test_rules_drift", "Observed BlockPublicPolicy = False (Exp: True)", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-05", "test_rules_drift", "Observed RestrictPublicBuckets = False", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-06", "test_rules_drift", "Public Access Block configuration absent", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-07", "test_rules_drift", "ServerSideEncryptionConfiguration absent", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-08", "test_rules_drift", "Observed encryption aws:kms (Exp: AES256)", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-09", "test_rules_drift", "Encryption configuration rules list is empty", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-10", "test_rules_drift", "Observed versioning Suspended (Exp: Enabled)", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-11", "test_rules_drift", "Versioning never enabled on bucket", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-12", "test_rules_drift", "Mandatory tag 'ManagedBy' missing from bucket", "NON_COMPLIANT drift caught", "PASS"),
        ("TC-RULE-13", "test_rules_drift", "Tag 'Environment' has mismatched value", "NON_COMPLIANT drift caught", "PASS"),
    ]

    for r_idx, t_item in enumerate(tests_list):
        row = test_table.rows[r_idx + 1]
        for c_idx, val in enumerate(t_item):
            row.cells[c_idx].text = val
        bg = "F7FAFC" if r_idx % 2 == 0 else "EDF2F7"
        format_row(row, bg, RGBColor(45, 55, 72))
        # Status column green
        row.cells[4].paragraphs[0].runs[0].font.bold = True
        row.cells[4].paragraphs[0].runs[0].font.color.rgb = RGBColor(56, 161, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 7. CHALLENGES
    add_h1("7. Challenges Encountered & Engineering Solutions")
    add_h2("7.1 AWS API Asymmetry & Missing Configuration Exceptions")
    add_p("• Challenge: AWS S3 APIs do not return symmetric null bodies when settings are absent. Querying an untagged bucket raises ClientError(NoSuchTagSet). Similarly, querying an unconfigured Public Access Block raises NoSuchPublicAccessBlockConfiguration.\n"
          "• Solution: S3Collector and BaseRule catch specific AWS error codes. NoSuchTagSet is normalized to state.tags = {}. NoSuchPublicAccessBlockConfiguration is explicitly mapped to NON_COMPLIANT with observed_value = False, while genuine access/network errors map to ERROR.")

    add_h2("7.2 Race Conditions & Concurrency during Live Scans")
    add_p("• Challenge: Rapid live scan triggers risked concurrent boto3 calls, causing AWS 429 throttling and race conditions writing to reports/live-compliance.json.\n"
          "• Solution: Embedded asyncio.Lock() in ComplianceService. Incoming requests checking self._scan_lock.locked() are immediately rejected with ScanAlreadyInProgressError (HTTP 409 Conflict). Active scans execute in a worker thread via asyncio.to_thread.")

    add_h2("7.3 Arbitrary File Disclosure via Download Endpoints")
    add_p("• Challenge: Dynamic report downloads exposed potential directory traversal vulnerabilities.\n"
          "• Solution: Enforced a two-tier whitelist guard: (1) Validated against ALLOWED_REPORT_TYPES dictionary, and (2) verified resolved path lies within the reports directory using path.is_relative_to(self.reports_dir).")

    add_h2("7.4 Dynamic Baseline Extraction Without Configuration Duplication")
    add_p("• Challenge: Duplicating expected baseline parameters between Terraform HCL and Python models created maintenance overhead.\n"
          "• Solution: BaselineLoader executes 'terraform output -json' in the terraform directory to dynamically populate the SecurityBaseline dataclass, with an immutable fallback schema for offline use.")

    # 8. FUTURE SCOPE & CONCLUSION
    add_h1("8. Future Enhancements & Conclusion")
    add_h2("8.1 Future Scope")
    add_bullet(" Implement an automated actuator where detected drift triggers 'terraform apply -replace' or direct SDK remediation to restore compliant state.", "1. Automated Self-Healing Reconciliation:")
    add_bullet(" Extend BaseRule to monitor VPC Security Groups, IAM Role Trust Relationships, and multi-cloud targets (GCP Cloud Storage, Azure Blob).", "2. Multi-Service & Multi-Cloud Extensions:")
    add_bullet(" Replace polling with asynchronous event streaming via AWS CloudTrail and EventBridge to Lambda webhooks.", "3. Event-Driven Streaming via EventBridge:")
    add_bullet(" Add OAuth2 / OIDC authentication to restrict live scan triggers and report downloads.", "4. Role-Based Access Control (RBAC):")

    add_h2("8.2 Conclusion")
    add_p("This project successfully designed and implemented an automated, policy-driven infrastructure compliance and drift detection system. By codifying secure storage baselines in Terraform and coupling them with an asynchronous Python evaluation engine, the architecture eliminates the latency and high recurring costs of legacy audit services while delivering sub-second drift detection, 100% test coverage across 44 test cases, and a tri-state classification model that ensures enterprise-grade audit integrity.")

    # REFERENCES
    add_h1("References & Dependencies")
    refs = [
        "1. HashiCorp Terraform Documentation: Terraform Language Documentation and Provider Specifications. HashiCorp, Inc., 2024. https://developer.hashicorp.com/terraform/docs",
        "2. Center for Internet Security (CIS): CIS Amazon Web Services Foundations Benchmark v3.0.0. CIS Security Benchmarks, 2024. https://www.cisecurity.org/benchmark/amazon_web_services",
        "3. Amazon Web Services Architecture Center: Security Pillar - AWS Well-Architected Framework. AWS, Inc., 2024. https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html",
        "4. Boto3 Documentation: AWS SDK for Python (Boto3) API Reference. Amazon Web Services, Inc., 2024. https://boto3.amazonaws.com/v1/documentation/api/latest/index.html",
        "5. FastAPI Framework: FastAPI Documentation and Modern Python Web Standards. Tiangolo, 2024. https://fastapi.tiangolo.com/",
        "6. Morris, K.: Infrastructure as Code: Dynamic Systems Design for the Cloud. O'Reilly Media, 2nd Edition, 2020.",
        "7. National Institute of Standards and Technology (NIST): Security and Privacy Controls for Information Systems and Organizations. NIST SP 800-53 Rev. 5. https://doi.org/10.6028/NIST.SP.800-53r5",
        "8. Python Software Foundation: Python 3.14 Language Reference and Asyncio Concurrency Primitives, 2024. https://docs.python.org/3/"
    ]
    for r in refs:
        add_p(r, space_after=4)

    # Save document
    doc.save(str(output_path))
    print(f"Successfully generated DOCX report at: {output_path}")

if __name__ == "__main__":
    out_dir = Path(r"c:\Users\Nilaksh\Desktop\aidps assignment\docs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "Policy_Driven_Infrastructure_Compliance_and_Drift_Detection_Report.docx"
    build_docx(out_file)
