# Windows configuration
from sys import platform
import tkinter as tk
import tkinter.ttk as ttk

from utility import SpecInfo

# ttk.Style is configured in main

# Spectrographs list with data (name, min_h_pixel, max_h_pixel, h_image, l_row)
SPEC_INFO = [
    SpecInfo("Alpy + ASI294", 10, 280, 281, 270),
    SpecInfo("LHIRESS + ATIK460ex", 10, 280, 281, 270)
]

# Star List Window Entry height for win resizing
if platform == "linux":
    STARL_EN_HG = 34
else:
    STARL_EN_HG = 30

# General
GEN_FG = "#dadada"

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

# Option Menù style
OM_STYLE = "Optionmenu.TMenubutton"
OM_BG = EN_BG
OM_FG = GEN_FG
OM_ABG = BT_ABG  # Active background color
OM_BDC = BT_BDC
OM_BDT = 1

# Labels style
LB_BG = FR_BG
LB_FG = GEN_FG
