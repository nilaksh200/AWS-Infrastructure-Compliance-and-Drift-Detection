import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

os.makedirs("docs/figures", exist_ok=True)

# -------------------------------------------------------------
# Figure 4.1: High-Level System Architecture Diagram
# -------------------------------------------------------------
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Draw Title Box
    ax.text(5.5, 6.1, "Policy-Driven Infrastructure Compliance and Drift Detection Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A', fontfamily='sans-serif')
    ax.text(5.5, 5.75, "Decoupled Telemetry, Multi-State Evaluation, and Asynchronous Web Audit System", 
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#475569', fontfamily='sans-serif')

    def draw_box(x, y, w, h, title, subtitle, bg_color, border_color, title_color='#0F172A', badge=None):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      linewidth=1.8, edgecolor=border_color, facecolor=bg_color)
        ax.add_patch(rect)
        if badge:
            badge_rect = patches.FancyBboxPatch((x + 0.15, y + h - 0.28), 1.4, 0.22, 
                                                boxstyle="round,pad=0.02,rounding_size=0.06",
                                                linewidth=0, facecolor=border_color)
            ax.add_patch(badge_rect)
            ax.text(x + 0.85, y + h - 0.17, badge, ha='center', va='center', 
                    fontsize=7, fontweight='bold', color='#FFFFFF', fontfamily='sans-serif')
            ax.text(x + w/2, y + h - 0.5, title, ha='center', va='center', 
                    fontsize=10.5, fontweight='bold', color=title_color, fontfamily='sans-serif')
        else:
            ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', 
                    fontsize=10.5, fontweight='bold', color=title_color, fontfamily='sans-serif')
            
        ax.text(x + w/2, y + (h/2) - 0.25, subtitle, ha='center', va='center', 
                fontsize=8, color='#334155', fontfamily='sans-serif', multialignment='center')

    # 1. Terraform IaC Layer
    draw_box(0.5, 3.4, 2.8, 1.9, "1. Terraform IaC Layer", 
             "• Codified AWS S3 Bucket\n• Strict Public Access Block\n• AES-256 Server Encryption\n• Versioning & Governance Tags\n(terraform/*.tf)",
             "#EFF6FF", "#2563EB", badge="IAC BASELINE")

    # 2. AWS Cloud Platform
    draw_box(7.7, 3.4, 2.8, 1.9, "2. Live AWS Cloud", 
             "• Region: ap-south-1\n• S3 Bucket Storage Target\n• Access Control Lists (ACLs)\n• Bucket Policies & KMS/SSE\n• Runtime Tag Metadata",
             "#FEF2F2", "#DC2626", badge="RUNTIME TARGET")

    # 3. Baseline Ingestion Loader
    draw_box(0.5, 0.8, 2.8, 1.8, "3. Baseline Loader", 
             "• Query: terraform output -json\n• Dynamic Resource Parsing\n• Fallback Baseline Schema\n• Immutable Parameter Hydration",
             "#F0FDF4", "#16A34A", badge="HYDRATION")

    # 4. S3 Telemetry Collector
    draw_box(7.7, 0.8, 2.8, 1.8, "4. S3 Telemetry Collector", 
             "• Read-Only AWS SDK (boto3)\n• TLS HTTPS API Queries\n• HeadBucket, Encryption\n• PublicAccessBlock, Versioning\n• Non-Mutating Audit Scans",
             "#FFFBEB", "#D97706", badge="TELEMETRY")

    # 5. Central Compliance & Drift Evaluator
    draw_box(4.0, 1.8, 3.0, 2.8, "5. Compliance Evaluator", 
             "Polymorphic Rule Engine (7 Rules):\n"
             "• S3BucketExistenceRule\n"
             "• S3PublicAccessBlockRule\n"
             "• S3EncryptionRule (AES256)\n"
             "• S3VersioningRule\n"
             "• S3MandatoryTagsRule\n"
             "• S3EnvironmentTagRule\n"
             "• S3ManagedByTagRule\n\n"
             "Tri-State Logic: COMPLIANT,\n"
             "NON_COMPLIANT (Drift), ERROR",
             "#FAF5FF", "#7C3AED", badge="EVALUATION CORE")

    # 6. Presentation & Dashboard API
    draw_box(3.8, 4.8, 3.4, 0.8, "6. FastAPI Bridge & Web UI", 
             "REST API (/api/scan, /api/compare) • Thread Locking • SPA UI",
             "#F8FAFC", "#0284C7", badge="PRESENTATION")

    # Connective Arrows
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=14))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.12, label, ha='center', va='center', fontsize=7.5, 
                    fontweight='bold', color='#1E293B', bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    draw_arrow(1.9, 3.4, 1.9, 2.6, "outputs.tf (JSON)")
    draw_arrow(9.1, 3.4, 9.1, 2.6, "Read-Only SDK APIs")
    draw_arrow(3.3, 1.7, 4.0, 2.4, "Expected Baseline")
    draw_arrow(7.7, 1.7, 7.0, 2.4, "Observed Telemetry")
    draw_arrow(5.5, 4.6, 5.5, 4.8, "ComplianceReport")

    plt.tight_layout()
    plt.savefig("docs/figures/fig_4_1_architecture.png", dpi=300, facecolor='#F8FAFC')
    plt.close()
    print("Created fig_4_1_architecture.png")

generate_architecture_diagram()
