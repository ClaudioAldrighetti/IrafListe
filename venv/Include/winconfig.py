# Windows configuration
from sys import platform
from utility import SpecInfo

# Spectrographs list with data (name, min_h_pixel, max_h_pixel, h_image, l_row)
SPEC_INFO = [
    SpecInfo("Alpy + ASI294", 10, 280, 281, 270),
    SpecInfo("LHIRESS + ATIK460ex", 10, 280, 281, 270)
]

# Entry height for win resizing
if platform == "linux":
    ENTRY_HEIGHT = 29
else:
    ENTRY_HEIGHT = 25

# Colors
COL_ERR = "Red"
COL_NORM = "White"
