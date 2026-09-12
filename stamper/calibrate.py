"""
calibrate.py
------------
Draws a coordinate grid over a PDF page and saves it as a PNG image, so you can
visually read off the (x, y) pixel position of the signature, stamp, and date
box on each template. PDF coordinates start at (0,0) top-left here, in points
(1 point = 1/72 inch), matching what PyMuPDF expects.

Usage:
    python3 calibrate.py input.pdf output_grid.png
"""

import sys
import fitz  # PyMuPDF


def calibrate(pdf_path, out_png, page_number=0, grid_step=50, zoom=2.0):
    doc = fitz.open(pdf_path)
    page = doc[page_number]

    # Render page to an image at higher resolution for clarity
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Draw grid lines + labels directly on the PDF page first (in PDF point space),
    # then re-render, so the labels correspond to true PDF coordinates (not pixels).
    width, height = page.rect.width, page.rect.height

    shape = page.new_shape()
    for x in range(0, int(width) + 1, grid_step):
        shape.draw_line((x, 0), (x, height))
        page.insert_text((x + 2, 10), str(x), fontsize=6, color=(1, 0, 0))
    for y in range(0, int(height) + 1, grid_step):
        shape.draw_line((0, y), (width, y))
        page.insert_text((2, y + 8), str(y), fontsize=6, color=(0, 0, 1))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.4)
    shape.commit()

    pix = page.get_pixmap(matrix=mat)
    pix.save(out_png)
    print(f"Saved grid overlay: {out_png}")
    print(f"Page size (points): {width:.0f} x {height:.0f}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 calibrate.py input.pdf output_grid.png [page_number]")
        sys.exit(1)
    page_num = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    calibrate(sys.argv[1], sys.argv[2], page_num)
