"""
docs/build_report_docx.py
Compiles the comprehensive, publication-grade Final Project Report in .docx format
for IntelliArchive (BCSE355L - Cloud Architecture Design).
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DOCX = PROJECT_ROOT / "docs" / "Final_Project_Report.docx"


def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_callout(doc, text: str, title: str = "Key Architecture Note"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📌 {title}: ")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = RGBColor(14, 116, 144)

    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_before = Pt(4)


def main():
    doc = docx.Document()

    # Set page margins: 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # -------------------------------------------------------------------------
    # Cover / Header
    # -------------------------------------------------------------------------
    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_course = p_course.add_run("BCSE355L – CLOUD ARCHITECTURE DESIGN")
    r_course.bold = True
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(14)
    r_course.font.color.rgb = RGBColor(14, 116, 144)
    p_course.paragraph_format.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("FINAL PROJECT TECHNICAL REPORT")
    r_sub.bold = True
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)
    p_sub.paragraph_format.space_after = Pt(16)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Intelligent Object Lifecycle Optimization for Satellite Image Archives using Vision Foundation Models")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.paragraph_format.space_after = Pt(20)

    # Team Box Table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Project Team:", "K. Pavan Kumar Reddy (24BIT0580)\nAnhad (24BIT0129)"),
        ("Faculty Supervisor:", "Dr. Priya V, Associate Professor"),
        ("Department & School:", "School of Computer Science & Engineering (SCOPE)"),
        ("Institution:", "Vellore Institute of Technology (VIT), Vellore")
    ]
    for i, (k, v) in enumerate(meta_rows):
        c0 = tbl_meta.cell(i, 0)
        c1 = tbl_meta.cell(i, 1)
        c0.text = k
        c1.text = v
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(10)
        c1.paragraphs[0].runs[0].font.size = Pt(10)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    # -------------------------------------------------------------------------
    # 1. Abstract
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("1. Abstract", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    p_abs = doc.add_paragraph(
        "Modern Earth observation satellites and aerial constellations collect petabytes of high-resolution imagery daily. "
        "However, prevailing cloud storage lifecycle frameworks (such as standard Amazon Web Services S3 Lifecycle rules) "
        "depend exclusively on object age, directory prefix matching, or fixed transition schedules. This age-based paradigm "
        "fails to capture operational semantics: imagery documenting dense urban infrastructure, transportation networks, or active "
        "natural disaster zones retains high operational and scientific value indefinitely, whereas cloud-obscured, blurred, or barren "
        "terrain imagery incurs unwarranted storage expenditures when maintained in hot storage tiers. "
        "This project introduces IntelliArchive, a content-aware storage lifecycle optimization system driven by vision foundation models. "
        "By employing OpenAI CLIP ViT-B/32, satellite imagery is dynamically evaluated via zero-shot semantic importance scoring. "
        "The calculated score automates object tiering across Amazon S3 Standard, S3 Standard-IA, and S3 Glacier Flexible Retrieval tiers. "
        "The project provides a comprehensive software implementation featuring an aerospace-styled FastAPI web platform, dual-mode "
        "storage execution (atomic local directory simulation and live AWS S3 private bucket integration in ap-south-1), Docker "
        "containerization optimized with CPU PyTorch wheels (1.36 GB pushed to Amazon ECR), and 100% automated test verification (41/41 passed). "
        "Empirical evaluation on SpaceNet satellite datasets projects recurring cloud storage cost reductions of up to 49% compared to traditional flat storage architectures."
    )
    p_abs.paragraph_format.line_spacing = 1.15
    p_abs.paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # 2. Problem Statement & Motivation
    # -------------------------------------------------------------------------
    h2 = doc.add_heading("2. Problem Statement & Motivation", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Traditional cloud object storage lifecycle policies are inherently 'content-blind'. When an organization configures an S3 Lifecycle "
        "rule, the policy inspects only object metadata—primarily the object creation date and key prefix. For satellite archives, this leads "
        "to two fundamental operational inefficiencies:"
    )

    p_p1 = doc.add_paragraph()
    r = p_p1.add_run("• Premature Cold Archival of Mission-Critical Assets: ")
    r.bold = True
    p_p1.add_run(
        "A 90-day-old high-resolution satellite scene of a dense urban center or critical transportation hub is transitioned into cold "
        "storage (e.g., S3 Glacier), requiring hours of retrieval latency and significant egress fees when analysts require urgent access."
    )

    p_p2 = doc.add_paragraph()
    r = p_p2.add_run("• Unnecessary Hot Storage Cost Accumulation: ")
    r.bold = True
    p_p2.add_run(
        "Images rendered unusable by heavy cloud cover, sensor glint, or uninformative open ocean remain in hot S3 Standard storage ($0.023/GB/month) "
        "for the entire retention window simply because their age has not met the transition threshold."
    )

    add_callout(
        doc,
        "IntelliArchive solves this structural discrepancy by decoupling lifecycle decisions from chronological age, replacing static schedules with "
        "instantaneous, automated semantic relevance assessment at ingestion time.",
        "Core Value Proposition"
    )

    # -------------------------------------------------------------------------
    # 3. System Architecture & Dual Execution Model
    # -------------------------------------------------------------------------
    h3 = doc.add_heading("3. System Architecture & Dual Execution Model", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "IntelliArchive is designed around a dual-engine architecture that provides both a zero-dependency local simulation prototype "
        "for reproducible academic evaluation and a production-grade cloud integration with Amazon Web Services."
    )

    # Table comparing Prototype vs Proposed Cloud
    tbl_arch = doc.add_table(rows=6, cols=3)
    tbl_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Architecture Dimension", "Implemented Prototype", "Proposed Cloud Production Architecture"]
    for j, h in enumerate(headers):
        cell = tbl_arch.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "0E7490")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 100, 100)

    rows_data = [
        ("Compute & Application Host", "Local FastAPI ASGI server / Docker Container", "AWS ECS Fargate serverless container tasks"),
        ("Vision Foundation Model", "OpenAI CLIP ViT-B/32 (PyTorch CPU singleton)", "Amazon Bedrock (Claude 3.5 Sonnet / Titan Multimodal)"),
        ("Storage Classes", "Directory tiers (cloud_simulation/S3_STANDARD, IA, GLACIER)", "Amazon S3 Intelligent-Tiering & Lifecycle Transitions"),
        ("Live Cloud Bucket", "Amazon S3 ap-south-1 (intelliarchive-pavan-satellite-2026)", "Multi-region S3 Buckets with Cross-Region Replication"),
        ("Audit & Metadata Ledger", "Atomic CSV ledgers (results/lifecycle_log.csv)", "Amazon DynamoDB (Global Secondary Index on Tier/Score)")
    ]

    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = tbl_arch.cell(i + 1, j)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # 4. Vision Foundation Model Methodology
    # -------------------------------------------------------------------------
    h4 = doc.add_heading("4. Vision Foundation Model Pipeline", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The semantic evaluation pipeline consists of three sequential processing phases: radiometric contrast preprocessing, "
        "zero-shot foundation model inference, and composite tier thresholding."
    )

    doc.add_heading("4.1 Satellite Radiometric Preprocessing", level=2)
    doc.add_paragraph(
        "Satellite imagery sourced from sensors such as WorldView-3 (SpaceNet Las Vegas) is delivered as multi-spectral 16-bit GeoTIFF files. "
        "Because sensor pixel intensities typically cluster in narrow intervals near zero, uncorrected images appear pitch black when passed "
        "to vision models trained on standard 8-bit web imagery. To resolve this, enhance_satellite_image() applies dynamic per-channel min-max "
        "contrast stretching across color channels to rescale pixel values to [0, 255], followed by bilinear resampling to 224 × 224 pixels."
    )

    doc.add_heading("4.2 Zero-Shot Semantic Scoring Formulation", level=2)
    doc.add_paragraph(
        "Rather than training brittle supervised classifiers, IntelliArchive employs the OpenAI CLIP ViT-B/32 foundation model. "
        "Zero-shot classification is executed against three semantic prompt anchors:"
    )
    p_pr = doc.add_paragraph()
    p_pr.add_run("1. High Importance Prompt (P_High): ").bold = True
    p_pr.add_run('"important satellite image containing urban infrastructure"\n')
    p_pr.add_run("2. Medium Importance Prompt (P_Med): ").bold = True
    p_pr.add_run('"moderately important satellite image"\n')
    p_pr.add_run("3. Low Importance Prompt (P_Low): ").bold = True
    p_pr.add_run('"unimportant satellite image with little useful information"')

    doc.add_paragraph(
        "The normalized softmax probabilities P_High, P_Med, and P_Low are combined into a bounded composite importance score (0 - 100):"
    )

    p_eq = doc.add_paragraph()
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq = p_eq.add_run("Importance Score = (P_High × 100) + (P_Med × 50) + (P_Low × 0)")
    r_eq.bold = True
    r_eq.font.size = Pt(11)
    r_eq.font.color.rgb = RGBColor(14, 116, 144)

    doc.add_heading("4.3 Lifecycle Tier Assignment Thresholds", level=2)
    doc.add_paragraph(
        "The composite score directly maps into storage tiers and access characteristics:"
    )
    p_t1 = doc.add_paragraph()
    p_t1.add_run("• Score ≥ 70.0 (HIGH) → S3_STANDARD: ").bold = True
    p_t1.add_run("Mission-critical urban infrastructure and active monitoring regions requiring millisecond access latency.")
    p_t2 = doc.add_paragraph()
    p_t2.add_run("• 40.0 ≤ Score < 70.0 (MEDIUM) → S3_STANDARD_IA: ").bold = True
    p_t2.add_run("Suburban and moderate-detail regions accessed infrequently, yielding immediate 45.6% storage savings.")
    p_t3 = doc.add_paragraph()
    p_t3.add_run("• Score < 40.0 (LOW) → S3_GLACIER: ").bold = True
    p_t3.add_run("Cloud-covered, redundant, or low-information imagery transitioned to cold archival, yielding 82.6% cost reduction.")

    # -------------------------------------------------------------------------
    # 5. Experimental Results & Cost Optimization Analysis
    # -------------------------------------------------------------------------
    h5 = doc.add_heading("5. Experimental Results & Cost Optimization", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Experimental validation was conducted on SpaceNet Las Vegas high-resolution satellite scenes. "
        "The importance score distribution demonstrates effective separation between dense structural infrastructure and open ground/cloud cover."
    )

    # Insert charts if available
    chart_score = PROJECT_ROOT / "results" / "importance_scores_chart.png"
    if chart_score.exists():
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(chart_score), width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 1: Semantic Importance Scores across SpaceNet Satellite Image Archive")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True

    chart_cat = PROJECT_ROOT / "results" / "category_distribution.png"
    if chart_cat.exists():
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(chart_cat), width=Inches(4.8))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap2 = p_cap2.add_run("Figure 2: Distribution of Evaluated Imagery across Importance Categories")
        r_cap2.font.size = Pt(9)
        r_cap2.font.italic = True

    doc.add_heading("5.1 Cloud Economic Cost Model", level=2)
    doc.add_paragraph(
        "Based on prevailing AWS S3 pricing in the ap-south-1 (Mumbai) region ($0.023/GB for S3 Standard, $0.0125/GB for S3 Standard-IA, "
        "and $0.0040/GB for S3 Glacier Flexible Retrieval), the cost benefit for a sample 10 TB satellite archive is modeled below:"
    )

    # Cost Table
    tbl_cost = doc.add_table(rows=4, cols=4)
    tbl_cost.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Storage Architecture", "Allocation (10 TB Archive)", "Unit Pricing", "Monthly Cost"]
    for j, h in enumerate(c_headers):
        cell = tbl_cost.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "0E7490")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 100, 100)

    cost_data = [
        ("Baseline (Flat S3 Standard)", "10 TB (100% Hot)", "$0.0230 / GB", "$230.00 / mo"),
        ("Static Time-Based Policy", "6 TB Standard, 4 TB IA", "Mixed Rates", "$188.00 / mo (18.2% savings)"),
        ("IntelliArchive Content-Aware", "2.5 TB Standard, 3.5 TB IA, 4.0 TB Glacier", "Optimized Rates", "$117.25 / mo (49.0% savings)")
    ]
    for i, row in enumerate(cost_data):
        for j, val in enumerate(row):
            cell = tbl_cost.cell(i + 1, j)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if i == 2:
                cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "DCFCE7")  # soft green
            else:
                set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # 6. Containerization & Amazon ECR Verification
    # -------------------------------------------------------------------------
    h6 = doc.add_heading("6. Containerization & Amazon ECR Verification", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The application is packaged inside a security-hardened Docker container adhering to container best practices:"
    )
    p_d1 = doc.add_paragraph()
    p_d1.add_run("• PyTorch CPU Optimization: ").bold = True
    p_d1.add_run("Standard deep learning Docker images frequently balloon to 12+ GB due to embedded CUDA/NVIDIA shared libraries. "
                 "By explicitly targeting official PyTorch CPU wheels (--index-url https://download.pytorch.org/whl/cpu), the image was shrunk to 1.36 GB.")
    p_d2 = doc.add_paragraph()
    p_d2.add_run("• Pre-Baked Model Caching: ").bold = True
    p_d2.add_run("CLIP ViT-B/32 weights are downloaded during build time into /app/.cache/huggingface, guaranteeing deterministic startup and eliminating cold-start network latency.")
    p_d3 = doc.add_paragraph()
    p_d3.add_run("• Amazon ECR Registry Status: ").bold = True
    p_d3.add_run("The container image has been successfully pushed and verified in Amazon Elastic Container Registry at URI: "
                 "371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive:cpu-test.")

    # -------------------------------------------------------------------------
    # 7. Automated Test Suite Verification
    # -------------------------------------------------------------------------
    h7 = doc.add_heading("7. Automated Test Suite Verification", level=1)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The project enforces rigorous automated test coverage via pytest, achieving a 100% pass rate across 41 unit and integration tests:"
    )
    p_ts1 = doc.add_paragraph()
    p_ts1.add_run("• tests/test_lifecycle_storage.py (10 Tests Passed): ").bold = True
    p_ts1.add_run("Validates storage tier validation, atomic migration of multi-hop tier transitions without file corruption, duplicate prevention, and CSV ledger consistency.")
    p_ts2 = doc.add_paragraph()
    p_ts2.add_run("• tests/test_s3_service.py (24 Tests Passed): ").bold = True
    p_ts2.add_run("Validates real and mocked boto3 client behaviors, custom object key prefixing, error sanitization (zero leaked credentials), and AWS ECS IAM task role resolution.")
    p_ts3 = doc.add_paragraph()
    p_ts3.add_run("• tests/test_web_app.py (7 Tests Passed): ").bold = True
    p_ts3.add_run("Tests HTML rendering across all 5 user views and validates FastAPI REST endpoints (/api/summary, /api/analytics, /api/lifecycle, /api/analyze-sample).")

    # -------------------------------------------------------------------------
    # 8. Work Distribution & Individual Contributions
    # -------------------------------------------------------------------------
    h8 = doc.add_heading("8. Work Distribution & Individual Contributions", level=1)
    h8.paragraph_format.space_before = Pt(14)
    h8.paragraph_format.space_after = Pt(6)

    tbl_work = doc.add_table(rows=3, cols=2)
    tbl_work.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_work.cell(0, 0).text = "Team Member"
    tbl_work.cell(0, 1).text = "Core Responsibilities & Technical Deliverables"
    for c in [tbl_work.cell(0, 0), tbl_work.cell(0, 1)]:
        c.paragraphs[0].runs[0].bold = True
        set_cell_background(c, "0E7490")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(c, 80, 80, 100, 100)

    contribs = [
        ("K. Pavan Kumar Reddy\n(24BIT0580)",
         "• Cloud Architecture & AWS Integration (S3 service, IAM credential fallbacks)\n"
         "• FastAPI Web Application, Aerospace UI & Chart.js dynamic dashboard\n"
         "• Docker containerization, CPU-wheel optimization & Amazon ECR push management\n"
         "• Integration testing for S3 service and web client endpoints"),
        ("Anhad\n(24BIT0129)",
         "• Vision Foundation Model integration (OpenAI CLIP ViT-B/32 zero-shot pipeline)\n"
         "• Image preprocessing (16-bit GeoTIFF contrast stretching & normalization)\n"
         "• Storage simulation directory engine and atomic CSV audit ledgers\n"
         "• Cloud cost analysis mathematical model & lifecycle unit tests")
    ]
    for i, (m, d) in enumerate(contribs):
        c0 = tbl_work.cell(i + 1, 0)
        c1 = tbl_work.cell(i + 1, 1)
        c0.text = m
        c1.text = d
        c0.paragraphs[0].runs[0].bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9)
        set_cell_background(c0, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # 9. Conclusion
    # -------------------------------------------------------------------------
    h9 = doc.add_heading("9. Conclusion & Future Roadmap", level=1)
    h9.paragraph_format.space_before = Pt(14)
    h9.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "IntelliArchive successfully demonstrates that modern Vision Foundation Models can revolutionize cloud storage lifecycle management. "
        "By replacing age-based assumptions with semantic content evaluation, satellite image repositories can achieve nearly 50% storage cost "
        "reductions while safeguarding critical high-value imagery from premature archival. "
        "Future enhancements will focus on deploying serverless Amazon Bedrock multimodal inference, automating S3 EventBridge ingestion "
        "triggers, and migrating CSV metadata ledgers into high-throughput Amazon DynamoDB tables."
    )

    doc.save(str(OUTPUT_DOCX))
    print(f"Final Project Report successfully created at: {OUTPUT_DOCX}")


if __name__ == "__main__":
    main()
