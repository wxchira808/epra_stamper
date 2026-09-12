"""
stamp.py
--------
Overlays a signature PNG, a stamp PNG, and a handwritten-style date onto an
EPRA Commencement Notice or Completion Certificate PDF, fully digitally —
no printing/scanning needed.

USAGE (single file):
    python3 stamp.py input.pdf signature.png stamp.png 29/07/2025 output.pdf

USAGE (batch — process every PDF in a folder):
    python3 batch.py input_folder/ signature.png stamp.png 29/07/2025 output_folder/
"""

import sys
import os
import fitz  # PyMuPDF
from config import TEMPLATES, CURSIVE_FONT_PATH, DATE_COLOR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def detect_template(page_text):
    # Normalize ligatures (e.g. "ﬁ" -> "fi") that some PDFs embed, which would
    # otherwise break plain substring matching.
    normalized = (
        page_text.replace("\ufb01", "fi")
        .replace("\ufb02", "fl")
        .lower()
    )
    for name, cfg in TEMPLATES.items():
        if cfg["match_text"].lower() in normalized:
            return name
    return None


def resolve_path(path):
    if os.path.isabs(path):
        return path
    return os.path.join(BASE_DIR, path)


def _apply_stamp(page, layout_cfg, signature_png, stamp_png, date_str):
    # --- Place signature ---
    sig = layout_cfg["signature"]
    sig_rect = fitz.Rect(sig["x"], sig["y"], sig["x"] + sig["width"], sig["y"] + sig["height"])
    page.insert_image(sig_rect, filename=signature_png, keep_proportion=True, overlay=True)

    # --- Place stamp ---
    stp = layout_cfg["stamp"]
    stamp_rect = fitz.Rect(stp["x"], stp["y"], stp["x"] + stp["width"], stp["y"] + stp["height"])
    page.insert_image(stamp_rect, filename=stamp_png, keep_proportion=True, overlay=True)

    # --- Place handwritten-style date inside the stamp's date box ---
    off = layout_cfg["date_offset"]
    date_x = stp["x"] + off["dx"]
    date_y = stp["y"] + off["dy"]

    font_path = resolve_path(CURSIVE_FONT_PATH)
    use_cursive = os.path.isfile(font_path)

    page.insert_text(
        (date_x, date_y),
        date_str,
        fontsize=layout_cfg["date_fontsize"],
        fontname="cursive-date" if use_cursive else "helv",
        fontfile=font_path if use_cursive else None,
        color=DATE_COLOR,
        render_mode=0,
    )


def stamp_pdf(input_pdf, signature_png, stamp_png, date_str, output_pdf, page_number=0):
    doc = fitz.open(input_pdf)
    page = doc[page_number]
    text = page.get_text()

    template_name = detect_template(text)
    if template_name is None:
        raise ValueError(
            f"Could not detect a known template in '{input_pdf}'. "
            f"Checked for: {[c['match_text'] for c in TEMPLATES.values()]}"
        )
    cfg = TEMPLATES[template_name]

    # --- Stamp primary page ---
    _apply_stamp(page, cfg, signature_png, stamp_png, date_str)

    # --- Stamp page 2 if configured and present ---
    if "page_2" in cfg and len(doc) > 1:
        _apply_stamp(doc[1], cfg["page_2"], signature_png, stamp_png, date_str)

    os.makedirs(os.path.dirname(output_pdf) or ".", exist_ok=True)
    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"[{template_name}] {os.path.basename(input_pdf)} -> {output_pdf}")
    return template_name


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 stamp.py input.pdf signature.png stamp.png DD/MM/YYYY output.pdf")
        sys.exit(1)
    input_pdf, signature_png, stamp_png, date_str, output_pdf = sys.argv[1:6]
    stamp_pdf(input_pdf, signature_png, stamp_png, date_str, output_pdf)
