# EPRA Document Auto-Stamper

Digitally places your signature, company stamp, and handwritten-style date onto EPRA **Commencement of Work Notices** and **Completion Certificates** (including page 2 Installation Test Certificates) with full PDF compression and optimization.

---

## Quick Start (Windows)

1. **Clone or download** this repository onto your computer:
   ```bash
   git clone https://github.com/wxchira808/epra_stamper.git
   cd epra_stamper
   ```
2. **Copy your unstamped EPRA PDFs** directly into:
   ```
   completions and commencements/
   ```
3. **Double-click `run_stamper.bat`**:
   - On the very first run, it will automatically create a Python virtual environment (`.venv`) and install all required packages (`PyMuPDF`, `Pillow`).
   - It will automatically detect each document type, stamp Page 1 (and Page 2 for Completion Certificates), embed today's date in cursive blue ink, and apply PDF compression.
4. **Collect your stamped documents** inside:
   ```
   completions and commencements/output/
   ```

---

## Features

- **One-Click Automation**: Double-click `run_stamper.bat` on any Windows PC with Python installed. No manual terminal commands needed.
- **Auto-Detection**: Automatically detects whether each file is a Commencement of Work Notice or Completion Certificate and selects the right template.
- **Multi-Page Stamping**: For Completion Certificates with a second page (Installation Test Certificate), both Page 1 and Page 2 are automatically stamped and signed.
- **High Efficiency & Small File Size**: Output PDFs are compressed with stream deflation and garbage collection, reducing file size by ~92% (from ~5.5 MB down to ~430 KB) while keeping text selectable and crisp.
- **Cursive Blue Pen Matching**: Embedded cursive font (`Caveat-Regular.ttf`) sampled in deep navy blue ink matching the physical signature pen tone.
- **Git-Safe Workflow**: `.gitignore` is pre-configured to keep your input/output folders tracked without accidentally uploading private client PDFs to GitHub.

---

## Manual / Command-Line Usage

If you prefer using the command line:

```bash
# Setup environment (one time)
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Run batch stamping on 'completions and commencements' with today's date
.venv\Scripts\python stamper\batch.py

# Specify a custom date
.venv\Scripts\python stamper\batch.py 31/07/2026

# Stamp a single document
.venv\Scripts\python stamper\stamp.py input.pdf stamper/assets/signature_cropped.png stamper/assets/stamp_cropped.png 31/07/2026 output_signed.pdf
```

---

## Project Structure

```text
epra_stamper/
├── run_stamper.bat                 # One-click Windows runner
├── requirements.txt                # Python dependencies (pymupdf, pillow)
├── completions and commencements/  # Place unstamped PDFs here
│   ├── run_stamper.bat             # Convenience runner inside the folder
│   └── output/                     # Stamped PDFs land here
└── stamper/
    ├── batch.py                    # Batch processing engine
    ├── stamp.py                    # PDF stamping core
    ├── config.py                   # Coordinates and font/color settings
    ├── assets/                     # Signature and stamp image assets
    └── fonts/                      # Cursive handwriting font
```
