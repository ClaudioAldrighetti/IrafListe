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

        self.selected = -1
        self.starEntries = []
        self.posesEntries = []
        self.flatEntries = []
        self.neonEntries = []
        self.darkEntries = []
        self.standardEntries = []

        self.removeButton = mtk.make_Button(self.listFrame, text="-", row=1, pady=1, command=self.remove_selected)

        self.selected_label = tk.StringVar(self, '')
        self.starEntry = tk.Menubutton(self.listFrame, width=15, bg=EN_BG, fg=EN_FG, relief=BT_REL,
                                       textvariable=self.selected_label)
        self.starEntry.grid(row=1, column=1, padx=1, pady=7, ipadx=0, ipady=0, sticky=tk.EW)
        self.starEntry.menu = tk.Menu(self.starEntry, tearoff=0)
        self.starEntry["menu"] = self.starEntry.menu

        # REF Data
        self.poseEntry = mtk.make_Entry(self.listFrame, row=1, column=2, width=6, sticky=tk.EW)
        self.flatEntry = mtk.make_Entry(self.listFrame, text=5, row=1, column=3, width=6, sticky=tk.EW)
        self.neonEntry = mtk.make_Entry(self.listFrame, text=3, row=1, column=4, width=6, sticky=tk.EW)
        self.darkEntry = mtk.make_Entry(self.listFrame, row=1, column=5, width=6, sticky=tk.EW)
        self.standardEntry = mtk.make_Entry(self.listFrame, row=1, column=6, width=15, sticky=tk.EW)

        # Ref frame
        self.refFrame = tk.Frame(self, bg=FR_BG)
        self.refFrame.grid(row=2)

        self.refLabel = mtk.make_Label(self.refFrame, text="REF: ", padx=2, state=tk.DISABLED)
        self.refEntry = mtk.make_Entry(self.refFrame, column=1, padx=2, sticky=tk.EW, state=tk.DISABLED)
        self.refPoseLabel = mtk.make_Label(self.refFrame, text="REF pose: ", column=2, padx=2, state=tk.DISABLED)
        self.refPoseEntry = mtk.make_Entry(self.refFrame, width=5, column=3, padx=2, sticky=tk.EW, state=tk.DISABLED)

        # Start button
        self.startButton = mtk.make_Button(self, self.start_session, text="Start Session", row=3, columnspan=2, pady=2)

        # List Info Window
        self.infoWindow = ListInfoWindow(self)

        return

    def select(self, index, store=True):
        print('SELECT INDEX: ', index)

        if store:
            self.store_selected_data()

        mtk.clear_Entry(self.poseEntry)
        self.poseEntry.insert(0, self.posesEntries[index])
        mtk.clear_Entry(self.flatEntry)
        self.flatEntry.insert(0, self.flatEntries[index])
        mtk.clear_Entry(self.neonEntry)
        self.neonEntry.insert(0, self.neonEntries[index])
        mtk.clear_Entry(self.darkEntry)
        self.darkEntry.insert(0, self.darkEntries[index])
        star_name = self.starEntries[index]
        if is_standard(star_name):
            mtk.clear_Entry(self.standardEntry, tk.DISABLED)
        else:
            mtk.clear_Entry(self.standardEntry, tk.NORMAL)
            self.standardEntry.insert(0, self.standardEntries[index])

        self.selected_label.set(star_name)
        self.selected = index
        return

    def select_name(self, name):
        print('SELECT NAME: ', name)
        self.select(self.starEntries.index(name))

        return

    def store_selected_data(self):
        print('STORE SELECTED')
        index = self.selected
        self.posesEntries[index] = self.poseEntry.get()
        self.flatEntries[index] = self.flatEntry.get()
        self.neonEntries[index] = self.neonEntry.get()
        self.darkEntries[index] = self.darkEntry.get()
        star_name = self.starEntries[index]
        if not is_standard(star_name):
            self.standardEntries[index] = self.standardEntry.get()

        # Refresh info data
        self.infoWindow.refresh()

        return

    def remove_selected(self):
        print('REMOVE SELECTED: ', self.starEntries[self.selected])
        self.starEntry.menu.delete(self.starEntries[self.selected])
        self.master.remove_star(self.selected)

        if self.master.starListDim > 0:
            self.selected_label.set(self.starEntries[0])
            self.selected = 0
        else:
            self.close()

        return

    # Create general IRAF files
    def start_session(self):
        print("START SESSION")

        # Store selected star to update its data if it has been changed
        self.store_selected_data()

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
            star_entry = self.starEntries[i]
            poses_entry_str = self.posesEntries[i]
            flat_entry_str = self.flatEntries[i]
            neon_entry_str = self.neonEntries[i]
            dark_entry_str = self.darkEntries[i]
            standard_entry = rm_spaces(self.standardEntries[i])
            std_poses = None
            std_flag = False

            if not str_is_positive_int(poses_entry_str):
                print("Error: illegal poses value for star: " + star_entry + "!")
                # mtk.entry_err_blink(self.posesEntries[i])
                star_poses = None
                err_flag = True
            else:
                star_poses = int(poses_entry_str)

            if not str_is_positive_int(flat_entry_str):
                print("Error: illegal flat value for star: " + star_entry + "!")
                # mtk.entry_err_blink(self.flatEntries[i])
                star_flat = None
                err_flag = True
            else:
                star_flat = int(flat_entry_str)

            if not str_is_positive_int(neon_entry_str):
                print("Error: illegal neon value for star: " + star_entry + "!")
                # mtk.entry_err_blink(self.neonEntries[i])
                star_neon = None
                err_flag = True
            else:
                star_neon = int(neon_entry_str)

            if not str_is_positive_int(dark_entry_str):
                print("Error: illegal dark time value for star: " + star_entry + "!")
                # mtk.entry_err_blink(self.darkEntries[i])
                star_dark = None
                err_flag = True
            else:
                star_dark = int(dark_entry_str)

            if std_check_flag and not is_standard(star_entry):
                if not standard_entry or not is_standard(standard_entry):
                    print("Error: invalid standard for star: " + star_entry + "!")
                    # mtk.entry_err_blink(self.standardEntries[i])
                    standard_entry = None
                    err_flag = True
                else:
                    for j in range(0, list_dim):
                        if standard_entry != self.starEntries[j]:
                            continue

                        std_poses_entry = rm_spaces(self.posesEntries[j])
                        if not str_is_positive_int(std_poses_entry):
                            print("Error: illegal poses value for standard: " + standard_entry + "!")
                            # mtk.entry_err_blink(self.posesEntries[j])
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
                # mtk.entry_err_blink(self.standardEntries[i])
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


# Star List Info Window class
class ListInfoWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("List Info")
        self.geometryBase = WinGeometry(650, 150, 420, 300)
        self.geometry(str(self.geometryBase))
        self.minsize(500, 150)
        self.configure(bg=FR_BG)

        self.listFrame = tk.Frame(self, bg=FR_BG)
        self.listFrame.pack(expand=True, fill=tk.BOTH)
        self.listText = tk.Text(self.listFrame, state=tk.NORMAL, bg=EN_BG, fg=GEN_FG, relief=tk.FLAT)
        self.listText.pack(expand=True, fill=tk.BOTH)
        self.refresh()

        return

    # Star List Info
    def refresh(self):
        self.listText.configure(state=tk.NORMAL)
        self.listText.delete("1.0", tk.END)

        std_check_flag = self.master.master.standardVar.get()

        list_string = ""
        for i in range(0, self.master.master.starListDim):
            star_name = self.master.starEntries[i]

            if std_check_flag and not is_standard(star_name):
                std_str = self.master.standardEntries[i] + "\n"
            else:
                std_str = "None\n"

            list_string += ("Star: " + star_name + "\t| " +
                            "Poses: " + str(self.master.posesEntries[i]) + "\t| " +
                            "Flat: " + str(self.master.flatEntries[i]) + "\t| " +
                            "Neon: " + str(self.master.neonEntries[i]) + "\t| " +
                            "Dark-T: " + str(self.master.darkEntries[i]) + "\t| " +
                            "Standard: " + std_str)

        self.listText.insert("end", list_string)
        self.listText.configure(state=tk.DISABLED)
        return
