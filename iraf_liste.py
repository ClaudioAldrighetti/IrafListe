from tkinter import ttk

from mainwindow import MainWindow
from winconfig import *


if __name__ == "__main__":
    # Main window
    mainFrame = MainWindow()

    # ttk style
    style = ttk.Style(mainFrame)
    style.configure(OM_STYLE, background=OM_BG, foreground=OM_FG)
    style.configure(SEP_STYLE, background=GEN_FG)

    # Run application
    mainFrame.mainloop()
