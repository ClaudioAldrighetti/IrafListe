# Windows configuration and widgets layout
from sys import platform
from tkinter import FLAT

from utility import WinGeometry

# Windows size and offset
if platform == "linux":
    # Linux distribution configuration
    MAIN_WIN_DEF_GEOM = WinGeometry(420, 500, 100, 100)     # Main Window configuration
    MASTER_WIN_DEF_GEOM = WinGeometry(270, 55, 420, 370)    # Master List Window configuration
    STAR_WIN_DEF_GEOM = WinGeometry(545, 105, 420, 100)     # Star List Window configuration
    SPEC_WIN_DEF_GEOM = WinGeometry(245, 260, 420, 250)     # Spectrographs Setting Window configuration
    STARL_EN_HG = 45                                        # (Star) List Entry
else:
    # Windows or other
    MAIN_WIN_DEF_GEOM = WinGeometry(300, 370, 100, 100)
    MASTER_WIN_DEF_GEOM = WinGeometry(160, 60, 420, 370)
    STAR_WIN_DEF_GEOM = WinGeometry(390, 85, 420, 100)
    SPEC_WIN_DEF_GEOM = WinGeometry(175, 170, 420, 250)
    STARL_EN_HG = 30
MASTERL_EN_HG = STARL_EN_HG                                 # (Master) List Entry

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
BT_REL = FLAT       # Relief

# Entries style
EN_BG = "#454545"
EN_FG = GEN_FG
EN_INS = "#f0f0f0"

# Option Menu style
OM_STYLE = "Optionmenu.TMenubutton"
OM_BG = EN_BG
OM_FG = GEN_FG
OM_ABG = BT_ABG  # Active background color
OM_BDC = BT_BDC
OM_BDT = 1

# Checkbutton style
CB_BG = FR_BG
CB_FG = BT_FG
CB_SELC = BT_BG
CB_ABC = FR_BG
CB_AFC = BT_FG

# Labels style
LB_BG = FR_BG
LB_FG = GEN_FG

# Separators style
SEP_STYLE = "MySep.TSeparator"
SEP_BG = "#595959"
SEP_HGT = 2
