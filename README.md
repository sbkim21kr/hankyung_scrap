# Hankyung Article Summarizer

This project processes weekly Hankyung news articles (in Korean) and produces:
- **CSV files** → structured datasets for future investment analysis
- **PDF reports** → clean, reader-friendly summaries for quick review

## ✨ Features
- Translates Korean articles into English summaries
- Auto-adjusts summary length based on article size
- Prompts for TXT file path (e.g., `raw_txt/2025_week45.txt`)
- Outputs both CSV (for data/analysis) and PDF (for reading/sharing)
- Automatically creates `csv_data/` and `pdf_reports/` folders if missing
- Neat PDF formatting with numbered summaries, headers/footers
- Skips unavailable summaries (no clutter)
- Auto-opens the PDF in your default viewer

## 🛠 Requirements
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management

## 📦 Installation
Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/hankyung-summarizer.git
cd hankyung-summarizer
uv add deep-translator reportlab
```

## 🚀 Usage
1. Save your Hankyung articles in a `.txt` file, separated by `--` lines.
   - Example: `raw_txt/2025_week45.txt`
2. Run the script:

```bash
uv run python main.py
```

3. Enter:
   - Path to your TXT file (e.g., `raw_txt/2025_week45.txt`)
   - Year (e.g., `2025`)
   - Week number (e.g., `45`)

4. Outputs:
   - `csv_data/2025_week45_hankyung.csv` → structured dataset
   - `pdf_reports/2025_week45_hankyung.pdf` → formatted report (auto-opens)

## 📂 Folder Structure
```
hankyung-summarizer/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
│
├── raw_txt/        # raw source files (Samsung Note exports)
├── pdf_reports/    # generated PDFs for reading
└── csv_data/       # structured CSVs for analysis
```

## 📂 Example Output
**PDF Table:**

| No. | English Summary |
|-----|-----------------|
| 1   | Exports in October rose 3.6% year-on-year, driven by semiconductors and ships... |
| 2   | Nvidia plans to turn Korea into a massive AI factory... |

**CSV File:**
```csv
"No.","English Summary"
"1","Exports in October rose 3.6% year-on-year..."
"2","Nvidia plans to turn Korea into a massive AI factory..."
```

## 📝 .gitignore
Make sure you don’t commit generated files:

```gitignore
.venv/
__pycache__/
*.py[cod]
*.csv
*.pdf
.DS_Store
Thumbs.db
```

## 📈 Future Ideas
- Auto-tag summaries by sector (semiconductors, shipping, AI, etc.)
- Correlate summaries with stock/ETF performance
- Add sentiment analysis
