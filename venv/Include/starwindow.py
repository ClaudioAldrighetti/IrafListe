import tkinter as tk
import os

import makefiles as mf
import maketk as mtk
from utility import rm_spaces, is_standard, str_is_positive_int, StarInfo
from winconfig import *
from spectrographs import get_spec_info


# Star list window class
class StarListWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Star List")

        self.defGeometry = STAR_WIN_DEF_GEOM
        self.geometry(str(self.defGeometry))
        self.resizable(False, False)
        self.configure(bg=FR_BG)
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Star list
        self.listFrame = tk.Frame(self, bg=FR_BG)
        self.listFrame.grid()

        self.starLabel = mtk.make_Label(self.listFrame, text="Star", column=1, pady=2, sticky=tk.EW)
        self.posesLabel = mtk.make_Label(self.listFrame, text="Poses", column=2, pady=2, sticky=tk.EW)
        self.flatLabel = mtk.make_Label(self.listFrame, text="Flat", column=3, pady=2, sticky=tk.EW)
        self.neonLabel = mtk.make_Label(self.listFrame, text="Neon", column=4, pady=2, sticky=tk.EW)
        self.darkLabel = mtk.make_Label(self.listFrame, text="Dark T", column=5, pady=2, sticky=tk.EW)
        self.standardLabel = mtk.make_Label(self.listFrame, text="Standard", column=6, pady=2, sticky=tk.EW)

        self.starEntries = []
        self.posesEntries = []
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

        return

    # Create general IRAF files
    def start_session(self):
        print("START SESSION")

        err_flag = False
        std_check_flag = self.master.standardVar.get()
        master_flag = self.master.masterFlag
        self.master.starList = []

        print("Checking environment...")
        # Check workspace directory
        ws_path = self.master.wsPath
        if not os.path.exists(ws_path):
            print("Error: workspace directory doesn't exist!")
            err_flag = True

        # Check star list length
        list_dim = self.master.starListDim
        if list_dim == 0:
            print("Error: star list is empty!")
            err_flag = True

        # Check reference pose
        ref_pose_str = rm_spaces(self.refPoseEntry.get())
        if not str_is_positive_int(ref_pose_str):
            print("Error: illegal reference pose value!")
            mtk.entry_err_blink(self.refPoseEntry)
            self.master.refPose = None
            err_flag = True
        else:
            self.master.refPose = int(ref_pose_str)

        # Check and retrieve stars information
        print("Checking star list information...")
        for i in range(0, list_dim):
            star_entry = self.starEntries[i].get()
            poses_entry_str = rm_spaces(self.posesEntries[i].get())
            flat_entry_str = rm_spaces(self.flatEntries[i].get())
            neon_entry_str = rm_spaces(self.neonEntries[i].get())
            dark_entry_str = rm_spaces(self.darkEntries[i].get())
            standard_entry = rm_spaces(self.standardEntries[i].get())
            std_poses = None
            std_flag = False

            if not str_is_positive_int(poses_entry_str):
                print("Error: illegal poses value for star: " + star_entry + "!")
                mtk.entry_err_blink(self.posesEntries[i])
                star_poses = None
                err_flag = True
            else:
                star_poses = int(poses_entry_str)

            if not str_is_positive_int(flat_entry_str):
                print("Error: illegal flat value for star: " + star_entry + "!")
                mtk.entry_err_blink(self.flatEntries[i])
                star_flat = None
                err_flag = True
            else:
                star_flat = int(flat_entry_str)

            if not str_is_positive_int(neon_entry_str):
                print("Error: illegal neon value for star: " + star_entry + "!")
                mtk.entry_err_blink(self.neonEntries[i])
                star_neon = None
                err_flag = True
            else:
                star_neon = int(neon_entry_str)

            if not str_is_positive_int(dark_entry_str):
                print("Error: illegal dark time value for star: " + star_entry + "!")
                mtk.entry_err_blink(self.darkEntries[i])
                star_dark = None
                err_flag = True
            else:
                star_dark = int(dark_entry_str)

            if std_check_flag and not is_standard(star_entry):
                if not standard_entry or not is_standard(standard_entry):
                    print("Error: invalid standard for star: " + star_entry + "!")
                    mtk.entry_err_blink(self.standardEntries[i])
                    standard_entry = None
                    err_flag = True
                else:
                    for j in range(0, list_dim):
                        if standard_entry != self.starEntries[j].get():
                            continue

                        std_poses_entry = rm_spaces(self.posesEntries[j].get())
                        if not str_is_positive_int(std_poses_entry):
                            print("Error: illegal poses value for standard: " + standard_entry + "!")
                            mtk.entry_err_blink(self.posesEntries[j])
                            err_flag = True
                        else:
                            std_poses = int(std_poses_entry)

                        std_flag = True
                        break
            else:
                standard_entry = None
                std_flag = True

            if not std_flag:
                print("Error: standard not found for star: " + star_entry + "!")
                mtk.entry_err_blink(self.standardEntries[i])
                standard_entry = None
                err_flag = True

            star_info = StarInfo(star_entry, star_poses, star_flat, star_neon, star_dark, standard_entry, std_poses)
            self.master.starList.append(star_info)

        # Retrieve spectrograph data
        spec_info = get_spec_info(self.master.specVal.get())
        if spec_info is None:
            # Quite impossible error, it's just for the sake of security...
            print("Error: invalid spectrograph!")
            err_flag = True

        if err_flag:
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
        if std_check_flag:
            # Files needed only if standard stars are considered
            mf.make_DaFlussare(ws_path, star_list, list_dim)
            mf.make_Flussati(ws_path, star_list, list_dim)
        mf.make_HelioRename(ws_path, star_list, list_dim, std_check_flag)
        mf.make_RvCorrected(ws_path, star_list, list_dim, std_check_flag)
        mf.make_PreparoHelio(ws_path, star_list, list_dim)
        mf.make_Mediana(ws_path, star_list, list_dim)
        mf.make_Pulizia3(ws_path, star_list, list_dim, std_check_flag)
        # mf.make_Pulizia4(ws_path)
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
        self.master.standardCheck.configure(state=tk.DISABLED)
        self.master.curRefLabel.configure(state=tk.DISABLED)
        self.master.curRefEntry.configure(state=tk.DISABLED)

        self.master.specLabel.configure(state=tk.DISABLED)
        self.master.specOptions.configure(state=tk.DISABLED)
        self.master.addSpecButton.configure(state=tk.DISABLED)
        self.master.modSpecButton.configure(state=tk.DISABLED)
        self.master.delSpecButton.configure(state=tk.DISABLED)

        # Close star list window
        print("Closing star list window...")
        self.master.starListWindow = None
        self.destroy()
        return

    def close(self):
        # Delete star list information
        print("Deleting star list information...")
        self.master.starListDim = 0
        self.master.refName = None
        self.master.refPose = None

        self.master.refButton.configure(state=tk.DISABLED)
        self.master.refLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.master.refEntry, tk.DISABLED)
        self.master.curRefLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.master.curRefEntry, tk.DISABLED)

        # Close star list window
        print("Closing star list window...")
        self.master.starListWindow = None
        self.destroy()
        return
