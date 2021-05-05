# import tkinter as tk
# from tkinter import filedialog as fd
# import tkinter.ttk as ttk
import os

import makefiles as mf
import maketk as mtk
from utility import *
from winconfig import *


# Star list window class
class StarListWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Star List")

        if platform == "linux":
            self.geometryBase = WinGeometry(510, 90, 420, 100)
        else:
            self.geometryBase = WinGeometry(390, 85, 420, 100)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)
        self.configure(bg=FR_BG)

        self._errFlag = False

        # Star list
        self.listFrame = tk.Frame(self, bg=FR_BG)
        self.listFrame.grid()

        self.starLabel = mtk.make_Label(self.listFrame, text="Star", column=1, pady=2, sticky=tk.EW)
        self.poseLabel = mtk.make_Label(self.listFrame, text="Poses", column=2, pady=2, sticky=tk.EW)
        self.flatLabel = mtk.make_Label(self.listFrame, text="Flat", column=3, pady=2, sticky=tk.EW)
        self.neonLabel = mtk.make_Label(self.listFrame, text="Neon", column=4, pady=2, sticky=tk.EW)
        self.darkLabel = mtk.make_Label(self.listFrame, text="Dark T", column=5, pady=2, sticky=tk.EW)
        self.standardLabel = mtk.make_Label(self.listFrame, text="Standard", column=6, pady=2, sticky=tk.EW)

        self.starEntries = []
        self.poseEntries = []
        self.flatEntries = []
        self.neonEntries = []
        self.darkEntries = []
        self.standardEntries = []
        self.removeButtons = []

        # Ref frame
        self.refFrame = tk.Frame(self, bg=FR_BG)
        self.refFrame.grid()

        self.refLabel = mtk.make_Label(self.refFrame, text="REF: ", padx=2, state=tk.DISABLED)
        self.refEntry = mtk.make_Entry(self.refFrame, column=1, padx=2, sticky=tk.EW, state=tk.DISABLED)
        self.refPoseLabel = mtk.make_Label(self.refFrame, text="REF pose: ", column=2, padx=2, state=tk.DISABLED)
        self.refPoseEntry = mtk.make_Entry(self.refFrame, width=5, column=3, padx=2, sticky=tk.EW, state=tk.DISABLED)

        # Start button
        self.startButton = mtk.make_Button(self, self.start_session, text="Start Session", row=2, pady=2)

    # Create general IRAF files
    def start_session(self):
        print("START SESSION")

        ref_pose_str = rm_spaces(self.refPoseEntry.get())
        master_flag = self.master.masterFlag
        self.master.starList = []

        print("Checking environment...")
        # Check workspace directory
        if not os.path.exists(self.master.wsPath):
            print("Error: workspace directory doesn't exist!")
            self._errFlag = True
        ws_path = self.master.wsPath

        # Check star list length
        if self.master.listDim == 0:
            print("Error: star list is empty!")
            self._errFlag = True
        list_dim = self.master.listDim

        # Check reference pose
        if not ref_pose_str or int(ref_pose_str) <= 0:
            print("Error: illegal reference pose value!")
            self.refPoseEntry.configure(bg=COL_ERR)
            self.master.refPose = None
            self._errFlag = True
        else:
            self.refPoseEntry.configure(bg=EN_BG)
            self.master.refPose = int(ref_pose_str)

        # Check and retrieve stars information
        print("Checking star list information...")
        for i in range(0, list_dim):
            star_entry = self.starEntries[i].get()
            pose_entry_str = rm_spaces(self.poseEntries[i].get())
            flat_entry_str = rm_spaces(self.flatEntries[i].get())
            neon_entry_str = rm_spaces(self.neonEntries[i].get())
            dark_entry_str = rm_spaces(self.darkEntries[i].get())
            standard_entry = rm_spaces(self.standardEntries[i].get())
            std_pose = None
            std_flag = False

            if not pose_entry_str or int(pose_entry_str) <= 0:
                print("Error: illegal pose value for star: " + star_entry + "!")
                self.poseEntries[i].configure(bg=COL_ERR)
                star_pose = None
                self._errFlag = True
            else:
                self.poseEntries[i].configure(bg=EN_BG)
                star_pose = int(pose_entry_str)

            if not flat_entry_str or int(flat_entry_str) <= 0:
                print("Error: illegal flat value for star: " + star_entry + "!")
                self.flatEntries[i].configure(bg=COL_ERR)
                star_flat = None
                self._errFlag = True
            else:
                self.flatEntries[i].configure(bg=EN_BG)
                star_flat = int(flat_entry_str)

            if not neon_entry_str or int(neon_entry_str) <= 0:
                print("Error: illegal neon value for star: " + star_entry + "!")
                self.neonEntries[i].configure(bg=COL_ERR)
                star_neon = None
                self._errFlag = True
            else:
                self.neonEntries[i].configure(bg=EN_BG)
                star_neon = int(neon_entry_str)

            if not dark_entry_str or int(dark_entry_str) <= 0:
                print("Error: illegal dark time value for star: " + star_entry + "!")
                self.darkEntries[i].configure(bg=COL_ERR)
                star_dark = None
                self._errFlag = True
            else:
                self.neonEntries[i].configure(bg=EN_BG)
                star_dark = int(dark_entry_str)

            if not is_standard(star_entry):
                if not standard_entry or not is_standard(standard_entry):
                    print("Error: invalid standard for star: " + star_entry + "!")
                    self.standardEntries[i].configure(bg=COL_ERR)
                    standard_entry = None
                    self._errFlag = True
                else:
                    for j in range(0, list_dim):
                        if standard_entry != self.starEntries[j].get():
                            continue
                        self.standardEntries[i].configure(bg=EN_BG)
                        std_pose = int(self.poseEntries[j].get())
                        std_flag = True
                        break
            else:
                standard_entry = None
                std_flag = True

            if not std_flag:
                print("Error: standard not found for star: " + star_entry + "!")
                self.standardEntries[i].configure(bg=COL_ERR)
                standard_entry = None
                self._errFlag = True

            star_info = StarInfo(star_entry, star_pose, star_flat, star_neon, star_dark, standard_entry, std_pose)
            self.master.starList.append(star_info)

        # Retrieve spectrograph data
        spec_name = self.master.specVal.get()
        spec_info = None
        for specInfo in SPEC_INFO:
            if specInfo.name == spec_name:
                spec_info = specInfo
                break
        if spec_info is None:
            # Quite impossible error, it's just for the sake of security...
            print("Error: invalid spectrograph!")
            self._errFlag = True

        if self._errFlag:
            self._errFlag = False
            return

        star_list = self.master.starList

        # CREATE IRAF FILES
        print("Creating session files...")

        mf.make_Pulizia0(ws_path)
        mf.make_CreaDarkati(ws_path, star_list, list_dim)
        mf.make_ListaGenerale(ws_path, star_list, list_dim)
        mf.make_ListaBiassati(ws_path, star_list, list_dim)
        mf.make_FLAT(ws_path, star_list, list_dim)
        mf.make_Pulizia1(ws_path)
        mf.make_GeneraMasterFlat(ws_path, star_list, list_dim,
                                 spec_info.min_h_pixel, spec_info.max_h_pixel, spec_info.h_image, spec_info.l_row)
        mf.make_ListaFlattati(ws_path, star_list, list_dim)
        mf.make_ListaTracciamoStelle(ws_path, star_list, list_dim)
        mf.make_Pulizia2(ws_path)
        mf.make_NEON(ws_path, star_list, list_dim)
        mf.make_GeneraMasterNeon(ws_path, star_list, list_dim)
        mf.make_ListaApallNe(ws_path, star_list, list_dim)
        mf.make_ListaReidentify(ws_path, star_list, list_dim, self.master.refName, self.master.refPose)
        mf.make_ListaChiConChi(ws_path, star_list, list_dim)
        mf.make_ListaCalibraLambda(ws_path, star_list, list_dim)
        mf.make_STANDARD(ws_path, star_list, list_dim)
        mf.make_DaFlussare(ws_path, star_list, list_dim)
        mf.make_Flussati(ws_path, star_list, list_dim)
        mf.make_HelioRename(ws_path, star_list, list_dim)
        mf.make_RvCorrected(ws_path, star_list, list_dim)
        mf.make_PreparoHelio(ws_path, star_list, list_dim)
        mf.make_Mediana(ws_path, star_list, list_dim)
        mf.make_Pulizia3(ws_path, star_list, list_dim)
        mf.make_Pulizia4(ws_path)
        mf.make_ListaInizio(ws_path, master_flag)

        print("Session files have been created successfully")

        # Enable Synthesis button
        self.master.synButton.configure(state=tk.NORMAL)

        # Disable first part
        self.master.wsButton.configure(state=tk.DISABLED)
        self.master.wsLabel.configure(state=tk.DISABLED)
        self.master.wsEntry.configure(state=tk.DISABLED)

        self.master.starButton.configure(state=tk.DISABLED)
        self.master.starLabel.configure(state=tk.DISABLED)
        self.master.starEntry.configure(state=tk.DISABLED)

        self.master.refButton.configure(state=tk.DISABLED)
        self.master.refLabel.configure(state=tk.DISABLED)
        self.master.refEntry.configure(state=tk.DISABLED)
        self.master.curRefLabel.configure(state=tk.DISABLED)
        self.master.curRefEntry.configure(state=tk.DISABLED)

        self.master.specLabel.configure(state=tk.DISABLED)
        self.master.specOptions.configure(state=tk.DISABLED)

        # Close star list window
        print("Closing star list window...")
        self.destroy()
        return
