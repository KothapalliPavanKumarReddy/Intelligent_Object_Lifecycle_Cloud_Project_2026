"""
presentation/build_presentation.py
Generates the comprehensive, professional 16:9 PowerPoint presentation
for IntelliArchive: Intelligent Object Lifecycle Optimization.
"""

from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "presentation" / "IntelliArchive_Final_Presentation.pptx"

# Dimensions: 16:9 Widescreen
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Color Palette: Aerospace Dark Theme
COLOR_BG = RGBColor(15, 23, 42)          # Deep Slate/Navy (#0F172A)
COLOR_CARD = RGBColor(30, 41, 59)        # Card Slate (#1E293B)
COLOR_CARD_BORDER = RGBColor(51, 65, 85) # Slate border (#334155)
COLOR_CYAN = RGBColor(56, 189, 248)      # Sky/Cyan Accent (#38BDF8)
COLOR_WHITE = RGBColor(255, 255, 255)    # White
COLOR_MUTED = RGBColor(148, 163, 184)    # Slate 400 (#94A3B8)
COLOR_EMERALD = RGBColor(52, 211, 153)   # Green Accent (#34D399)
COLOR_AMBER = RGBColor(251, 191, 36)     # Amber (#FBBF24)


def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, title: str, category: str = "INTELLIARCHIVE | BCSE355L"):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE


def add_card(slide, left, top, width, height, title: str = "", bg_color=COLOR_CARD):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = COLOR_CARD_BORDER
    shape.line.width = Pt(1)

    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
    return shape


def main():
    prs = pptx.Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(5.8), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(14, 116, 144)
    pill.line.fill.background()
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "  BCSE355L – CLOUD ARCHITECTURE DESIGN  •  PROJECT FINAL REVIEW  "
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_WHITE
    p_pill.alignment = PP_ALIGN.CENTER

    # Project Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "IntelliArchive: Intelligent Object Lifecycle"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Optimization for Satellite Archives using Vision Foundation Models"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CYAN

    p3 = tf.add_paragraph()
    p3.text = "Content-Aware Cloud Storage Tiering (S3 Standard / IA / Glacier) via OpenAI CLIP ViT-B/32"
    p3.font.size = Pt(15)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(12)

    # Team & Faculty Card
    c_left = Inches(1.0)
    c_top = Inches(4.5)
    add_card(s1, c_left, c_top, Inches(6.0), Inches(2.2), "PROJECT TEAM MEMBERS")
    tb = s1.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.7), Inches(5.4), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "•  K. Pavan Kumar Reddy  (Reg. No: 24BIT0580)"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "•  Anhad  (Reg. No: 24BIT0129)"
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(8)

    add_card(s1, Inches(7.3), c_top, Inches(5.0), Inches(2.2), "ACADEMIC SUPERVISION")
    tb = s1.shapes.add_textbox(Inches(7.6), c_top + Inches(0.7), Inches(4.4), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Course Faculty:  Dr. Priya V"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "School of Computer Science & Engineering (SCOPE)"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(6)
    p = tf.add_paragraph()
    p.text = "Vellore Institute of Technology, Vellore"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement: The Flaw in Static Cloud Lifecycle Policies")

    # Card 1: Static Rules
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.2), "TRADITIONAL S3 LIFECYCLE LIMITATIONS")
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    bullets1 = [
        ("Time-Only Triggers: ", "Objects transition strictly based on creation age (e.g. 30, 90, 180 days) regardless of content value."),
        ("Blind Prefix Filtering: ", "Prefix rules treat all files in a folder equally. High-value and low-value images are grouped together."),
        ("Premature Archival: ", "Critical urban disaster and high-resolution infrastructure imagery gets cold-archived prematurely, incurring expensive retrieval latencies."),
        ("Unnecessary Hot Costs: ", "Cloud-obscured, blurred, or empty terrain imagery sits in expensive S3 Standard for months before expiring.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets1):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_AMBER
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(12)

    # Card 2: The Solution
    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), "THE INTELLIARCHIVE PARADIGM")
    tb = s2.shapes.add_textbox(Inches(7.1), Inches(2.4), Inches(5.1), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    bullets2 = [
        ("Content-Aware Intelligence: ", "Evaluates the actual semantic information in satellite imagery at ingestion time."),
        ("Vision Foundation Models: ", "Leverages zero-shot OpenAI CLIP ViT-B/32 to score geospatial utility without requiring custom task training."),
        ("Automated Tiering Logic: ", "Dynamically maps high-utility imagery to S3 Standard, moderate detail to S3 Standard-IA, and empty/cloudy imagery to S3 Glacier immediately."),
        ("Provable Cost Reductions: ", "Simulates up to 45% - 60% recurring monthly storage savings while preserving immediate access to critical assets.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets2):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_EMERALD
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 3: System Objectives & Research Novelty
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Objectives & Research Novelty")

    objs = [
        ("1. Zero-Shot Semantic Evaluation", "Implement vision foundation models (CLIP ViT-B/32) to compute semantic importance scores without labor-intensive manual labeling.", COLOR_CYAN),
        ("2. Intelligent S3 Storage Tiering", "Automate storage allocation across AWS S3 Standard, S3 Standard-IA, and S3 Glacier Flexible Retrieval based on semantic thresholds.", COLOR_EMERALD),
        ("3. Dual-Engine Storage Architecture", "Simulate multi-tier local storage alongside live Amazon S3 private bucket integration in AWS ap-south-1 (Mumbai).", COLOR_AMBER),
        ("4. Interactive Web Platform", "Develop a FastAPI dashboard with real-time inference, archive filtering, and interactive Chart.js cost optimization visualizers.", COLOR_CYAN),
        ("5. Containerization & Verification", "Dockerize with CPU-optimized PyTorch wheels (1.36 GB pushed to Amazon ECR) and 100% automated test verification.", COLOR_EMERALD)
    ]

    for i, (title, desc, accent) in enumerate(objs):
        top_pos = Inches(1.6 + i * 1.05)
        add_card(s3, Inches(0.8), top_pos, Inches(11.7), Inches(0.95))
        tb = s3.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = title + "  —  "
        r1.font.bold = True
        r1.font.size = Pt(14)
        r1.font.color.rgb = accent
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 4: Architecture Comparison (Prototype vs. Proposed Production)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture: Local Prototype vs. AWS Cloud Production")

    # Card 1: Local Simulation Prototype
    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "CURRENT IMPLEMENTED PROTOTYPE")
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    proto_items = [
        ("Execution Engine: ", "FastAPI (Python 3.11) with Uvicorn ASGI server."),
        ("Vision Inference: ", "PyTorch CPU-only CLIP ViT-B/32 foundation model running locally."),
        ("Preprocessing Pipeline: ", "Dynamic 16-bit to 8-bit contrast stretching & 224x224 RGB conversion."),
        ("Storage Simulation: ", "Directory-based tiers (cloud_simulation/S3_STANDARD, IA, GLACIER)."),
        ("Live Cloud Integration: ", "Amazon S3 bucket in ap-south-1 (intelliarchive-pavan-satellite-2026)."),
        ("Audit Ledgers: ", "Atomic CSV ledgers (results/lifecycle_log.csv, importance_scores.csv).")
    ]
    for i, (k, v) in enumerate(proto_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    # Card 2: Proposed AWS Production Architecture
    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "PROPOSED AWS CLOUD PRODUCTION ARCHITECTURE")
    tb = s4.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    prod_items = [
        ("Container Compute: ", "AWS ECS Fargate serverless containers (zero server maintenance)."),
        ("Container Registry: ", "Amazon ECR (371234372967.dkr.ecr.ap-south-1.amazonaws.com)."),
        ("Foundation Models: ", "Amazon Bedrock (Claude 3 / Titan Multimodal) or SageMaker."),
        ("Storage Engine: ", "Amazon S3 Intelligent-Tiering & S3 Lifecycle automated transitions."),
        ("Metadata & Audit: ", "Amazon DynamoDB (low-latency distributed NoSQL lifecycle ledger)."),
        ("Security: ", "AWS IAM Task Roles (zero long-lived credentials stored in images).")
    ]
    for i, (k, v) in enumerate(prod_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_EMERALD
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 5: AI Model Pipeline & Scoring Formulation
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Vision Foundation Model: CLIP ViT-B/32 Pipeline")

    # Step 1: Preprocessing
    add_card(s5, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.3), "1. PREPROCESSING")
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(3.2), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Satellite TIFF Radiometry:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "16-bit GeoTIFF imagery values cluster near zero and appear black to standard RGB models."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_MUTED
    p.space_before = Pt(6)
    p = tf.add_paragraph()
    p.text = "Dynamic Contrast Stretching:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN
    p.space_before = Pt(12)
    p = tf.add_paragraph()
    p.text = "Per-channel min-max stretching maps pixel range to [0, 255] and resizes to 224×224 RGB."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(6)

    # Step 2: Zero-shot formulation
    add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3), "2. ZERO-SHOT PROMPT PAIRS")
    tb = s5.shapes.add_textbox(Inches(5.0), Inches(2.2), Inches(3.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Semantic Prompt Anchors:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE
    prompts = [
        ("High (P_H):", '"important satellite image containing urban infrastructure"', COLOR_EMERALD),
        ("Medium (P_M):", '"moderately important satellite image"', COLOR_AMBER),
        ("Low (P_L):", '"unimportant satellite image with little useful information"', RGBColor(248, 113, 113))
    ]
    for label, text, col in prompts:
        p = tf.add_paragraph()
        p.text = label
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.space_before = Pt(8)
        p = tf.add_paragraph()
        p.text = text
        p.font.italic = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_MUTED

    # Step 3: Composite Score
    add_card(s5, Inches(8.9), Inches(1.6), Inches(3.6), Inches(5.3), "3. COMPOSITE SCORING")
    tb = s5.shapes.add_textbox(Inches(9.1), Inches(2.2), Inches(3.2), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Weighted Score Formula:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "Score = (P_H × 100) + (P_M × 50) + (P_L × 0)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_CYAN
    p.space_before = Pt(8)
    p = tf.add_paragraph()
    p.text = "Tier Thresholds:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(14)
    thresholds = [
        ("Score ≥ 70.0", "HIGH → S3_STANDARD", COLOR_EMERALD),
        ("40.0 ≤ Score < 70.0", "MEDIUM → S3_STANDARD_IA", COLOR_AMBER),
        ("Score < 40.0", "LOW → S3_GLACIER", RGBColor(248, 113, 113))
    ]
    for r, t, col in thresholds:
        p = tf.add_paragraph()
        p.text = f"• {r}: {t}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: Dual Storage Engine & Live AWS S3 Integration
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Dual Storage Engine & Live Amazon S3 Integration")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "LOCAL SIMULATION ENGINE")
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    local_bullets = [
        ("Multi-Tier Directory Structure: ", "Separate folders for S3_STANDARD, S3_STANDARD_IA, and S3_GLACIER."),
        ("Atomic Multi-Hop Migrations: ", "Prevents duplicate or orphaned files across re-classification hops."),
        ("Audit Trails: ", "Tracks filename, score, category, source tier, destination tier, and timestamp in results/lifecycle_log.csv."),
        ("Analytics Ledger: ", "Historical score distribution maintained in results/importance_scores.csv.")
    ]
    for i, (k, v) in enumerate(local_bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "LIVE AMAZON S3 INTEGRATION")
    tb = s6.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    s3_bullets = [
        ("Target Bucket: ", "intelliarchive-pavan-satellite-2026"),
        ("AWS Region: ", "ap-south-1 (Asia Pacific - Mumbai)"),
        ("Private Access: ", "Block Public Access enabled, secured via IAM"),
        ("Direct Upload Pipeline: ", "Interactive Archive Browser allows direct multipart upload to S3 prefix satellite-images/"),
        ("Live Bucket Browser: ", "Lists remote cloud objects, object sizes, and storage class metadata in real-time.")
    ]
    for i, (k, v) in enumerate(s3_bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_EMERALD
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: Experimental Results & Dataset Evaluation
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Experimental Results: SpaceNet Satellite Evaluation")

    # Add Chart 1: Category distribution
    chart1_path = PROJECT_ROOT / "results" / "category_distribution.png"
    if chart1_path.exists():
        add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "IMPORTANCE CATEGORY SPREAD")
        s7.shapes.add_picture(str(chart1_path), Inches(1.0), Inches(2.3), width=Inches(5.2))

    # Add Chart 2: Storage distribution
    chart2_path = PROJECT_ROOT / "results" / "storage_distribution.png"
    if chart2_path.exists():
        add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "STORAGE CLASS ALLOCATION")
        s7.shapes.add_picture(str(chart2_path), Inches(7.0), Inches(2.3), width=Inches(5.3))

    # =========================================================================
    # SLIDE 8: Cloud Cost Optimization Analysis
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Cloud Cost Optimization Model")

    # Pricing Table Card
    add_card(s8, Inches(0.8), Inches(1.6), Inches(6.2), Inches(5.3), "AWS S3 STORAGE PRICING BENCHMARK (ap-south-1)")
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    pricing_data = [
        ("S3 Standard (Hot Tier):", "$0.023 per GB / month", "Frequent access, low latency"),
        ("S3 Standard-IA (Warm Tier):", "$0.0125 per GB / month", "45.6% cost reduction vs Standard"),
        ("S3 Glacier Flex (Cold Tier):", "$0.0040 per GB / month", "82.6% cost reduction vs Standard")
    ]
    for tier, cost, note in pricing_data:
        p = tf.paragraphs[0] if tier == pricing_data[0][0] else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = tier + "\n"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = f"• Rate: {cost}\n• Impact: {note}\n"
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    # Cost Savings Model Card
    add_card(s8, Inches(7.4), Inches(1.6), Inches(5.1), Inches(5.3), "COST SAVINGS SIMULATION")
    tb = s8.shapes.add_textbox(Inches(7.7), Inches(2.2), Inches(4.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Baseline (Flat S3 Standard):"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_AMBER
    p = tf.add_paragraph()
    p.text = "All satellite imagery retained in S3 Standard @ $0.023/GB.\nFor a 10 TB archive = $230.00 / month."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "IntelliArchive Dynamic Tiering:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_EMERALD
    p.space_before = Pt(14)
    p = tf.add_paragraph()
    p.text = "• 25% High (S3 Standard): 2.5 TB = $57.50\n• 35% Medium (S3 Standard-IA): 3.5 TB = $43.75\n• 40% Low (S3 Glacier): 4.0 TB = $16.00\n\nTotal Optimized = $117.25 / month"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "Net Projected Savings: 49.02%"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_CYAN
    p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 9: Containerization & Amazon ECR Verification
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Containerization & Amazon ECR Verification")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "DOCKER IMAGE OPTIMIZATION")
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    docker_bullets = [
        ("Base Image: ", "python:3.11-slim for minimal security attack surface."),
        ("PyTorch CPU Optimization: ", "Switched from default CUDA PyTorch wheel (5 GB) to CPU-only wheel (--index-url https://download.pytorch.org/whl/cpu)."),
        ("Model Pre-Caching: ", "CLIP ViT-B/32 weights downloaded during build time to eliminate cold-start latency."),
        ("Unprivileged User: ", "Runs as non-root user 'appuser' with least privilege."),
        ("Integrated Healthcheck: ", "Querying http://localhost:8080/ for zero-downtime container monitoring.")
    ]
    for i, (k, v) in enumerate(docker_bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "AMAZON ECR REGISTRY STATUS")
    tb = s9.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    ecr_bullets = [
        ("ECR Repository: ", "intelliarchive (Private)"),
        ("Registry URI: ", "371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive"),
        ("Pushed Image Tag: ", "cpu-test (Active & Verified in ECR)"),
        ("Image Size: ", "1.36 GB (Dramatic reduction from initial unoptimized ~12 GB image)"),
        ("Readiness: ", "Ready for immediate deployment to AWS ECS Fargate Task Definition.")
    ]
    for i, (k, v) in enumerate(ecr_bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_EMERALD
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 10: Automated Testing & Verification
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Automated Verification & Test Suite Audit")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3), "TEST SUITE EXECUTION SUMMARY — 41 / 41 TESTS PASSED (100%)")
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(11.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    test_modules = [
        ("test_lifecycle_storage.py (10 Tests Passed)", [
            "Validates storage tier acceptance (S3_STANDARD, S3_STANDARD_IA, S3_GLACIER)",
            "Enforces rejection of invalid storage tiers",
            "Verifies multi-hop migrations cleanly purge stale copies without data loss",
            "Ensures audit CSVs remain synchronized and atomic across concurrent transactions"
        ], COLOR_CYAN),
        ("test_s3_service.py (24 Tests Passed)", [
            "Tests upload success, custom object keys, and missing file error handling",
            "Validates paginated object listing and custom prefix filtering",
            "Ensures zero AWS credentials leak in client error messages",
            "Validates ECS IAM Task Role credential resolution with empty AWS_PROFILE"
        ], COLOR_EMERALD),
        ("test_web_app.py (7 Tests Passed)", [
            "Validates HTML rendering for Dashboard, Analyze, Archive, Analytics, and Architecture",
            "Tests /api/summary, /api/analytics, /api/lifecycle, and sample preview endpoints",
            "Verifies full end-to-end zero-shot CLIP inference via /api/analyze-sample"
        ], COLOR_AMBER)
    ]

    for mod_title, mod_tests, col in test_modules:
        p = tf.add_paragraph()
        p.text = mod_title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = col
        p.space_before = Pt(8)
        for t in mod_tests:
            p = tf.add_paragraph()
            p.text = f"   ✔  {t}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 11: Work Distribution & Team Contributions
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Work Distribution & Individual Contributions")

    # Member 1
    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "K. PAVAN KUMAR REDDY (24BIT0580)")
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p1_contribs = [
        ("Cloud Architecture Design: ", "Formulated S3 storage tier mapping and ECS Fargate deployment topology."),
        ("FastAPI Platform & UI: ", "Designed aerospace dark-theme UI, Jinja2 templates, Chart.js integrations, and REST endpoints."),
        ("AWS S3 Integration: ", "Implemented boto3 wrapper, IAM credential fallback, and live bucket listing/upload service."),
        ("Docker Containerization: ", "Authored Dockerfile, optimized CPU PyTorch wheel, and managed Amazon ECR registry push.")
    ]
    for i, (k, v) in enumerate(p1_contribs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    # Member 2
    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "ANHAD (24BIT0129)")
    tb = s11.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p2_contribs = [
        ("AI Foundation Model Pipeline: ", "Configured CLIP ViT-B/32 zero-shot classification and semantic prompt anchors."),
        ("Image Preprocessing: ", "Developed dynamic contrast stretching for 16-bit GeoTIFF satellite imagery."),
        ("Lifecycle Simulation Ledger: ", "Implemented atomic local directory tiering and CSV audit logging engines."),
        ("Testing & Cost Modeling: ", "Developed pytest test suites and built the analytical AWS cost comparison models.")
    ]
    for i, (k, v) in enumerate(p2_contribs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_EMERALD
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 12: Conclusion & Future Scope
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Conclusion & Future Roadmap")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3), "KEY PROJECT ACHIEVEMENTS")
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    achieves = [
        ("Proven Content-Aware Tiering: ", "Demonstrated that satellite semantic scoring avoids premature archival of high-value imagery."),
        ("Substantial Cost Savings: ", "Demonstrated up to 49% monthly cloud storage savings over static S3 Standard storage."),
        ("Dual-Mode Flexibility: ", "Seamlessly switches between offline local simulation and live Amazon S3 private cloud."),
        ("Production Packaging: ", "Lightweight, secure Docker container registered in Amazon ECR with 100% test pass rate.")
    ]
    for i, (k, v) in enumerate(achieves):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3), "FUTURE CLOUD EXTENSIONS")
    tb = s12.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    roadmap = [
        ("Amazon Bedrock Integration: ", "Utilize multimodal models (Claude 3.5 Sonnet / Amazon Titan) via AWS Bedrock API for cloud-native inference."),
        ("Amazon DynamoDB Metadata Index: ", "Migrate CSV ledgers to DynamoDB with global secondary indexes on semantic score and tier."),
        ("AWS EventBridge & Lambda: ", "Trigger automated inference asynchronously whenever new satellite images land in an S3 intake bucket."),
        ("Specialized Geospatial Models: ", "Incorporate RemoteCLIP or Earth Observation models fine-tuned on multispectral satellite bands.")
    ]
    for i, (k, v) in enumerate(roadmap):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + k
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_EMERALD
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 13: Q&A / Closing Slide
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)

    tb = s13.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "IntelliArchive: Intelligent Object Lifecycle Optimization for Satellite Archives"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(16)

    p = tf.add_paragraph()
    p.text = "Questions & Technical Discussion"
    p.font.size = Pt(16)
    p.font.italic = True
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(12)

    prs.save(str(OUTPUT_FILE))
    print(f"Presentation successfully created at: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
