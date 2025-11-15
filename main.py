import os
import re
import sys
import subprocess
from datetime import datetime

from deep_translator import GoogleTranslator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

def summarize_text(text, translator):
    try:
        translation = translator.translate(text)
        sentences = [s.strip() for s in translation.split(".") if s.strip()]
        word_count = len(translation.split())

        if word_count < 100:
            length = 2
        elif word_count < 300:
            length = 3
        elif word_count < 600:
            length = 4
        else:
            length = 5

        summary_sentences = sentences[:length]
        summary = ". ".join(summary_sentences)
        if summary and not summary.endswith("."):
            summary += "."
        return summary if summary else None
    except Exception as e:
        print(f"⚠️ Summarization failed: {e}")
        return None

def open_in_default_app(file_path):
    try:
        if sys.platform.startswith("darwin"):  # macOS
            subprocess.call(["open", file_path])
        elif sys.platform.startswith("win"):   # Windows
            os.startfile(file_path)  # type: ignore[attr-defined]
        else:  # Linux/Unix
            subprocess.call(["xdg-open", file_path])
    except Exception as e:
        print(f"⚠️ Could not open automatically: {e}")

def header_footer(canvas, doc, title_text):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(20 * mm, (A4[1] - 15 * mm), title_text)
    canvas.setFont("Helvetica", 9)
    page_str = f"Page {doc.page}"
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, page_str)
    canvas.restoreState()

def build_pdf(output_pdf, year, week, rows):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    summary_style = ParagraphStyle(
        "Summary",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=6,
    )

    story = []

    # Table data with numbering only
    table_data = []
    table_data.append([
        Paragraph("<b>No.</b>", styles["Normal"]),
        Paragraph("<b>English summary</b>", styles["Normal"]),
    ])

    for idx, summary in enumerate(rows, start=1):
        table_data.append([
            Paragraph(str(idx), styles["Normal"]),
            Paragraph(summary, summary_style),
        ])

    tbl = Table(table_data, colWidths=[15 * mm, None])
    tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfbfb")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8c8c8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(tbl)

    title_text = f"Hankyung article summaries — Year {year}, Week {week}"
    doc.build(
        story,
        onFirstPage=lambda canvas, doc: header_footer(canvas, doc, title_text),
        onLaterPages=lambda canvas, doc: header_footer(canvas, doc, title_text),
    )

def main():
    print("📂 Hankyung Article Logger")

    # Prompt for TXT file path
    txt_file = input("Enter the path to your TXT file (e.g., raw_txt/2025_week45.txt): ").strip()
    if not os.path.exists(txt_file):
        print(f"❌ TXT file not found at {txt_file}")
        return

    year = input("Enter the year: ").strip()
    week = input("Enter the week number (e.g., 45): ").strip()

    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    articles = [a.strip() for a in re.split(r"-{2,}", content) if a.strip()]
    translator = GoogleTranslator(source="ko", target="en")

    # Ensure output folders exist
    os.makedirs("csv_data", exist_ok=True)
    os.makedirs("pdf_reports", exist_ok=True)

    # Output paths
    output_csv = os.path.join("csv_data", f"{year}_week{week}_hankyung.csv")
    output_pdf = os.path.join("pdf_reports", f"{year}_week{week}_hankyung.pdf")

    rows = []
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        import csv
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["No.", "English Summary"])

        for idx, article in enumerate(articles, start=1):
            print(f"\nProcessing Article {idx}...")
            summary = summarize_text(article, translator)
            if summary:
                writer.writerow([idx, summary])
                rows.append(summary)

    # Build PDF
    build_pdf(output_pdf, year, week, rows)

    # Auto-open PDF
    open_in_default_app(output_pdf)

    print(f"\n✅ Done! CSV saved to {output_csv}, PDF saved to {output_pdf} and opened.")

if __name__ == "__main__":
    main()
