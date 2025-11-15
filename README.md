# Hankyung Article Summarizer

This project processes weekly Hankyung news articles (in Korean) and produces:
- **CSV files** → structured dataset for future investment analysis
- **PDF reports** → clean, reader-friendly summaries for quick review

## ✨ Features
- Translates Korean articles into English summaries
- Auto-adjusts summary length based on article size
- Outputs both CSV (for data/analysis) and PDF (for reading/sharing)
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
uv add deep-translator reportlab tabulate
```

## 🚀 Usage
1. Save your Hankyung articles in a `.txt` file, separated by `--` lines.
2. Run the script:

```bash
uv run python main.py
```

3. Enter:
   - Year (e.g., `2025`)
   - Week number (e.g., `45`)
   - Path to your `.txt` file

4. Outputs:
   - `2025_week45_hankyung.csv` → structured dataset
   - `2025_week45_hankyung.pdf` → formatted report (auto-opens)

## 📂 Example Output
**PDF Table:**

| No. | English Summary |
|-----|-----------------|
| 1   | Exports in October rose 3.6% year-on-year, driven by semiconductors and ships... |
| 2   | Nvidia plans to turn Korea into a massive AI factory... |
| 3   | Data is the key to AI success... |

**CSV File:**
```csv
"Year","Week","English Summary"
"2025","45","Exports in October rose 3.6% year-on-year..."
"2025","45","Nvidia plans to turn Korea into a massive AI factory..."
```

## 📊 Why Keep CSVs?
- CSVs are your **data asset** for future investment analysis
- PDFs are for **reading/sharing**
- Over time, you’ll build a historical dataset of Hankyung summaries

## 📝 .gitignore
Make sure you don’t commit generated files:

```gitignore
.venv/
__pycache__/
*.py[cod]
*.csv
*.pdf
.DS_Store
```

## 📈 Future Ideas
- Auto-tag summaries by sector (semiconductors, shipping, AI, etc.)
- Correlate summaries with stock/ETF performance
- Add sentiment analysis