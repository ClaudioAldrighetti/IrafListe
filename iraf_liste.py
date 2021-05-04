# import tkinter as tk
from tkinter import filedialog as fd
# import tkinter.ttk as ttk
import os

import makefiles as mf
import maketk as mtk
from utility import *
from winconfig import *


# Main window class
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IRAF Liste")

        if platform == "linux":
            # Linux distribution configuration
            self.geometryBase = WinGeometry(390, 350, 100, 100)
        else:
            # Windows or other
            self.geometryBase = WinGeometry(300, 350, 100, 100)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)
        self.configure(bg=FR_BG)

        # Settings frame
        self.settingFrame = tk.Frame(self, bg=FR_BG)
        self.settingFrame.pack()

        # Workspace settings
        self.wsButton = mtk.make_Button(self.settingFrame, self.select_ws_path, text="Choose WS dir")
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

        # Master Button
        self.masterButton = mtk.make_Button(self, self.open_master,
                                            text="Master Bias and Dark", state=tk.DISABLED, grid_flag=False, fill="x")
        self.masterWindow = None
        self.masterFlag = False

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

        self.wsEntry.configure(state="normal")
        self.wsEntry.insert(0, self.wsPath)
        self.wsEntry.configure(state="readonly")

        self.starEntry.configure(state="normal")
        self.starLabel.configure(state="normal")
        self.starButton.configure(state="normal")
        self.specLabel.configure(state="normal")
        self.specOptions.configure(state="normal")
        self.masterButton.configure(state="normal")
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
        self.starEntry.configure(bg=EN_BG)

        self.listDim += 1
        list_dim = self.listDim

        if list_dim == 1:
            # Open star list window
            print("Opening star list window...")
            self.starListWindow = StarListWindow()
            self.refButton.configure(state=tk.NORMAL)
            self.refLabel.configure(state=tk.NORMAL)
            self.refEntry.configure(state=tk.NORMAL)

        list_frame = self.starListWindow.listFrame

        print("Adding a new line in the star list window...")
        # New entry on the star list window
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
        base_height = self.starListWindow.geometryBase.height
        new_height = base_height + STARL_EN_HG * list_dim
        base_width = self.starListWindow.geometryBase.width
        self.starListWindow.geometry(str(base_width) + "x" + str(new_height))

        print("New star added successfully")
        return

    # Remove a star from the list
    def remove_star(self, row_to_remove):
        print("REMOVE STAR")

        index_to_remove = row_to_remove-1
        name_to_remove = self.starListWindow.starEntries[index_to_remove].get()
        # Check if the star to remove is the reference star
        if is_standard(name_to_remove) and self.curRefEntry.get() == name_to_remove:
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
            self.starListWindow.destroy()
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
        base_height = self.starListWindow.geometryBase.height
        new_height = base_height + STARL_EN_HG * self.listDim
        base_width = self.starListWindow.geometryBase.width
        self.starListWindow.geometry(str(base_width) + "x" + str(new_height))

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

            print("Setting the reference star...")
            # Set reference star
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

    def open_master(self):
        print("OPEN MASTER")

        print("Opening Master window...")
        self.masterWindow = MasterWindow(self)
        self.masterFlag = True
        return

    def gen_syn(self):
        print("GEN SYN")

        print("Opening Synthesis window...")
        self.synWindow = SynthesisWindow(self)
        return

    def restart(self):
        print("RESTART")

        if not (self.starListWindow is None):
            self.starListWindow.destroy()
            self.starListWindow = None

        if not (self.masterWindow is None):
            self.masterWindow.destroy()
            self.masterWindow = None

        if not (self.synWindow is None):
            self.synWindow.destroy()
            self.synWindow = None

        self.wsPath = ""
        self.starList = []
        self.listDim = 0
        self.refName = None
        self.refPose = None
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
        self.masterButton.configure(state=tk.DISABLED)

        return


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

        print("All initial files have been created successfully")

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


# Synthesis window class
class SynthesisWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Synthesis")
        self.geometryBase = WinGeometry(600, 150, 110, 260)
        self.geometry(str(self.geometryBase))
        self.minsize(300, 100)
        self.configure(bg=FR_BG)

        # Synthesis
        self.synFrame = tk.Frame(self, bg=FR_BG)
        self.synFrame.pack(expand=True, fill="both")
        self.synText = tk.Text(self.synFrame, state="normal", bg=EN_BG, fg=GEN_FG, relief=tk.FLAT)
        self.synText.pack(expand=True, fill="both")

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
        self.synText.configure(state="disabled")


# Star list window class
class MasterWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Master Dark and Bias List")

        if platform == "linux":
            self.geometryBase = WinGeometry(235, 175, 110, 260)
        else:
            self.geometryBase = WinGeometry(190, 155, 110, 260)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)
        self.configure(bg=FR_BG)

        self._errFlag = False

        # Bias Frame
        self.biasFrame = tk.Frame(self, bg=FR_BG)
        self.biasFrame.grid()
        self.biasLabel = tk.Label(self.biasFrame, text="Bias Num Pose: ")
        self.biasLabel.grid(row=0, column=0, padx=1, pady=2, sticky="WE")
        self.biasEntry = tk.Entry(self.biasFrame, width=10)
        self.biasEntry.grid(row=0, column=1, padx=1, pady=3, sticky="WE")

        # Star list
        self.darkTitleLabel = tk.Label(self.biasFrame, text="Dark List:")
        self.darkTitleLabel.grid(sticky="W")
        self.listFrame = tk.Frame(self)
        self.listFrame.grid()

        self.numPoseLabel = tk.Label(self.listFrame, text="Num Pose")
        self.numPoseLabel.grid(row=0, column=0, padx=1, pady=2, sticky="WE")
        self.timePoseLabel = tk.Label(self.listFrame, text="Time Pose")
        self.timePoseLabel.grid(row=0, column=1, padx=1, pady=2, sticky="WE")

        self.numEntries = []
        self.timeEntries = []

        first_num_entry = tk.Entry(self.listFrame, width=10)
        first_num_entry.grid(row=1, column=0, padx=1, pady=3, sticky="WE")
        self.numEntries.append(first_num_entry)
        first_time_entry = tk.Entry(self.listFrame, width=10)
        first_time_entry.grid(row=1, column=1, padx=1, pady=3, sticky="WE")
        self.timeEntries.append(first_time_entry)

        self.darkList = []
        self.listDim = 1

        # Add Dark Button
        self.addButton = tk.Button(self, text="+", command=self.add_dark)
        self.addButton.grid(padx=3, pady=2)

        # Generate Master Button
        self.masterButton = tk.Button(self, text="Generate Master", command=self.gen_master, width=25)
        self.masterButton.grid(padx=3, pady=2, sticky="WE")

    # Add master dark line
    def add_dark(self):
        print("ADD DARK")

        print("Adding a new dark line")

        self.listDim += 1

        new_num_entry = tk.Entry(self.listFrame, width=10)
        new_num_entry.grid(row=self.listDim, column=0, padx=1, pady=3, sticky="WE")
        self.numEntries.append(new_num_entry)

        new_time_entry = tk.Entry(self.listFrame, width=10)
        new_time_entry.grid(row=self.listDim, column=1, padx=1, pady=3, sticky="WE")
        self.timeEntries.append(new_time_entry)

        # Resize the Master Window
        base_height = self.geometryBase.height
        new_height = base_height + STARL_EN_HG * (self.listDim - 1)
        base_width = self.geometryBase.width
        self.geometry(str(base_width) + "x" + str(new_height))

    # Generate master dark and bias files
    def gen_master(self):
        print("GEN MASTER")

        ws_path = self.master.wsPath
        list_dim = self.listDim
        bias_pose = int(rm_spaces(self.biasEntry.get()))

        for i in range(0, list_dim):
            pose = int(rm_spaces(self.numEntries[i].get()))
            dark_time = int(rm_spaces(self.timeEntries[i].get()))
            dark_info = DarkInfo(pose, dark_time)
            self.darkList.append(dark_info)
        dark_list = self.darkList

        mf.make_DARK(ws_path, dark_list, list_dim)
        mf.make_ListaBias(ws_path, bias_pose)
        mf.make_CreaMasterDb(ws_path, dark_list, list_dim)

        # Close Master window
        print("Closing Master window...")
        self.destroy()
        return


if __name__ == "__main__":
    # Main window
    mainFrame = MainWindow()

    # ttk style
    style = ttk.Style(mainFrame)
    style.configure(OM_STYLE, background=OM_BG, foreground=OM_FG)

    # Run application
    mainFrame.mainloop()
