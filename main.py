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
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer
)

# --- Text cleaning helper ---
def clean_text(text: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"</?(?!b|i)[^>]+>", "", text)
    return text.strip()

# --- Hybrid chunking helper ---
def chunk_text_safe(text: str, max_chars: int = 800, max_words: int = 120) -> list[str]:
    words = text.split()
    chunks, current = [], []
    for w in words:
        if (len(" ".join(current)) + len(w) + 1 > max_chars) or (len(current) >= max_words):
            if current:
                chunks.append(" ".join(current))
                current = []
        current.append(w)
    if current:
        chunks.append(" ".join(current))
    return chunks

def translate_text(text, translator):
    try:
        translation = translator.translate(text)
        return translation if translation else None
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return None

def open_in_default_app(file_path):
    try:
        if sys.platform.startswith("darwin"):
            subprocess.call(["open", file_path])
        elif sys.platform.startswith("win"):
            os.startfile(file_path)  # type: ignore[attr-defined]
        else:
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
    text_style = ParagraphStyle(
        "Text",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=6,
    )

    story = []

    # Header row
    header_tbl = Table(
        [[Paragraph("<b>No.</b>", styles["Normal"]),
          Paragraph("<b>English Translation</b>", styles["Normal"])]],
        colWidths=[15 * mm, None]
    )
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8c8c8")),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 12))

    # Each article
    for idx, translation_chunks in enumerate(rows, start=1):
        table_rows = []
        for sub_idx, chunk in enumerate(translation_chunks, start=1):
            safe_text = clean_text(chunk or "")
            label = f"{idx}-{sub_idx}" if len(translation_chunks) > 1 else str(idx)
            table_rows.append([Paragraph(label, styles["Normal"]),
                               Paragraph(safe_text, text_style)])

        # Create table for this article
        article_tbl = Table(table_rows, colWidths=[20 * mm, None])
        article_tbl.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8c8c8")),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ]))
        story.append(article_tbl)
        story.append(Spacer(1, 12))

    title_text = f"Hankyung article translations — Year {year}, Week {week}"
    doc.build(
        story,
        onFirstPage=lambda canvas, doc: header_footer(canvas, doc, title_text),
        onLaterPages=lambda canvas, doc: header_footer(canvas, doc, title_text),
    )

def main():
    print("📂 Hankyung Article Logger")

    txt_file = input("Enter the path to your TXT file (e.g., raw_txt/2025_week45.txt): ").strip()
    if not os.path.exists(txt_file):
        print(f"❌ TXT file not found at {txt_file}")
        return

    year = input("Enter the year: ").strip()
    week = input("Enter the week number (e.g., 45): ").strip()

    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split articles by any number of dashes
    articles = [a.strip() for a in re.split(r"-{2,}", content) if a.strip()]
    translator = GoogleTranslator(source="ko", target="en")

    os.makedirs("csv_data", exist_ok=True)
    os.makedirs("pdf_reports", exist_ok=True)

    output_csv = os.path.join("csv_data", f"{year}_week{week}_hankyung.csv")
    output_pdf = os.path.join("pdf_reports", f"{year}_week{week}_hankyung.pdf")

    rows = []
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        import csv
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["No.", "English Translation"])

        for idx, article in enumerate(articles, start=1):
            print(f"\nProcessing Article {idx}...")
            chunks = chunk_text_safe(article, max_chars=800, max_words=120)
            translated_chunks = []
            for sub_idx, chunk in enumerate(chunks, start=1):
                translation = translate_text(chunk, translator)
                if translation:
                    label = f"{idx}-{sub_idx}" if len(chunks) > 1 else str(idx)
                    writer.writerow([label, translation])
                    translated_chunks.append(translation)
                else:
                    print(f"⚠️ Article {idx}-{sub_idx} translation failed or empty — skipped.")
            if translated_chunks:
                rows.append(translated_chunks)

    build_pdf(output_pdf, year, week, rows)
    open_in_default_app(output_pdf)

    print(f"\n✅ Done! CSV saved to {output_csv}, PDF saved to {output_pdf} and opened.")

if __name__ == "__main__":
    main()
