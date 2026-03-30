# Final converted data

Converted PDF files in `results/2025` and `results/2026` with page-preserving structure.

## Repository policy for PR compatibility

This repository does **not** commit generated `.xlsx` files because the PR creation flow rejects binary artifacts.

## PR-friendly outputs (committable)

Generate CSV page folders (text files) with:

```bash
python convert_pdfs_to_excel.py --format csv
```

This produces:

- `results/2025/all_jnv_18012025_csv/` (`page_001.csv` ... `page_291.csv`)
- `results/2026/JNVs_13_dec_25_csv/` (`page_001.csv` ... `page_153.csv`)

## Optional local binary output (do not commit)

If you still need Excel locally:

```bash
python convert_pdfs_to_excel.py --format xlsx
```

Outputs:

- `results/2025/all_jnv_18012025.xlsx`
- `results/2026/JNVs_13_dec_25.xlsx`
