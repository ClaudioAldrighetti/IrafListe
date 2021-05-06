# import tkinter as tk
# import tkinter
from tkinter import filedialog as fd
# import tkinter.ttk as ttk

from starwindow import StarListWindow
from masterwindow import MasterListWindow
# import makefiles as mf
import maketk as mtk
from utility import *
from winconfig import *


# Main window class
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IRAF Liste")

        self.defGeometry = MAIN_WIN_DEF_GEOM
        self.geometry(str(self.defGeometry))
        self.resizable(False, False)
        self.configure(bg=FR_BG)

        # Settings frame
        self.settingFrame = tk.Frame(self, bg=FR_BG)
        self.settingFrame.pack()

        # Workspace settings
        self.wsButton = mtk.make_Button(self.settingFrame, self.select_ws_path, text="Choose WS dir", pady=5)
        self.wsLabel = mtk.make_Label(self.settingFrame, text="Workspace:", column=1)
        self.wsEntry = mtk.make_Entry(self.settingFrame, column=2, state="readonly")
        self.wsPath = ""

        # Add star interface
        self.starButton = mtk.make_Button(self.settingFrame, self.add_star,
                                          text="Add star", row=1, state=tk.DISABLED)
        self.starLabel = mtk.make_Label(self.settingFrame, text="New star:", row=1, column=1, state=tk.DISABLED)
        self.starEntry = mtk.make_Entry(self.settingFrame, row=1, column=2, state=tk.DISABLED)

        # Star list
        self.starList = []
        self.listDim = 0
        self.starListWindow = None

        # Reference star interface
        self.refButton = mtk.make_Button(self.settingFrame, self.select_ref,
                                         text="Choose reference", row=2, state=tk.DISABLED)
        self.refLabel = mtk.make_Label(self.settingFrame, text="New REF:", row=2, column=1, state=tk.DISABLED)
        self.refEntry = mtk.make_Entry(self.settingFrame, row=2, column=2, state=tk.DISABLED)

        self.curRefLabel = mtk.make_Label(self.settingFrame, text="Selected REF:", row=3, column=1, state=tk.DISABLED)
        self.curRefEntry = mtk.make_Entry(self.settingFrame, row=3, column=2, state=tk.DISABLED)

        self.refName = None
        self.refPose = None

        # Spectrograph selection interface
        self.specLabel = mtk.make_Label(self.settingFrame, text="Spectrograph:", row=4, column=1, state=tk.DISABLED)

        self.specVal = tk.StringVar(self)
        spec_list = (specInfo.name for specInfo in SPEC_INFO)
        self.specOptions = mtk.make_OptionMenu(self.settingFrame, self.specVal, spec_list,
                                               defaultval=SPEC_INFO[0].name, row=4, column=2, state=tk.DISABLED)

        # Synthesis Button
        self.synButton = mtk.make_Button(self, self.gen_syn,
                                         text="Generate Synthesis", state=tk.DISABLED, grid_flag=False, fill="x")
        self.synWindow = None
        self.sepSynMaster = mtk.make_Separator(self)

        # Master frame
        self.masterFrame = tk.Frame(self, bg=FR_BG)
        self.masterFrame.pack()

        # Master dark interface
        self.darkButton = mtk.make_Button(self.masterFrame, command=lambda: self.add_master(DARK),
                                          text="Add Master Dark", state=tk.DISABLED)
        self.darkPosesLabel = mtk.make_Label(self.masterFrame, text="Dark poses:", column=1, state=tk.DISABLED)
        self.darkPosesEntry = mtk.make_Entry(self.masterFrame, column=2, state=tk.DISABLED)
        self.darkTimeLabel = mtk.make_Label(self.masterFrame, text="Dark time:", row=1, column=1, state=tk.DISABLED)
        self.darkTimeEntry = mtk.make_Entry(self.masterFrame, row=1, column=2, state=tk.DISABLED)

        # Master list
        self.masterListDim = 0
        self.masterListWindow = None
        self.masterFlag = False

        # Master bias interface
        self.biasButton = mtk.make_Button(self.masterFrame, command=lambda: self.add_master(BIAS),
                                          text="Insert Master Bias", row=2, state=tk.DISABLED)
        self.biasPosesLabel = mtk.make_Label(self.masterFrame, text="Bias poses:", row=2, column=1, state=tk.DISABLED)
        self.biasPosesEntry = mtk.make_Entry(self.masterFrame, row=2, column=2, state=tk.DISABLED)

        # Bottom frame
        self.bottomFrame = tk.Frame(self, bg=FR_BG)
        self.bottomFrame.pack(side=tk.BOTTOM, fill=tk.X)
        self.restartFrame = tk.Frame(self.bottomFrame, bg=FR_BG)
        self.restartFrame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.closeFrame = tk.Frame(self.bottomFrame, bg=FR_BG)
        self.closeFrame.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        # Restart button
        self.restartButton = mtk.make_Button(self.restartFrame, self.restart,
                                             text="Restart", pady=5, grid_flag=False, fill=tk.X, expand=True)

        # Close button
        self.closeButton = mtk.make_Button(self.closeFrame, self.destroy,
                                           text="Close", pady=5, grid_flag=False, fill=tk.X, expand=True)

    # Workspace selection
    def select_ws_path(self):
        print("SELECT WS PATH")

        print("Selecting workspace directory...")
        self.wsPath = fd.askdirectory(initialdir="/", title="Choose Workspace Directory")
        if not self.wsPath:
            print("Error: no workspace directory selected!")
            return
        print("WS: " + self.wsPath)
        print("Workspace set successfully")

        self.wsEntry.configure(state=tk.NORMAL)
        self.wsEntry.insert(0, self.wsPath)
        self.wsEntry.configure(state="readonly")

        self.starEntry.configure(state=tk.NORMAL)
        self.starLabel.configure(state=tk.NORMAL)
        self.starButton.configure(state=tk.NORMAL)
        self.specLabel.configure(state=tk.NORMAL)
        self.specOptions.configure(state=tk.NORMAL)

        self.darkButton.configure(state=tk.NORMAL)
        self.darkPosesLabel.configure(state=tk.NORMAL)
        self.darkPosesEntry.configure(state=tk.NORMAL)
        self.darkTimeLabel.configure(state=tk.NORMAL)
        self.darkTimeEntry.configure(state=tk.NORMAL)
        self.biasButton.configure(state=tk.NORMAL)
        self.biasPosesLabel.configure(state=tk.NORMAL)
        self.biasPosesEntry.configure(state=tk.NORMAL)
        return

    # Add a star to the list
    def add_star(self):
        print("ADD STAR")

        # Check star name
        print("Checking inserted name...")
        star_name = rm_spaces(self.starEntry.get())
        mtk.clear_Entry(self.starEntry)
        if not star_name:
            print("Error: insert a star name!")
            self.starEntry.configure(bg=COL_ERR)
            return
        elif self.starListWindow is None:
            # Open star list window
            print("Opening star list window...")
            self.starListWindow = StarListWindow()
            self.refButton.configure(state=tk.NORMAL)
            self.refLabel.configure(state=tk.NORMAL)
            self.refEntry.configure(state=tk.NORMAL)
        else:
            for i in range(0, self.listDim):
                i_star = self.starListWindow.starEntries[i].get()
                if star_name == i_star:
                    print("Error: star is already in the list!")
                    self.starEntry.configure(bg=COL_ERR)
                    return
        self.starEntry.configure(bg=EN_BG)

        self.listDim += 1
        list_dim = self.listDim
        list_frame = self.starListWindow.listFrame

        # Add new record on the star list window
        print("Adding a new record on the star list window...")
        new_star_entry = mtk.make_Entry(list_frame, text=star_name,
                                        row=list_dim, column=1, padx=2, width=20, sticky=tk.EW, state="readonly")
        self.starListWindow.starEntries.append(new_star_entry)

        new_pose_entry = mtk.make_Entry(list_frame, row=list_dim, column=2, width=6, sticky=tk.EW)
        self.starListWindow.poseEntries.append(new_pose_entry)

        new_flat_entry = mtk.make_Entry(list_frame, text=5, row=list_dim, column=3, width=6, sticky=tk.EW)
        self.starListWindow.flatEntries.append(new_flat_entry)

        new_neon_entry = mtk.make_Entry(list_frame, text=3, row=list_dim, column=4, width=6, sticky=tk.EW)
        self.starListWindow.neonEntries.append(new_neon_entry)

        new_dark_entry = mtk.make_Entry(list_frame, row=list_dim, column=5, width=6, sticky=tk.EW)
        self.starListWindow.darkEntries.append(new_dark_entry)

        new_standard_entry = mtk.make_Entry(list_frame, row=list_dim, column=6, width=10, sticky=tk.EW)
        if is_standard(star_name):
            new_standard_entry.configure(state=tk.DISABLED)
        self.starListWindow.standardEntries.append(new_standard_entry)

        new_remove_button = mtk.make_Button(list_frame, text="-", row=list_dim, pady=1,
                                            command=lambda to_remove=list_dim: self.remove_star(to_remove))
        self.starListWindow.removeButtons.append(new_remove_button)

        # Resize star list window
        self.starListWindow = resized_window(self.starListWindow, self.listDim, STARL_EN_HG)

        print("New star added successfully")
        return

    # Remove a star from the list
    def remove_star(self, record_to_remove):
        print("REMOVE STAR")

        index_to_remove = record_to_remove - 1
        name_to_remove = self.starListWindow.starEntries[index_to_remove].get()

        # Check if the star to remove is the reference star
        if is_standard(name_to_remove) and self.curRefEntry.get() == name_to_remove:
            print("Removing reference information...")
            mtk.clear_Entry(self.curRefEntry)
            self.starListWindow.refLabel.configure(state=tk.DISABLED)
            mtk.clear_Entry(self.starListWindow.refEntry)
            self.starListWindow.refPoseLabel.configure(state=tk.DISABLED)
            mtk.clear_Entry(self.starListWindow.refPoseEntry, tk.DISABLED)

        self.starListWindow.removeButtons.pop(index_to_remove).destroy()
        self.starListWindow.starEntries.pop(index_to_remove).destroy()
        self.starListWindow.poseEntries.pop(index_to_remove).destroy()
        self.starListWindow.flatEntries.pop(index_to_remove).destroy()
        self.starListWindow.neonEntries.pop(index_to_remove).destroy()
        self.starListWindow.darkEntries.pop(index_to_remove).destroy()
        self.starListWindow.standardEntries.pop(index_to_remove).destroy()

        self.listDim -= 1

        if self.listDim == 0:
            print("Closing star list window...")
            self.starListWindow.destroy()
            self.starListWindow = None

            print("Star removed correctly")
            return

        for i in range(index_to_remove, self.listDim):
            new_row = self.starListWindow.starEntries[i].grid_info().get("row")-1
            self.starListWindow.removeButtons[i].configure(command=lambda to_remove=new_row:
                                                           self.remove_star(to_remove))
            self.starListWindow.removeButtons[i].grid(row=new_row)
            self.starListWindow.starEntries[i].grid(row=new_row)
            self.starListWindow.poseEntries[i].grid(row=new_row)
            self.starListWindow.flatEntries[i].grid(row=new_row)
            self.starListWindow.neonEntries[i].grid(row=new_row)
            self.starListWindow.darkEntries[i].grid(row=new_row)
            self.starListWindow.standardEntries[i].grid(row=new_row)

        # Resize star list window
        self.starListWindow = resized_window(self.starListWindow, self.listDim, STARL_EN_HG)

        print("Star removed correctly")
        return

    # Add reference star
    def select_ref(self):
        print("SELECT REF")

        # Check ref name
        print("Checking inserted name...")
        ref_name = rm_spaces(self.refEntry.get())
        mtk.clear_Entry(self.refEntry)
        if not ref_name:
            print("Error: insert a star name!")
            self.refEntry.configure(bg=COL_ERR)
            return

        for i in range(0, self.listDim):
            if ref_name != self.starListWindow.starEntries[i].get():
                continue

            # Set reference star
            print("Setting the reference star...")
            self.refName = ref_name

            self.refEntry.configure(bg=EN_BG)

            self.curRefLabel.configure(state=tk.NORMAL)
            mtk.clear_Entry(self.curRefEntry, tk.NORMAL)
            self.curRefEntry.insert(0, ref_name)
            self.curRefEntry.configure(state="readonly")

            self.starListWindow.refLabel.configure(state=tk.NORMAL)
            mtk.clear_Entry(self.starListWindow.refEntry, tk.NORMAL)
            self.starListWindow.refEntry.insert(0, ref_name)
            self.starListWindow.refEntry.configure(state="readonly")
            self.starListWindow.refPoseLabel.configure(state=tk.NORMAL)
            self.starListWindow.refPoseEntry.configure(state=tk.NORMAL)

            print("Reference star set successfully")
            return

        print("Error: illegal reference star name!")
        self.refEntry.configure(bg=COL_ERR)
        return

    def gen_syn(self):
        print("GEN SYN")

        print("Opening synthesis window...")
        self.synWindow = SynthesisWindow(self)
        return

    def add_master(self, master_type):
        print("ADD MASTER (" + master_type + ")")

        bias_flag = (master_type == BIAS)
        err_flag = False

        if bias_flag:
            print("Checking inserted bias poses value...")
            poses_entry = self.biasPosesEntry

        else:
            print("Checking inserted dark poses and time values...")
            poses_entry = self.darkPosesEntry
            time_entry = self.darkTimeEntry
            master_time = rm_spaces(time_entry.get())
            mtk.clear_Entry(time_entry)

            if not master_time:
                print("Error: insert dark time!")
                err_flag = True
            else:
                master_time = int(master_time)
                if master_time <= 0:
                    print("Error: dark time must be positive!")
                    err_flag = True
                elif not (self.masterListWindow is None):
                    for i in range(0, self.masterListDim):
                        if self.masterListWindow.typeEntries[i].get() == BIAS:
                            continue

                        i_time = int(self.masterListWindow.timeEntries[i].get())
                        if master_time == i_time:
                            print("Error: master dark with such pose time already exists!")
                            err_flag = True
                            break
                else:
                    # Dark time value is legal
                    time_entry.configure(bg=EN_BG)

        master_poses = rm_spaces(poses_entry.get())
        mtk.clear_Entry(poses_entry)

        if not master_poses:
            print("Error: insert poses number!")
            err_flag = True
        else:
            master_poses = int(master_poses)
            if master_poses <= 0:
                print("Error: poses number must be positive!")
                err_flag = True
            else:
                # Poses number is legal
                poses_entry.configure(bg=EN_BG)

        if err_flag:
            poses_entry.configure(bg=COL_ERR)
            if master_type == DARK:
                time_entry.configure(bg=COL_ERR)
            return

        if bias_flag:
            self.biasButton.configure(state=tk.DISABLED)
            self.biasPosesLabel.configure(state=tk.DISABLED)
            self.biasPosesEntry.configure(state=tk.DISABLED)

        self.masterListDim += 1
        self.masterFlag = True

        if self.masterListWindow is None:
            # Open dark list window
            print("Opening master list window...")
            self.masterListWindow = MasterListWindow()

        list_dim = self.masterListDim
        list_frame = self.masterListWindow.listFrame

        print("Adding the master to the list...")
        new_type_entry = mtk.make_Entry(list_frame, text=master_type,
                                        row=list_dim, column=1, padx=2, width=6, sticky=tk.EW, state="readonly")
        self.masterListWindow.typeEntries.append(new_type_entry)

        new_poses_entry = mtk.make_Entry(list_frame, text=master_poses,
                                         row=list_dim, column=2, padx=2, width=6, sticky=tk.EW, state="readonly")
        self.masterListWindow.posesEntries.append(new_poses_entry)

        new_time_entry = mtk.make_Entry(list_frame, row=list_dim, column=3, padx=2, width=6, sticky=tk.EW)
        if bias_flag:
            new_time_entry.configure(state=tk.DISABLED)
        else:
            new_time_entry.insert(0, master_time)
            new_time_entry.configure(state="readonly")
        self.masterListWindow.timeEntries.append(new_time_entry)

        new_remove_button = mtk.make_Button(list_frame, text="-", row=list_dim, pady=1,
                                            command=lambda: self.remove_master(list_dim))
        self.masterListWindow.removeButtons.append(new_remove_button)

        # Resize master list window
        self.masterListWindow = resized_window(self.masterListWindow, list_dim, MASTERL_EN_HG)

        print("New master added successfully")
        return

    def remove_master(self, record_to_remove):
        print("REMOVE MASTER")

        index_to_remove = record_to_remove - 1
        master_type = self.masterListWindow.typeEntries[index_to_remove].get()
        print(master_type, " ", BIAS)
        if master_type == BIAS:
            self.biasButton.configure(state=tk.NORMAL)
            self.biasPosesLabel.configure(state=tk.NORMAL)
            self.biasPosesEntry.configure(state=tk.NORMAL)

        self.masterListWindow.removeButtons.pop(index_to_remove).destroy()
        self.masterListWindow.typeEntries.pop(index_to_remove).destroy()
        self.masterListWindow.posesEntries.pop(index_to_remove).destroy()
        self.masterListWindow.timeEntries.pop(index_to_remove).destroy()

        self.masterListDim -= 1

        if self.masterListDim == 0:
            print("Closing master list window...")
            self.masterListWindow.destroy()
            self.masterListWindow = None
            self.masterFlag = False

            print("Master removed correctly")
            return

        list_dim = self.masterListDim
        for i in range(index_to_remove, list_dim):
            new_record = self.masterListWindow.typeEntries[i].grid_info().get("row")-1
            self.masterListWindow.removeButtons[i].configure(command=lambda: self.remove_master(new_record))
            self.masterListWindow.removeButtons[i].grid(row=new_record)
            self.masterListWindow.typeEntries[i].grid(row=new_record)
            self.masterListWindow.posesEntries[i].grid(row=new_record)
            self.masterListWindow.timeEntries[i].grid(row=new_record)

        # Resize master list window
        self.masterListWindow = resized_window(self.masterListWindow, list_dim, MASTERL_EN_HG)

        print("Master removed correctly")
        return

    def restart(self):
        print("RESTART")

        # Close all the other windows (if there are)
        if not (self.starListWindow is None):
            self.starListWindow.destroy()
            self.starListWindow = None

        if not (self.masterListWindow is None):
            self.masterListWindow.destroy()
            self.masterListWindow = None

        if not (self.synWindow is None):
            self.synWindow.destroy()
            self.synWindow = None

        # Delete information about the previous session
        self.wsPath = ""

        self.starList = []
        self.listDim = 0
        self.refName = None
        self.refPose = None

        self.masterListDim = 0
        self.masterFlag = False

        self.wsButton.configure(state=tk.NORMAL)
        self.wsLabel.configure(state=tk.NORMAL)
        mtk.clear_Entry(self.wsEntry)

        self.starButton.configure(state=tk.DISABLED)
        self.starLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.starEntry, tk.DISABLED)

        self.refButton.configure(state=tk.DISABLED)
        self.refLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.refEntry, tk.DISABLED)
        self.curRefLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.curRefEntry)

        self.specLabel.configure(state=tk.DISABLED)
        self.specOptions.configure(state=tk.DISABLED)

        self.synButton.configure(state=tk.DISABLED)

        self.darkButton.configure(state=tk.DISABLED)
        self.darkPosesLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.darkPosesEntry, tk.DISABLED)
        self.darkTimeLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.darkTimeEntry, tk.DISABLED)

        self.biasButton.configure(state=tk.DISABLED)
        self.biasPosesLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.biasPosesEntry, tk.DISABLED)

        return


# Synthesis window class
class SynthesisWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Synthesis")
        self.geometryBase = WinGeometry(600, 150, 110, 260)
        self.geometry(str(self.geometryBase))
        self.minsize(300, 100)
        self.configure(bg=FR_BG)

        self.synFrame = tk.Frame(self, bg=FR_BG)
        self.synFrame.pack(expand=True, fill=tk.BOTH)
        self.synText = tk.Text(self.synFrame, state=tk.NORMAL, bg=EN_BG, fg=GEN_FG, relief=tk.FLAT)
        self.synText.pack(expand=True, fill=tk.BOTH)
        self.syn()

    # Synthesis report
    def syn(self):
        syn_string = ""
        for i in range(0, self.master.listDim):
            star_info = self.master.starList[i]

            if not is_standard(star_info.name):
                std_str = " Standard: " + star_info.standard + "\n"
            else:
                std_str = "\n"

            syn_string += ("STAR: " + star_info.name +
                           " N_Pose: " + str(star_info.pose) +
                           " N_Flat: " + str(star_info.flat) +
                           " N_Neon: " + str(star_info.neon) +
                           " T_Dark: " + str(star_info.dark_time) +
                           std_str)
        syn_string += "REFERENCE: " + self.master.refName + " Pose: " + str(self.master.refPose)

        self.synText.insert("end", syn_string)
        self.synText.configure(state=tk.DISABLED)
        return
