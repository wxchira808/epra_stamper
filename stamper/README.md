# EPRA Document Auto-Stamper

Digitally places your signature, company stamp, and a handwritten-style date
onto Commencement of Work Notices and Completion Certificates — no print,
sign, scan cycle needed. Works on Ubuntu and Windows (same Python script).

This copy is already calibrated and tested against YOUR actual signature and
stamp (in `assets/`) and a cursive font is already bundled in `fonts/` — you
can start stamping documents immediately.

## 1. One-time setup

### Install Python (skip if you already have it)
- Ubuntu: usually pre-installed. Check with `python3 --version`.
- Windows: download from https://python.org (tick "Add to PATH" during install).

### Install the one required library
```bash
python3 -m venv .venv
.venv/bin/pip install pymupdf
```
(Windows: `python -m venv .venv` then `.venv\Scripts\pip install pymupdf`.)

That's it — no other setup needed. Your signature/stamp images and the
cursive date font are already in this folder.

## 2. Stamp a single document
```bash
.venv/bin/python stamper/stamp.py input.pdf stamper/assets/signature_cropped.png stamper/assets/stamp_cropped.png 29/07/2025 output_signed.pdf
```
The script automatically detects whether `input.pdf` is a Commencement
Notice or Completion Certificate and applies the right template.

## 3. Batch-stamp a whole folder
Put all your unsigned PDFs in `input/`, then run:
```bash
.venv/bin/python stamper/batch.py
```
Every PDF in `input/` gets processed; results land in `input/output/` with
`_signed` added to each filename. Mixed folders (some commencement, some
completion) work fine — each is auto-detected individually.

If you need a different stamping date, pass it directly:
```bash
.venv/bin/python stamper/batch.py 29/07/2025
```
Or, for full manual control, keep the older explicit form:
```bash
.venv/bin/python stamper/batch.py input/ stamper/assets/signature_cropped.png stamper/assets/stamp_cropped.png 29/07/2025 output/
```

If a particular file's date differs from the rest, just run `stamp.py` on
that one file separately with its own date.

## 4. Re-calibrate (only if EPRA changes the form layout)
```bash
.venv/bin/python stamper/calibrate.py your_sample.pdf grid_preview.png
```
Open `grid_preview.png` — it shows a ruler grid in points over the document.
Read off the x,y where you want the top-left of the signature/stamp, and
update the matching block in `config.py`.

## Files in this project
| File | Purpose |
|---|---|
| `assets/signature.png`, `assets/stamp.png` | Your original uploaded images |
| `assets/signature_cropped.png`, `assets/stamp_cropped.png` | Same images, auto-cropped to remove excess transparent margin — use these for stamping, they place more accurately |
| `fonts/Caveat-Regular.ttf` | Cursive font used for the handwritten date |
| `config.py` | Coordinates for where signature/stamp/date go on each template, already calibrated to your assets |
| `stamp.py` | Stamps one PDF |
| `batch.py` | Stamps every PDF in a folder |
| `calibrate.py` | Generates a ruler-grid image to help you read off coordinates if you ever need to adjust |
| `input/output/` | Default destination for newly stamped PDFs |
| `sample_output/` | Example outputs already generated from your two sample PDFs, so you can see exactly what it produces |

## Notes
- The date color is sampled directly from your signature's ink (deep navy
  blue, ~RGB 24,30,101), so it visually matches your blue pen.
- Output PDFs stay text-based (not flattened to images), so file size stays
  small and the original text remains selectable/searchable.
- If a PDF doesn't match either template (e.g. a different EPRA form), the
  script will skip it and tell you, rather than guessing wrong placement.
- Want a third template (e.g. a different certificate type)? Just send me a
  sample PDF and I'll add it to `config.py`.
