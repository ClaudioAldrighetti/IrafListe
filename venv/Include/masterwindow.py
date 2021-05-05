# import tkinter as tk
# import tkinter.ttk as ttk
# import tkinter

import makefiles as mf
import maketk as mtk
from utility import *
from winconfig import *


class MasterListWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Master List")

        if platform == "linux":
            self.geometryBase = WinGeometry(270, 65, 420, 370)
        else:
            self.geometryBase = WinGeometry(160, 60, 420, 370)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)
        self.configure(bg=FR_BG)

        self._errFlag = False

        # Master list
        self.listFrame = tk.Frame(self, bg=FR_BG)
        self.listFrame.pack()

        self.typeLabel = mtk.make_Label(self.listFrame, text="Type", column=1, pady=2, sticky=tk.EW)
        self.posesLabel = mtk.make_Label(self.listFrame, text="Poses", column=2, pady=2, sticky=tk.EW)
        self.timeLabel = mtk.make_Label(self.listFrame, text="Time", column=3, pady=2, sticky=tk.EW)

        self.typeEntries = []
        self.posesEntries = []
        self.timeEntries = []
        self.removeButtons = []

        # Generate master button
        self.genButton = mtk.make_Button(self, self.gen_master,
                                         text="Generate Master", pady=2, grid_flag=False, fill="x")

    # Create master dark and bias files
    def gen_master(self):
        print("GEN MASTER")

        ws_path = self.master.wsPath
        list_dim = self.master.masterListDim
        master_win = self.master.masterListWindow
        master_list = []

        for i in range(0, list_dim):
            master_type = master_win.typeEntries[i].get()
            master_poses = int(rm_spaces(master_win.posesEntries[i].get()))
            if master_type == DARK:
                master_time = int(rm_spaces(self.timeEntries[i].get()))
            else:
                bias_poses = master_poses
                master_time = None

            master_info = MasterInfo(master_type, master_poses, master_time)
            master_list.append(master_info)

        print("Creating master files...")
        mf.make_DARK(ws_path, master_list, list_dim)
        mf.make_ListaBias(ws_path, bias_poses)
        mf.make_CreaMasterDb(ws_path, master_list, list_dim)

        print("Master files have been created successfully")

        self.master.darkButton.configure(state=tk.DISABLED)
        self.master.darkPosesLabel.configure(state=tk.DISABLED)
        self.master.darkPosesEntry.configure(state=tk.DISABLED)
        self.master.darkTimeLabel.configure(state=tk.DISABLED)
        self.master.darkTimeEntry.configure(state=tk.DISABLED)

        self.master.biasButton.configure(state=tk.DISABLED)
        self.master.biasPosesLabel.configure(state=tk.DISABLED)
        self.master.biasPosesEntry.configure(state=tk.DISABLED)

        # Close master list window
        print("Closing master list window...")
        self.destroy()
        return
