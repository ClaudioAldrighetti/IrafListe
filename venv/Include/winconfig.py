# Windows configuration, widgets layout and spectrographs data
from sys import platform
import tkinter as tk

from utility import SpecInfo, WinGeometry

# Spectrographs list with data (name, min_h_pixel, max_h_pixel, h_image, l_row)
SPEC_INFO = [
    SpecInfo("Alpy + ASI294", 10, 280, 281, 270),
    SpecInfo("LHIRESS + ATIK460ex", 10, 280, 281, 270)
]

# Windows size and offset
if platform == "linux":
    # Linux distribution configuration
    MAIN_WIN_DEF_GEOM = WinGeometry(390, 435, 100, 100)
    MASTER_WIN_DEF_GEOM = WinGeometry(270, 65, 420, 370)
    STAR_WIN_DEF_GEOM = WinGeometry(510, 90, 420, 100)
else:
    # Windows or other
    MAIN_WIN_DEF_GEOM = WinGeometry(300, 335, 100, 100)
    MASTER_WIN_DEF_GEOM = WinGeometry(160, 60, 420, 370)
    STAR_WIN_DEF_GEOM = WinGeometry(390, 85, 420, 100)

# Star List Window Entry height for win resizing
if platform == "linux":
    STARL_EN_HG = 34
else:
    STARL_EN_HG = 30
MASTERL_EN_HG = STARL_EN_HG

# General
GEN_FG = "#dadada"

# Menu bar style
MN_BG = "#555555"

# Frames style
FR_BG = "#505050"

# Buttons style
BT_BG = "#484848"   # Background color
BT_ABG = "#5184e4"  # Active background color
BT_FG = GEN_FG      # Foreground color
BT_BDC = "#b0b0b0"  # Border color
BT_BDT = 2          # Border dimension
BT_REL = tk.FLAT    # Relief

# Entries style
EN_BG = "#454545"
EN_FG = GEN_FG
EN_INS = "#f0f0f0"
COL_ERR = "Red"

# Option Menu style
OM_STYLE = "Optionmenu.TMenubutton"
OM_BG = EN_BG
OM_FG = GEN_FG
OM_ABG = BT_ABG  # Active background color
OM_BDC = BT_BDC
OM_BDT = 1

# Labels style
LB_BG = FR_BG
LB_FG = GEN_FG

# Separators style
SEP_STYLE = "MySep.TSeparator"
SEP_BG = "#595959"
SEP_HGT = 2
