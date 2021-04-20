# Windows configuration
from sys import platform

# Entry height for win resizing
if platform == "linux":
    ENTRY_HEIGHT = 29
else:
    ENTRY_HEIGHT = 25

# Colors
COL_ERR = "Red"
COL_NORM = "White"
