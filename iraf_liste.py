import tkinter as tk
from tkinter import filedialog as fd
import os
from sys import platform

import makefiles as mf
from utility import *

COL_ERR = "Red"
COL_NORM = "White"


# Main window class
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IRAF Liste")

        if platform == "linux":
            # Linux distribution configuration
            self.geometryBase = WinGeometry(385, 350, 100, 100)
        else:
            # Windows or other
            self.geometryBase = WinGeometry(285, 350, 100, 100)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)

        # Settings frame
        self.settingFrame = tk.Frame(self)
        self.settingFrame.pack()

        # Workspace settings
        self.wsButton = tk.Button(self.settingFrame, text="Choose WS dir", command=self.select_ws_path)
        self.wsButton.grid(row=0, column=0, padx=5, pady=3, sticky="WE")
        self.wsPath = ""

        self.wsLabel = tk.Label(self.settingFrame, text="Workspace:")
        self.wsLabel.grid(row=0, column=1, padx=0, pady=3, sticky="E")

        self.wsEntry = tk.Entry(self.settingFrame, width=15, state="readonly")
        self.wsEntry.grid(row=0, column=2, padx=0, pady=3, sticky="WE")

        # Add star interface
        self.starButton = tk.Button(self.settingFrame, text="Add star", command=self.add_star, state="disabled")
        self.starButton.grid(row=1, column=0, padx=5, pady=3, sticky="WE")

        self.starLabel = tk.Label(self.settingFrame, text="New star:", state="disabled")
        self.starLabel.grid(row=1, column=1, padx=0, pady=3, sticky="E")

        self.starEntry = tk.Entry(self.settingFrame, width=15, state="disabled")
        self.starEntry.grid(row=1, column=2, padx=0, pady=3, sticky="WE")

        # Star list
        self.starList = []
        self.listDim = 0
        self.starFrame = None

        # Reference star interface
        self.refButton = tk.Button(self.settingFrame, text="Choose reference", command=self.add_ref, state="disabled")
        self.refButton.grid(row=2, column=0, padx=5, pady=3, sticky="WE")

        self.refLabel = tk.Label(self.settingFrame, text="New REF:", state="disabled")
        self.refLabel.grid(row=2, column=1, padx=0, pady=3, sticky="E")

        self.refEntry = tk.Entry(self.settingFrame, width=15, state="disabled")
        self.refEntry.grid(row=2, column=2, padx=0, pady=3, sticky="WE")

        self.curRefLabel = tk.Label(self.settingFrame, text="Selected REF:", state="disabled")
        self.curRefLabel.grid(row=3, column=1, padx=0, pady=3, sticky="E")

        self.curRefEntry = tk.Entry(self.settingFrame, width=15, state="disabled")
        self.curRefEntry.grid(row=3, column=2, padx=0, pady=3, sticky="WE")

        self.refName = None
        self.refPose = None

        # Synthesis Button
        self.synButton = tk.Button(self, text="Generate Synthesis", command=self.gen_syn, state="disabled")
        self.synButton.pack(padx=3, pady=3, fill="x")

        self.synWindow = None

        # Master Button
        self.masterButton = tk.Button(self, text="Master Bias and Dark", command=self.open_master, state="disabled")
        self.masterButton.pack(padx=3, pady=3, fill="x")

        self.masterWindow = None

        # Close button
        self.closeButton = tk.Button(self, text="Close", command=self.destroy)
        self.closeButton.pack(side="bottom", padx=3, pady=3, fill="x")

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

        self.wsEntry.configure(state="normal", bg=COL_NORM)
        self.wsEntry.insert(0, self.wsPath)
        self.wsEntry.configure(state="readonly")

        self.starEntry.configure(state="normal")
        self.starLabel.configure(state="normal")
        self.starButton.configure(state="normal")
        self.masterButton.configure(state="normal")
        return

    # Add a star to the list
    def add_star(self):
        print("ADD STAR")

        # Check star name
        print("Checking inserted name...")
        star_name = rm_spaces(self.starEntry.get())
        self.starEntry.delete(0, "end")
        if not star_name:
            print("Error: insert a star name!")
            self.starEntry.configure(bg=COL_ERR)
            return
        self.starEntry.configure(bg=COL_NORM)

        self.listDim += 1
        list_dim = self.listDim

        if list_dim == 1:
            # Open star list window
            print("Opening star list window...")
            self.starFrame = StarListWindow()
            self.refButton.configure(state="normal")
            self.refLabel.configure(state="normal")
            self.refEntry.configure(state="normal")

        print("Adding a new line in the star list window...")
        # New entry on the star list window
        new_star_entry = tk.Entry(self.starFrame.listFrame, width=20)
        new_star_entry.grid(row=list_dim, column=0, padx=2, pady=3, sticky="WE")
        new_star_entry.insert(0, star_name)
        new_star_entry.configure(state="readonly")
        self.starFrame.starEntries.append(new_star_entry)

        new_pose_entry = tk.Entry(self.starFrame.listFrame, width=6)
        new_pose_entry.grid(row=list_dim, column=1, padx=1, pady=3, sticky="WE")
        self.starFrame.poseEntries.append(new_pose_entry)

        new_flat_entry = tk.Entry(self.starFrame.listFrame, width=6)
        new_flat_entry.grid(row=list_dim, column=2, padx=1, pady=3, sticky="WE")
        new_flat_entry.insert(0, 5)
        self.starFrame.flatEntries.append(new_flat_entry)

        new_neon_entry = tk.Entry(self.starFrame.listFrame, width=6)
        new_neon_entry.grid(row=list_dim, column=3, padx=1, pady=3, sticky="WE")
        new_neon_entry.insert(0, 3)
        self.starFrame.neonEntries.append(new_neon_entry)

        new_dark_entry = tk.Entry(self.starFrame.listFrame, width=6)
        new_dark_entry.grid(row=list_dim, column=4, padx=1, pady=3, sticky="WE")
        self.starFrame.darkEntries.append(new_dark_entry)

        new_standard_entry = tk.Entry(self.starFrame.listFrame, width=10)
        new_standard_entry.grid(row=list_dim, column=5, padx=1, pady=3, sticky="WE")
        if is_standard(star_name):
            new_standard_entry.configure(state="disabled")
        self.starFrame.standardEntries.append(new_standard_entry)

        # Resize star list window
        if platform == "linux":
            entry_height = 29
        else:
            entry_height = 25
        base_height = self.starFrame.geometryBase.height
        new_height = base_height + entry_height * list_dim
        base_width = self.starFrame.geometryBase.width
        self.starFrame.geometry(str(base_width) + "x" + str(new_height))

        print("New star added successfully")
        return

    # Add reference star
    def add_ref(self):
        print("ADD REF")

        # Check ref name
        print("Checking inserted name...")
        ref_name = rm_spaces(self.refEntry.get())
        self.refEntry.delete(0, "end")
        if not ref_name:
            print("Error: insert a star name!")
            self.refEntry.configure(bg=COL_ERR)
            return

        for i in range(0, self.listDim):
            if ref_name == self.starFrame.starEntries[i].get():
                print("Setting the reference star...")
                # Set reference star
                self.refName = ref_name

                self.refEntry.configure(bg=COL_NORM)

                self.curRefLabel.configure(state="normal")
                self.curRefEntry.configure(state="normal")
                self.curRefEntry.delete(0, "end")
                self.curRefEntry.insert(0, ref_name)
                self.curRefEntry.configure(state="readonly")

                self.starFrame.refLabel.configure(state="normal")
                self.starFrame.refEntry.configure(state="normal")
                self.starFrame.refEntry.delete(0, "end")
                self.starFrame.refEntry.insert(0, ref_name)
                self.starFrame.refEntry.configure(state="readonly")
                self.starFrame.refPoseLabel.configure(state="normal")
                self.starFrame.refPoseEntry.configure(state="normal")

                print("Reference star set successfully")
                return

        print("Error: illegal reference star name!")
        self.refEntry.configure(bg=COL_ERR)
        return

    def open_master(self):
        print("OPEN MASTER")

        print("Opening Master window...")
        self.masterWindow = MasterWindow(self)
        return

    def gen_syn(self):
        print("GEN SYN")

        print("Opening Synthesis window...")
        self.synWindow = SynthesisWindow(self)
        return


# Star list window class
class StarListWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Star List")

        if platform == "linux":
            self.geometryBase = WinGeometry(485, 90, 110, 260)
        else:
            self.geometryBase = WinGeometry(365, 85, 110, 260)
        self.geometry(str(self.geometryBase))
        self.resizable(False, False)

        self._errFlag = False

        # Star list
        self.listFrame = tk.Frame(self)
        self.listFrame.grid()

        self.starLabel = tk.Label(self.listFrame, text="Star")
        self.starLabel.grid(row=0, column=0, padx=1, pady=2, sticky="WE")
        self.poseLabel = tk.Label(self.listFrame, text="Poses")
        self.poseLabel.grid(row=0, column=1, padx=1, pady=2, sticky="WE")
        self.flatLabel = tk.Label(self.listFrame, text="Flat")
        self.flatLabel.grid(row=0, column=2, padx=1, pady=2, sticky="WE")
        self.neonLabel = tk.Label(self.listFrame, text="Neon")
        self.neonLabel.grid(row=0, column=3, padx=1, pady=2, sticky="WE")
        self.darkLabel = tk.Label(self.listFrame, text="Dark T")
        self.darkLabel.grid(row=0, column=4, padx=1, pady=2, sticky="WE")
        self.standardLabel = tk.Label(self.listFrame, text="Standard")
        self.standardLabel.grid(row=0, column=5, padx=1, pady=2, sticky="WE")

        self.starEntries = []
        self.poseEntries = []
        self.flatEntries = []
        self.neonEntries = []
        self.darkEntries = []
        self.standardEntries = []

        # Ref frame
        self.refFrame = tk.Frame(self)
        self.refFrame.grid()

        self.refLabel = tk.Label(self.refFrame, text="REF: ", state="disabled")
        self.refLabel.grid(row=0, column=0, padx=2, pady=3, sticky="E")
        self.refEntry = tk.Entry(self.refFrame, width=15, state="disabled")
        self.refEntry.grid(row=0, column=1, padx=2, pady=3, sticky="WE")
        self.refPoseLabel = tk.Label(self.refFrame, text="REF pose: ", state="disabled")
        self.refPoseLabel.grid(row=0, column=2, padx=2, pady=3, sticky="E")
        self.refPoseEntry = tk.Entry(self.refFrame, width=5, state="disabled")
        self.refPoseEntry.grid(row=0, column=3, padx=2, pady=3, sticky="WE")

        # Start button
        self.startButton = tk.Button(self, text="Start Session", command=self.start_session)
        self.startButton.grid(padx=3, pady=2, sticky="WE")

    # Create general IRAF files
    def start_session(self):
        print("START SESSION")

        ref_pose_str = rm_spaces(self.refPoseEntry.get())
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
            self.refPoseEntry.configure(bg=COL_NORM)
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
                self.poseEntries[i].configure(bg=COL_NORM)
                star_pose = int(pose_entry_str)

            if not flat_entry_str or int(flat_entry_str) <= 0:
                print("Error: illegal flat value for star: " + star_entry + "!")
                self.flatEntries[i].configure(bg=COL_ERR)
                star_flat = None
                self._errFlag = True
            else:
                self.flatEntries[i].configure(bg=COL_NORM)
                star_flat = int(flat_entry_str)

            if not neon_entry_str or int(neon_entry_str) <= 0:
                print("Error: illegal neon value for star: " + star_entry + "!")
                self.neonEntries[i].configure(bg=COL_ERR)
                star_neon = None
                self._errFlag = True
            else:
                self.neonEntries[i].configure(bg=COL_NORM)
                star_neon = int(neon_entry_str)

            if not dark_entry_str or int(dark_entry_str) <= 0:
                print("Error: illegal dark time value for star: " + star_entry + "!")
                self.darkEntries[i].configure(bg=COL_ERR)
                star_dark = None
                self._errFlag = True
            else:
                self.neonEntries[i].configure(bg=COL_NORM)
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
                        self.standardEntries[i].configure(bg=COL_NORM)
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
        mf.make_GeneraMasterFlat(ws_path, star_list, list_dim, 10, 280, 281)    # TODO
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

        print("All initial files have been created successfully")

        # Enable Synthesis button
        self.master.synButton.configure(state="normal")

        # Disable first part
        self.master.wsButton.configure(state="disabled")
        self.master.wsLabel.configure(state="disabled")
        self.master.wsEntry.configure(state="disabled")

        self.master.starButton.configure(state="disabled")
        self.master.starLabel.configure(state="disabled")
        self.master.starEntry.configure(state="disabled")

        self.master.refButton.configure(state="disabled")
        self.master.refLabel.configure(state="disabled")
        self.master.refEntry.configure(state="disabled")
        self.master.curRefLabel.configure(state="disabled")
        self.master.curRefEntry.configure(state="disabled")

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
        self.maxsize(600, 350)

        # self.yScroll = tk.Scrollbar(self)
        # self.yScroll.pack(side="right", fill="y")

        # Synthesis
        self.synText = tk.Text(self, state="normal")    # , yscrollcommand=self.yScroll.set)
        self.synText.pack(expand=True)

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

        self._errFlag = False

        # Bias Frame
        self.biasFrame = tk.Frame(self)
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
        if platform == "linux":
            entry_height = 29
        else:
            entry_height = 25
        base_height = self.geometryBase.height
        new_height = base_height + entry_height * (self.listDim-1)
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


# Main window
mainFrame = MainWindow()

# Run application
mainFrame.mainloop()