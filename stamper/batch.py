"""
batch.py
--------
Batch-stamps every PDF in the local `input/` folder and writes the signed
files to `output/`.

Default layout:
    ./input/   -> unsigned PDFs
    ./output/  -> stamped PDFs

You can still override the folders, assets, and date from the command line
if you need to.
"""

import glob
import os
import sys
from datetime import datetime

from stamp import stamp_pdf


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)


def get_default_input_dir():
    candidates = [
        os.path.join(PROJECT_ROOT, "completions and commencements"),
        os.path.join(PROJECT_ROOT, "completions and commencments"),
        os.path.join(BASE_DIR, "input"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return os.path.join(PROJECT_ROOT, "completions and commencements")


DEFAULT_SIGNATURE = os.path.join(BASE_DIR, "assets", "signature_cropped.png")
DEFAULT_STAMP = os.path.join(BASE_DIR, "assets", "stamp_cropped.png")


def batch_stamp(
    input_folder=None,
    signature_png=DEFAULT_SIGNATURE,
    stamp_png=DEFAULT_STAMP,
    date_str=None,
    output_folder=None,
):
    if input_folder is None:
        input_folder = get_default_input_dir()

    if output_folder is None:
        output_folder = os.path.join(input_folder, "output")

    if date_str is None or date_str == "" or date_str.lower() == "today":
        date_str = datetime.now().strftime("%d/%m/%Y")

    pdf_files = sorted(glob.glob(os.path.join(input_folder, "*.pdf")))
    if not pdf_files:
        print(f"No PDF files found in {input_folder}")
        return

    os.makedirs(output_folder, exist_ok=True)
    succeeded, failed = [], []

    for pdf_path in pdf_files:
        out_name = os.path.splitext(os.path.basename(pdf_path))[0] + "_signed.pdf"
        out_path = os.path.join(output_folder, out_name)
        try:
            stamp_pdf(pdf_path, signature_png, stamp_png, date_str, out_path)
            succeeded.append(pdf_path)
        except Exception as e:
            print(f"  SKIPPED {os.path.basename(pdf_path)}: {e}")
            failed.append(pdf_path)

    print(f"\nDone. {len(succeeded)} stamped, {len(failed)} skipped.")
    if failed:
        print("Skipped files:")
        for f in failed:
            print(f"  - {f}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        batch_stamp()
    elif len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            batch_stamp(input_folder=sys.argv[1])
        else:
            batch_stamp(date_str=sys.argv[1])
    elif len(sys.argv) == 6:
        batch_stamp(*sys.argv[1:6])
    else:
        print(
            "Usage: python3 batch.py [DD/MM/YYYY | input_folder signature.png stamp.png DD/MM/YYYY output_folder]"
        )
        sys.exit(1)
