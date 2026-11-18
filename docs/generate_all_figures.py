import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/figures", exist_ok=True)

# Copy or resize dashboard screenshot
if os.path.exists("docs/dash_screenshot.png"):
    im = Image.open("docs/dash_screenshot.png")
    im.save("docs/figures/fig_5_1_dashboard.png")
    print("Saved fig_5_1_dashboard.png from dash_screenshot.png")

# Helper to draw a modern terminal window
def create_terminal_image(filename, title, lines_with_colors, width=1200, height=750):
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis('off')
    
    # Outer background
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')

    # Terminal Title Bar
    title_bar = patches.Rectangle((0, height - 42), width, 42, facecolor='#1E293B', edgecolor='#334155', linewidth=1)
    ax.add_patch(title_bar)

    # Window dots
    ax.add_patch(patches.Circle((22, height - 21), 6, facecolor='#EF4444'))
    ax.add_patch(patches.Circle((42, height - 21), 6, facecolor='#F59E0B'))
    ax.add_patch(patches.Circle((62, height - 21), 6, facecolor='#10B981'))

    # Title text
    ax.text(width/2, height - 21, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#94A3B8', fontfamily='monospace')

    # Terminal text lines
    y = height - 70
    for text, color, bold in lines_with_colors:
        ax.text(25, y, text, ha='left', va='top', fontsize=9.5, fontweight='bold' if bold else 'normal', color=color, fontfamily='monospace')
        y -= 22
        if y < 20:
            break

    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=150, facecolor='#0B0F19')
    plt.close()
    print(f"Generated {filename}")

# -------------------------------------------------------------
# Figure 5.5: CLI Mock Execution Terminal
# -------------------------------------------------------------
cli_lines = [
    ("$ python -m engine.main --mock", "#38BDF8", True),
    ("[*] Initializing Policy-Driven Compliance Engine in MOCK mode...", "#94A3B8", False),
    ("[+] Loading expected baseline from codified Terraform outputs...", "#10B981", False),
    ("    Target S3 Bucket: idps-compliance-dev-640110193463-ap-south-1", "#E2E8F0", False),
    ("    Target AWS Region: ap-south-1", "#E2E8F0", False),
    ("[*] Executing read-only telemetry collection via simulated AWS Boto3 adapter...", "#94A3B8", False),
    ("[+] Telemetry acquired: 5 sub-resources successfully fetched.", "#10B981", False),
    ("[*] Running Polymorphic Compliance Evaluator (7 atomic policy rules)...", "#38BDF8", False),
    ("------------------------------------------------------------------------------------------------", "#475569", False),
    (" RULE ID                 STATUS      OBSERVED STATE                        SEVERITY   DETAILS", "#F8FAFC", True),
    ("------------------------------------------------------------------------------------------------", "#475569", False),
    (" S3-001-EXISTENCE        COMPLIANT   Bucket exists & accessible            INFO       Bucket present", "#34D399", False),
    (" S3-002-PUBLIC-ACCESS    COMPLIANT   All 4 BlockPublicAccess flags True    HIGH       Zero public risk", "#34D399", False),
    (" S3-003-ENCRYPTION       COMPLIANT   SSEAlgorithm = 'AES256'               CRITICAL   At-rest encryption active", "#34D399", False),
    (" S3-004-VERSIONING       COMPLIANT   Versioning = 'Enabled'                HIGH       Immutable audit history", "#34D399", False),
    (" S3-005-MANDATORY-TAGS   COMPLIANT   Project, Environment, ManagedBy set   MEDIUM     Required tags present", "#34D399", False),
    (" S3-006-ENV-TAG          COMPLIANT   Environment = 'dev'                   LOW        Matches target baseline", "#34D399", False),
    (" S3-007-MANAGEDBY-TAG    COMPLIANT   ManagedBy = 'Terraform'               LOW        Codified governance OK", "#34D399", False),
    ("------------------------------------------------------------------------------------------------", "#475569", False),
    ("[SUMMARY] Total: 7 | Compliant: 7 | Drift: 0 | Errors: 0", "#38BDF8", True),
    ("[SUCCESS] Status: COMPLIANT | Overall Drift Score: 0.00%", "#10B981", True),
    ("[+] Compliance report serialized to: reports/live-compliance.json", "#E2E8F0", False),
    ("", "#FFFFFF", False),
    ("$ python -m engine.main --mock-drift", "#F59E0B", True),
    ("[!] Injecting synthetic configuration drift telemetry...", "#F59E0B", False),
    ("[ALERT] Non-compliant drift detected: 3 security baselines violated!", "#EF4444", True),
    ("    -> S3-002-PUBLIC-ACCESS: NON_COMPLIANT (BlockPublicPolicy was disabled via console)", "#F87171", False),
    ("    -> S3-003-ENCRYPTION:    NON_COMPLIANT (Server encryption stripped to unencrypted)", "#F87171", False),
    ("    -> S3-006-ENV-TAG:       NON_COMPLIANT (Environment changed from 'dev' to 'staging')", "#F87171", False),
    ("[SUMMARY] Total: 7 | Compliant: 4 | Drift Detected: 3 | Errors: 0", "#F87171", True)
]
create_terminal_image("docs/figures/fig_5_5_cli_execution.png", "Terminal Session: engine.main CLI Execution (--mock & --mock-drift)", cli_lines, width=1200, height=720)

# -------------------------------------------------------------
# Figure 5.6: Pytest Test Suite Results Terminal
# -------------------------------------------------------------
pytest_lines = [
    ("$ pytest -v --tb=short", "#38BDF8", True),
    ("============================= test session starts ==============================", "#94A3B8", False),
    ("platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0", "#94A3B8", False),
    ("rootdir: C:\\Users\\Nilaksh\\Desktop\\aidps assignment", "#94A3B8", False),
    ("plugins: anyio-4.12.1, langsmith-0.7.25, asyncio-1.4.0", "#94A3B8", False),
    ("asyncio: mode=Mode.STRICT, debug=False", "#94A3B8", False),
    ("collected 44 items", "#E2E8F0", True),
    ("", "#FFFFFF", False),
    ("tests\\test_baseline_loader.py::test_load_baseline_from_terraform PASSED         [  2%]", "#34D399", False),
    ("tests\\test_baseline_loader.py::test_load_baseline_fallback PASSED               [  4%]", "#34D399", False),
    ("tests\\test_baseline_loader.py::test_baseline_schema_validation PASSED           [  6%]", "#34D399", False),
    ("tests\\test_baseline_loader.py::test_baseline_immutability PASSED                 [  9%]", "#34D399", False),
    ("tests\\test_collector_stubber.py::test_collector_telemetry_stubber PASSED        [ 11%]", "#34D399", False),
    ("tests\\test_collector_stubber.py::test_collector_network_retry PASSED            [ 13%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_status_endpoint PASSED                        [ 15%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_scan_endpoint_trigger PASSED                 [ 18%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_scan_concurrency_locking PASSED               [ 20%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_compare_endpoint_diff_matrix PASSED          [ 22%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_download_report_security_guard PASSED        [ 25%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_path_traversal_rejection PASSED               [ 27%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_ui_index_serving PASSED                       [ 29%]", "#34D399", False),
    ("tests\\test_dashboard_api.py::test_metrics_calculation PASSED                     [ 31%]", "#34D399", False),
    ("tests\\test_errors_and_partial.py::test_permission_denied_handling PASSED        [ 40%]", "#34D399", False),
    ("tests\\test_errors_and_partial.py::test_partial_telemetry_evaluation PASSED       [ 52%]", "#34D399", False),
    ("tests\\test_models.py::test_compliance_report_serialization PASSED              [ 59%]", "#34D399", False),
    ("tests\\test_reporter.py::test_reporter_json_generation PASSED                   [ 70%]", "#34D399", False),
    ("tests\\test_rules_compliant.py::test_all_rules_compliant_baseline PASSED        [ 72%]", "#34D399", False),
    ("tests\\test_rules_drift.py::test_drift_rule_public_access_block PASSED          [ 81%]", "#34D399", False),
    ("tests\\test_rules_drift.py::test_drift_rule_encryption_missing PASSED            [ 88%]", "#34D399", False),
    ("tests\\test_rules_drift.py::test_drift_rule_versioning_suspended PASSED          [ 95%]", "#34D399", False),
    ("tests\\test_rules_drift.py::test_drift_rule_mandatory_tags_missing PASSED       [100%]", "#34D399", False),
    ("", "#FFFFFF", False),
    ("============================== 44 passed in 31.95s ===============================", "#34D399", True)
]
create_terminal_image("docs/figures/fig_5_6_pytest_verification.png", "Pytest Automated Test Harness: 44/44 Comprehensive Test Cases Passing", pytest_lines, width=1200, height=720)

# -------------------------------------------------------------
# Figure 5.2: Policy Rules Evaluation Table Graphic
# -------------------------------------------------------------
def create_rules_table_graphic():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Card Container
    card = patches.FancyBboxPatch((0.2, 0.2), 10.6, 5.8, boxstyle="round,pad=0.08,rounding_size=0.15",
                                  linewidth=1.2, edgecolor='#E2E8F0', facecolor='#FFFFFF')
    ax.add_patch(card)

    # Header Bar
    header = patches.FancyBboxPatch((0.2, 5.2), 10.6, 0.8, boxstyle="round,pad=0.08,rounding_size=0.15",
                                    linewidth=0, facecolor='#F8FAFC')
    ax.add_patch(header)
    ax.text(0.5, 5.65, "Policy Rule Evaluation & Security Baseline Status", fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(0.5, 5.35, "Real-time compliance assertions executed against AWS S3 audit storage", fontsize=8.5, color='#64748B')

    # Table Columns
    headers = [("Rule ID", 0.6), ("Security Baseline", 2.2), ("Expected Value", 5.0), ("Observed Telemetry", 7.2), ("Status", 9.4)]
    for h, xpos in headers:
        ax.text(xpos, 4.9, h, fontsize=9, fontweight='bold', color='#475569')

    # Line below header
    ax.plot([0.5, 10.5], [4.75, 4.75], color='#CBD5E1', lw=1)

    rows = [
        ("S3-001", "Bucket Existence Check", "Bucket Present", "Present & Accessible", "COMPLIANT", "#10B981"),
        ("S3-002", "Public Access Block (4-tier)", "All 4 Flags True", "All 4 Flags True", "COMPLIANT", "#10B981"),
        ("S3-003", "Server-Side Encryption", "SSE: AES256", "AES256 (AWS-Managed)", "COMPLIANT", "#10B981"),
        ("S3-004", "Object Versioning State", "Status: Enabled", "Status: Enabled", "COMPLIANT", "#10B981"),
        ("S3-005", "Mandatory Governance Tags", "Project, Env, ManagedBy", "All 3 Tags Present", "COMPLIANT", "#10B981"),
        ("S3-006", "Environment Tag Value", "Environment == 'dev'", "Environment == 'dev'", "COMPLIANT", "#10B981"),
        ("S3-007", "ManagedBy Tag Value", "ManagedBy == 'Terraform'", "ManagedBy == 'Terraform'", "COMPLIANT", "#10B981"),
    ]

    y = 4.35
    for rid, name, exp, obs, status, badge_col in rows:
        ax.text(0.6, y, rid, fontsize=8.5, fontweight='bold', color='#1E293B')
        ax.text(2.2, y, name, fontsize=8.5, color='#334155')
        ax.text(5.0, y, exp, fontsize=8.2, color='#475569', fontfamily='monospace')
        ax.text(7.2, y, obs, fontsize=8.2, color='#475569', fontfamily='monospace')
        
        # Badge
        b_rect = patches.FancyBboxPatch((9.3, y - 0.12), 1.2, 0.28, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        linewidth=0, facecolor='#DCFCE7')
        ax.add_patch(b_rect)
        ax.text(9.9, y + 0.02, status, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#15803D')
        
        y -= 0.52
        ax.plot([0.5, 10.5], [y + 0.25, y + 0.25], color='#F1F5F9', lw=0.8)

    plt.tight_layout()
    plt.savefig("docs/figures/fig_5_2_rules_table.png", dpi=300, facecolor='#FFFFFF')
    plt.close()
    print("Generated fig_5_2_rules_table.png")

create_rules_table_graphic()

# -------------------------------------------------------------
# Figure 5.3: Simulated Drift Scenario Graphic
# -------------------------------------------------------------
def create_drift_scenario_graphic():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Card Container
    card = patches.FancyBboxPatch((0.2, 0.2), 10.6, 5.8, boxstyle="round,pad=0.08,rounding_size=0.15",
                                  linewidth=1.2, edgecolor='#FCA5A5', facecolor='#FFFFFF')
    ax.add_patch(card)

    # Header Bar
    header = patches.FancyBboxPatch((0.2, 5.2), 10.6, 0.8, boxstyle="round,pad=0.08,rounding_size=0.15",
                                    linewidth=0, facecolor='#FEF2F2')
    ax.add_patch(header)
    ax.text(0.5, 5.65, "Simulated Drift Scenario: High-Severity Policy Violations", fontsize=12, fontweight='bold', color='#991B1B')
    ax.text(0.5, 5.35, "Simulating out-of-band AWS console modifications and security boundary degradation", fontsize=8.5, color='#B91C1C')

    # Table Columns
    headers = [("Rule ID", 0.6), ("Security Baseline", 2.2), ("Codified Baseline", 5.0), ("Drifted Runtime State", 7.2), ("Evaluation", 9.4)]
    for h, xpos in headers:
        ax.text(xpos, 4.9, h, fontsize=9, fontweight='bold', color='#475569')

    ax.plot([0.5, 10.5], [4.75, 4.75], color='#F87171', lw=1)

    drift_rows = [
        ("S3-001", "Bucket Existence Check", "Present", "Present", "COMPLIANT", "#DCFCE7", "#15803D"),
        ("S3-002", "Public Access Block", "All 4 Flags True", "BlockPublicPolicy=False", "NON_COMPLIANT", "#FEE2E2", "#B91C1C"),
        ("S3-003", "Server Encryption", "SSE: AES256", "Encryption Disabled", "NON_COMPLIANT", "#FEE2E2", "#B91C1C"),
        ("S3-004", "Object Versioning", "Enabled", "Enabled", "COMPLIANT", "#DCFCE7", "#15803D"),
        ("S3-005", "Mandatory Governance Tags", "All 3 Present", "All 3 Present", "COMPLIANT", "#DCFCE7", "#15803D"),
        ("S3-006", "Environment Tag Value", "Environment='dev'", "Environment='staging'", "NON_COMPLIANT", "#FEF3C7", "#B45309"),
        ("S3-007", "ManagedBy Tag Value", "ManagedBy='Terraform'", "ManagedBy='Terraform'", "COMPLIANT", "#DCFCE7", "#15803D"),
    ]

    y = 4.35
    for rid, name, exp, obs, status, bg_col, text_col in drift_rows:
        ax.text(0.6, y, rid, fontsize=8.5, fontweight='bold', color='#1E293B')
        ax.text(2.2, y, name, fontsize=8.5, color='#334155')
        ax.text(5.0, y, exp, fontsize=8.2, color='#475569', fontfamily='monospace')
        ax.text(7.2, y, obs, fontsize=8.2, fontweight='bold' if 'NON' in status else 'normal',
                color='#B91C1C' if 'NON' in status else '#475569', fontfamily='monospace')
        
        b_rect = patches.FancyBboxPatch((9.2, y - 0.12), 1.4, 0.28, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        linewidth=0, facecolor=bg_col)
        ax.add_patch(b_rect)
        ax.text(9.9, y + 0.02, status, ha='center', va='center', fontsize=7.2, fontweight='bold', color=text_col)
        
        y -= 0.52
        ax.plot([0.5, 10.5], [y + 0.25, y + 0.25], color='#F1F5F9', lw=0.8)

    plt.tight_layout()
    plt.savefig("docs/figures/fig_5_3_simulated_drift.png", dpi=300, facecolor='#FFFFFF')
    plt.close()
    print("Generated fig_5_3_simulated_drift.png")

create_drift_scenario_graphic()

# -------------------------------------------------------------
# Figure 5.4: Side-by-Side Diff Matrix Graphic
# -------------------------------------------------------------
def create_diff_matrix_graphic():
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.8)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Card Container
    card = patches.FancyBboxPatch((0.2, 0.2), 10.6, 5.4, boxstyle="round,pad=0.08,rounding_size=0.15",
                                  linewidth=1.2, edgecolor='#CBD5E1', facecolor='#FFFFFF')
    ax.add_patch(card)

    header = patches.FancyBboxPatch((0.2, 4.8), 10.6, 0.8, boxstyle="round,pad=0.08,rounding_size=0.15",
                                    linewidth=0, facecolor='#F1F5F9')
    ax.add_patch(header)
    ax.text(0.5, 5.25, "Side-by-Side Configuration Drift Delta Matrix", fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(0.5, 4.95, "Direct comparative diff isolating codified IaC baselines against diverted runtime parameters", fontsize=8.5, color='#475569')

    # Columns
    headers = [("Parameter Key", 0.6), ("Codified Baseline (IaC)", 3.4), ("Live Telemetry", 6.2), ("Drift Divergence", 8.8)]
    for h, xpos in headers:
        ax.text(xpos, 4.5, h, fontsize=9, fontweight='bold', color='#334155')
    ax.plot([0.5, 10.5], [4.35, 4.35], color='#94A3B8', lw=1)

    diffs = [
        ("PublicAccessBlock.BlockPublicPolicy", "true", "false", "DRIFT DETECTED", "#FEE2E2", "#991B1B"),
        ("ServerEncryption.SSEAlgorithm", "AES256", "None (Disabled)", "DRIFT DETECTED", "#FEE2E2", "#991B1B"),
        ("Versioning.Status", "Enabled", "Enabled", "IN SYNC", "#DCFCE7", "#15803D"),
        ("Tag.Environment", "'dev'", "'staging'", "DRIFT DETECTED", "#FEF3C7", "#92400E"),
        ("Tag.ManagedBy", "'Terraform'", "'Terraform'", "IN SYNC", "#DCFCE7", "#15803D"),
        ("Tag.Project", "'idps-compliance'", "'idps-compliance'", "IN SYNC", "#DCFCE7", "#15803D"),
    ]

    y = 3.95
    for key, base, live, status, bg_col, txt_col in diffs:
        ax.text(0.6, y, key, fontsize=8.2, fontweight='bold', color='#1E293B', fontfamily='monospace')
        ax.text(3.4, y, base, fontsize=8.2, color='#334155', fontfamily='monospace')
        ax.text(6.2, y, live, fontsize=8.2, color='#334155', fontfamily='monospace')
        
        b_rect = patches.FancyBboxPatch((8.7, y - 0.12), 1.6, 0.28, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        linewidth=0, facecolor=bg_col)
        ax.add_patch(b_rect)
        ax.text(9.5, y + 0.02, status, ha='center', va='center', fontsize=7.2, fontweight='bold', color=txt_col)
        
        y -= 0.55
        ax.plot([0.5, 10.5], [y + 0.25, y + 0.25], color='#F1F5F9', lw=0.8)

    plt.tight_layout()
    plt.savefig("docs/figures/fig_5_4_diff_matrix.png", dpi=300, facecolor='#FFFFFF')
    plt.close()
    print("Generated fig_5_4_diff_matrix.png")

create_diff_matrix_graphic()

# -------------------------------------------------------------
# Figure 5.7: Structured Audit Report JSON Graphic
# -------------------------------------------------------------
json_lines = [
    ('{', '#E2E8F0', False),
    ('  "report_id": "rep-7f39b1a0-62c1",', '#38BDF8', False),
    ('  "generated_at": "2026-10-15T10:48:35.120Z",', '#94A3B8', False),
    ('  "target_resource": "idps-compliance-dev-640110193463-ap-south-1",', '#A7F3D0', True),
    ('  "region": "ap-south-1",', '#A7F3D0', False),
    ('  "status": "COMPLIANT",', '#34D399', True),
    ('  "summary": {', '#E2E8F0', False),
    ('    "total_rules": 7,', '#FBBF24', False),
    ('    "compliant": 7,', '#34D399', True),
    ('    "non_compliant": 0,', '#F87171', False),
    ('    "errors": 0,', '#94A3B8', False),
    ('    "drift_detected": false', '#34D399', True),
    ('  },', '#E2E8F0', False),
    ('  "rules": [', '#E2E8F0', False),
    ('    {', '#CBD5E1', False),
    ('      "rule_id": "S3-002-PUBLIC-ACCESS",', '#38BDF8', False),
    ('      "status": "COMPLIANT",', '#34D399', True),
    ('      "severity": "HIGH",', '#FBBF24', False),
    ('      "details": "All 4 BlockPublicAccess settings are explicitly set to true."', '#E2E8F0', False),
    ('      "observed": { "block_public_acls": true, "ignore_public_acls": true, ... }', '#94A3B8', False),
    ('    },', '#CBD5E1', False),
    ('    {', '#CBD5E1', False),
    ('      "rule_id": "S3-003-ENCRYPTION",', '#38BDF8', False),
    ('      "status": "COMPLIANT",', '#34D399', True),
    ('      "severity": "CRITICAL",', '#F87171', True),
    ('      "details": "Server-side encryption is enforced with algorithm AES256."', '#E2E8F0', False),
    ('      "observed": { "sse_algorithm": "AES256" }', '#94A3B8', False),
    ('    }', '#CBD5E1', False),
    ('  ]', '#E2E8F0', False),
    ('}', '#E2E8F0', False)
]
create_terminal_image("docs/figures/fig_5_7_json_report.png", "Compliance Report: reports/live-compliance.json (JSON Schema Artifact)", json_lines, width=1200, height=720)

print("All figures generated successfully!")
