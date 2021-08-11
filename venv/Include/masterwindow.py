import tkinter as tk
import os
#import os.path as opt

import makefiles as mf
import maketk as mtk
from utility import *
from winconfig import *


class MasterListWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Master List")

        self.defGeometry = MASTER_WIN_DEF_GEOM
        self.geometry(str(self.defGeometry))
        self.resizable(False, False)
        self.configure(bg=FR_BG)
        self.protocol("WM_DELETE_WINDOW", self.close)

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

        return

    # Create master dark and bias files
    def gen_master(self):
        print("GEN MASTER")

        # Check workspace directory
        ws_path = self.master.wsPath
        if not os.path.exists(ws_path):
            print("Error: workspace directory doesn't exist!")
            return

        list_dim = self.master.masterListDim
        master_win = self.master.masterListWindow
        master_list = []
        dark_flag = False
        bias_flag = False

        print("Retrieving masters data...")
        for i in range(0, list_dim):
            master_type = master_win.typeEntries[i].get()
            master_poses = int(rm_spaces(master_win.posesEntries[i].get()))
            if master_type == DARK:
                master_time = int(rm_spaces(self.timeEntries[i].get()))
                master_info = MasterInfo(master_type, master_poses, master_time)
                dark_flag = True
            else:
                bias_poses = master_poses
                master_info = MasterInfo(master_type, master_poses, None)
                bias_flag = True
            master_list.append(master_info)

        # There must be both master types
        if not (dark_flag and bias_flag):
            print("Error: there must be both master bias and master dark in the master list!")
            return

        print("Creating master files...")
        mf.make_DARK(ws_path, master_list, list_dim)
        mf.make_ListaBias(ws_path, bias_poses)
        mf.make_CreaMasterDb(ws_path, master_list, list_dim)

        # Ensure the file lista_inizio to contain the master command at the second line if it has already been created
        lista_inizio_path = os.path.join(ws_path, "lista_inizio.txt")
        if os.path.isfile(lista_inizio_path):
            print("Adding master command to lista_inizio.txt file...")
            os.remove(lista_inizio_path)
            mf.make_ListaInizio(ws_path, True)

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

    def close(self):
        # Delete star list information
        print("Deleting master list information...")
        self.master.masterListDim = 0
        self.master.masterFlag = False

        self.master.biasButton.configure(state=tk.NORMAL)
        self.master.biasPosesLabel.configure(state=tk.NORMAL)
        self.master.biasPosesEntry.configure(state=tk.NORMAL)

        # Check workspace directory
        ws_path = self.master.wsPath
        if not os.path.exists(ws_path):
            print("Error: workspace directory doesn't exist!")
            return

        # Delete the master command from lista_inizio if it has already been created
        lista_inizio_path = os.path.join(ws_path, "lista_inizio.txt")
        if os.path.isfile(lista_inizio_path):
            print("Removing master command from lista_inizio.txt file...")
            os.remove(lista_inizio_path)
            mf.make_ListaInizio(ws_path, False)

        # Close master list window
        print("Closing master list window...")
        self.master.masterListWindow = None
        self.destroy()
        return
