from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def generate_pdf():
    docs_dir = Path(__file__).resolve().parent
    md_file = docs_dir / "IDPS_Project_Report.md"
    pdf_file_primary = docs_dir / "IDPS_Project_Report_Nilaksh_Deval.pdf"
    pdf_file_alias = docs_dir / "IDPS_Project_Report.pdf"

    if not md_file.exists():
        raise FileNotFoundError(f"Markdown source not found at: {md_file}")

    md_content = md_file.read_text(encoding="utf-8")
    
    pdf = MarkdownPdf(toc_level=2)
    # A4 standard with 36pt (0.5 in) margins
    pdf.add_section(Section(md_content, paper_size="A4", borders=(36, 36, -36, -36)))
    pdf.save(str(pdf_file_primary))
    pdf.save(str(pdf_file_alias))
    print(f"Successfully generated PDF report ({pdf_file_primary.stat().st_size} bytes) at:\n- {pdf_file_primary}\n- {pdf_file_alias}")

if __name__ == "__main__":
    generate_pdf()
