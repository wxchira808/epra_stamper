"""
config.py
---------
One entry per document template. Coordinates are in PDF points (top-left
origin), the same units shown on the grid images from calibrate.py.

HOW TO ADJUST:
  1. Run calibrate.py on a fresh sample of that document type.
  2. Open the resulting *_grid.png and read off the x,y where you want the
     top-left corner of the signature/stamp to sit.
  3. Update the numbers below. width/height control how big the image is
     drawn (keep the aspect ratio close to your actual PNG to avoid
     stretching).
  4. date_offset is measured from the stamp's top-left corner (x, y) to
     where the date text should sit INSIDE the stamp's date box.
"""

TEMPLATES = {
    "commencement": {
        # text used to auto-detect this template in a PDF
        "match_text": "COMMENCEMENT OF WORK NOTICE",

        "signature": {
            "x": 210, "y": 467, "width": 138, "height": 44,
        },
        "stamp": {
            "x": 430, "y": 441, "width": 160, "height": 87,
        },
        # where the date text sits relative to the stamp's top-left corner
        # (calibrated against the actual stamp PNG's "Date ....." line)
        "date_offset": {"dx": 52, "dy": 47},
        "date_fontsize": 18,
    },

    "completion": {
        "match_text": "Completion Certificate",

        "signature": {
            "x": 160, "y": 486, "width": 116, "height": 37,
        },
        "stamp": {
            "x": 354, "y": 558, "width": 160, "height": 87,
        },
        "date_offset": {"dx": 52, "dy": 47},
        "date_fontsize": 18,

        # Page 2 (Installation Test Certificate table)
        "page_2": {
            "signature": {
                "x": 160, "y": 240, "width": 116, "height": 37,
            },
            "stamp": {
                "x": 354, "y": 240, "width": 160, "height": 87,
            },
            "date_offset": {"dx": 52, "dy": 47},
            "date_fontsize": 18,
        },
    },
}

# Path to a handwriting/cursive TTF font for the date text.
# Download a free one (e.g. "Caveat" or "Homemade Apple" from Google Fonts:
# https://fonts.google.com/) and point this at the .ttf file.
CURSIVE_FONT_PATH = "fonts/Caveat-Regular.ttf"

# Date ink color, sampled directly from the actual signature PNG so the date
# matches the blue pen tone of the signature. (R, G, B) as 0-1 floats.
DATE_COLOR = (0.095, 0.117, 0.395)

# Date format shown in the stamp's date box, e.g. 29/07/2025
DATE_FORMAT = "%d/%m/%Y"
