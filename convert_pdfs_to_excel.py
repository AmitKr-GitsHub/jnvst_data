from __future__ import annotations

import argparse
from pathlib import Path
import csv

import pdfplumber
import pandas as pd

BASE_DIR = Path("results")
DEFAULT_YEARS = ["2025", "2026"]


def clean_table(table):
    cleaned = []
    for row in table:
        if row is None:
            continue
        normalized = [((cell or "").replace("\n", " ").strip()) for cell in row]
        if any(cell != "" for cell in normalized):
            cleaned.append(normalized)
    return cleaned


def page_rows(page):
    tables = page.extract_tables() or []
    if not tables:
        text = (page.extract_text() or "").strip()
        lines = text.splitlines() if text else []
        return [[line] for line in lines], ["text"]

    blocks = []
    max_cols = 0
    for table in tables:
        cleaned = clean_table(table)
        if not cleaned:
            continue
        max_cols = max(max_cols, max(len(r) for r in cleaned))
        blocks.append(cleaned)

    if not blocks:
        return [], ["text"]

    combined_rows = []
    for block in blocks:
        for row in block:
            if len(row) < max_cols:
                row = row + [""] * (max_cols - len(row))
            combined_rows.append(row)
        combined_rows.append([""] * max_cols)

    if combined_rows and all(cell == "" for cell in combined_rows[-1]):
        combined_rows.pop()

    columns = [f"col_{j:02d}" for j in range(1, max_cols + 1)]
    return combined_rows, columns


def convert_pdf_to_xlsx(pdf_path: Path, output_path: Path):
    with pdfplumber.open(pdf_path) as pdf, pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for i, page in enumerate(pdf.pages, start=1):
            rows, columns = page_rows(page)
            df = pd.DataFrame(rows, columns=columns)
            df.to_excel(writer, index=False, sheet_name=f"page_{i:03d}")


def convert_pdf_to_csv_pages(pdf_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            rows, columns = page_rows(page)
            csv_path = output_dir / f"page_{i:03d}.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)


def convert(pdf_path: Path, fmt: str):
    if fmt == "xlsx":
        output_path = pdf_path.with_suffix(".xlsx")
        convert_pdf_to_xlsx(pdf_path, output_path)
        return output_path

    output_dir = pdf_path.with_suffix("")
    output_dir = output_dir.parent / f"{output_dir.name}_csv"
    convert_pdf_to_csv_pages(pdf_path, output_dir)
    return output_dir


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Convert PDF result files into structured outputs. "
            "Use --format xlsx for binary Excel output or --format csv for PR-friendly text output."
        )
    )
    parser.add_argument("--years", nargs="+", default=DEFAULT_YEARS, help="Year folders under results/ to process")
    parser.add_argument("--format", choices=["xlsx", "csv"], default="csv", help="Output format (default: csv for PR-safe, non-binary output)")
    return parser.parse_args()


def main():
    args = parse_args()
    converted = []
    for year in args.years:
        year_dir = BASE_DIR / year
        for pdf_path in sorted(year_dir.glob("*.pdf")):
            out = convert(pdf_path, args.format)
            converted.append((pdf_path, out))
            print(f"Converted: {pdf_path} -> {out}")

    print("\nSummary:")
    for src, dst in converted:
        print(f"- {src} => {dst}")


if __name__ == "__main__":
    main()
