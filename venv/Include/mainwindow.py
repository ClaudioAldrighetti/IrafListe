""" Main Window
author: Aldrighetti Claudio

description:
Principal dialog that allows to:
* Select the workspace of the project;
* Insert star and reference star into the star list;
* Insert master bias and dark into the master list.
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

# Local python files
from starwindow import StarListWindow
from masterwindow import MasterListWindow
import maketk as mtk
from winconfig import *
from utility import BIAS, DARK, rm_spaces, is_standard, str_is_positive_int, resized_window
from spectrographs import SPEC_INFO, ADD, MOD, DEL, get_spec_info, SpecWindow


# Main window class
class MainWindow(tk.Tk):
    """
    Implement principal window of the program.

    Fields
    ------
    wsPath : str
        Workspace path of the project, where IRAF command files are created.
    starList : StarInfo[]
        List of information about selected stars, is filled when the session is launched.
    starListDim : int
        Number of selected star (size of the star list).
    refName : str
        Reference star name.
    refPose : int
        Reference pose index.
    specVal : tk.StringVar
        Spectrograph used for the current session.
    masterListDim : int
        Dimension of the master list.
    masterFlag : boolean
        Flag that indicates if the temporary master list is empty or not, True means that there is at least one master.

    Methods
    -------
    select_ws_path()
        Open a dialog for the user to chose/change the workspace directory for the project, where the IRAF command
        files are created.
    add_star()
        Add the chosen star to the star list and open/update the StarWindow dialog.
    remove_star(record_to_remove)
        Remove the record at the passed index from StarWindow and the relative star from the star list; if there are no
        stars remaining, it also closes the StarWindow dialog.
    select_ref()
        Set the specified star as reference star for the current session. The selected star must already exist in the
        star list.
    set_spec()
        Add a new spectrograph to the list of the existing ones or modify the selected spectrograph by opening a new
        SpecWindow dialog. For the first case, the information is stored in the spectrographs.csv file.
    del_spec()
        Remove the selected spectrograph from the spectrograph list and csv file.
    gen_syn()
        Generate the synthesis of the session by opening the correlated dialog.
    add_master(master_type)
        Add the inserted master bias/dark to the master list. MasterWindow dialog is opened/updated.
    remove_master(record_to_remove)
        Remove the master at the given index in the list.
    restart()
        Restart the session, it also closes others dialog.
    """

    """
    Initialize 
    """
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
        self.starListDim = 0
        self.starListWindow = None

        # Reference star interface
        self.refButton = mtk.make_Button(self.settingFrame, self.select_ref,
                                         text="Choose reference", row=2, state=tk.DISABLED)
        self.refLabel = mtk.make_Label(self.settingFrame, text="New REF:", row=2, column=1, state=tk.DISABLED)
        self.refEntry = mtk.make_Entry(self.settingFrame, row=2, column=2, state=tk.DISABLED)

        self.standardVar = tk.IntVar(value=1)
        self.standardCheck = mtk.make_Checkbutton(self.settingFrame, self.standardVar, text="No Standard", row=3,
                                                  state=tk.DISABLED, offvalue=1, onvalue=0)

        self.curRefLabel = mtk.make_Label(self.settingFrame, text="Selected REF:", row=3, column=1, state=tk.DISABLED)
        self.curRefEntry = mtk.make_Entry(self.settingFrame, row=3, column=2, state=tk.DISABLED)

        self.refName = None
        self.refPose = None

        # Spectrograph selection interface
        self.specLabel = mtk.make_Label(self.settingFrame, text="Spectrograph:", row=4, column=1, state=tk.DISABLED)

        self.specVal = tk.StringVar(self)
        spec_name_list = (specInfo.name for specInfo in SPEC_INFO)
        self.specOptions = mtk.make_OptionMenu(self.settingFrame, self.specVal, spec_name_list,
                                               defaultval=SPEC_INFO[0].name, row=4, column=2, state=tk.DISABLED)

        self.addSpecButton = mtk.make_Button(self.settingFrame, command=lambda mode=ADD: self.set_spec(mode),
                                             text="Add New SPEC", row=5, padx=2, state=tk.DISABLED)
        self.modSpecButton = mtk.make_Button(self.settingFrame, command=lambda mode=MOD: self.set_spec(mode),
                                             text="Modify SPEC", column=1, row=5, padx=2, state=tk.DISABLED)
        self.delSpecButton = mtk.make_Button(self.settingFrame, self.del_spec,
                                             text="Delete SPEC", column=2, row=5, padx=2, state=tk.DISABLED)

        self.specWindow = None

        # Synthesis Button
        self.synButton = mtk.make_Button(self, self.gen_syn, text="Generate Synthesis",
                                         state=tk.DISABLED, grid_flag=False, fill="x", padx=5)
        self.synWindow = None
        self.sepSynMaster = mtk.make_Separator(self)

        # Master frame
        self.masterFrame = tk.Frame(self, bg=FR_BG)
        self.masterFrame.pack()

        # Master dark interface
        self.darkButton = mtk.make_Button(self.masterFrame, command=lambda spec_type=DARK: self.add_master(spec_type),
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
        self.biasButton = mtk.make_Button(self.masterFrame, command=lambda spec_type=BIAS: self.add_master(spec_type),
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

        return

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

        # self.wsEntry.configure(state=tk.NORMAL)
        mtk.clear_Entry(self.wsEntry, tk.NORMAL)
        self.wsEntry.insert(0, self.wsPath)
        self.wsEntry.configure(state="readonly")

        self.starEntry.configure(state=tk.NORMAL)
        self.starLabel.configure(state=tk.NORMAL)
        self.starButton.configure(state=tk.NORMAL)

        self.standardCheck.configure(state=tk.NORMAL)

        self.specLabel.configure(state=tk.NORMAL)
        self.specOptions.configure(state=tk.NORMAL)
        self.addSpecButton.configure(state=tk.NORMAL)
        self.modSpecButton.configure(state=tk.NORMAL)
        self.delSpecButton.configure(state=tk.NORMAL)

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
            mtk.entry_err_blink(self.starEntry)
            return
        elif self.starListWindow is None:
            # Open star list window
            print("Opening star list window...")
            self.starListWindow = StarListWindow()
            self.refButton.configure(state=tk.NORMAL)
            self.refLabel.configure(state=tk.NORMAL)
            self.refEntry.configure(state=tk.NORMAL)
        else:
            for i in range(0, self.starListDim):
                i_star = self.starListWindow.starEntries[i]
                if star_name == i_star:
                    print("Error: star is already in the list!")
                    mtk.entry_err_blink(self.starEntry)
                    return
        mtk.clear_Entry(self.starEntry)

        self.starListDim += 1
        list_dim = self.starListDim
        list_frame = self.starListWindow.listFrame

        # Add new record on the star list window
        print("Adding a new record on the star list window...")
        self.starListWindow.starEntries.append(star_name)
        self.starListWindow.posesEntries.append('')
        self.starListWindow.flatEntries.append(5)
        self.starListWindow.neonEntries.append(3)
        self.starListWindow.darkEntries.append('')
        self.starListWindow.standardEntries.append('')

        self.starListWindow.starEntry.menu.add_command(label=star_name,
                                                       command=lambda name=star_name:
                                                       self.starListWindow.select_name(name))

        if list_dim == 1:
            self.starListWindow.select(0)
        else:
            self.starListWindow.infoWindow.refresh()

        print("New star added successfully")
        return

    # Remove a star from the list
    def remove_star(self, index):
        print("REMOVE STAR")

        name_to_remove = self.starListWindow.starEntries[index]

        # Check if the star to remove is the reference star
        if is_standard(name_to_remove) and self.curRefEntry.get() == name_to_remove:
            print("Removing reference information...")
            self.curRefLabel.configure(state=tk.DISABLED)
            mtk.clear_Entry(self.curRefEntry)
            self.starListWindow.refLabel.configure(state=tk.DISABLED)
            mtk.clear_Entry(self.starListWindow.refEntry)
            self.starListWindow.refPoseLabel.configure(state=tk.DISABLED)
            mtk.clear_Entry(self.starListWindow.refPoseEntry, tk.DISABLED)

        self.starListWindow.starEntries.pop(index)
        self.starListWindow.posesEntries.pop(index)
        self.starListWindow.flatEntries.pop(index)
        self.starListWindow.neonEntries.pop(index)
        self.starListWindow.darkEntries.pop(index)
        self.starListWindow.standardEntries.pop(index)

        self.starListDim -= 1

        if self.starListDim == 0:
            print("Closing star list window...")
            self.starListWindow.close()
        else:
            self.starListWindow.select(0, False)
            self.starListWindow.infoWindow.refresh()

        print("Star removed correctly")
        return

    # Add reference star
    def select_ref(self):
        print("SELECT REF")

        # Check ref name
        print("Checking inserted name...")
        ref_name = rm_spaces(self.refEntry.get())
        if not ref_name:
            print("Error: insert a star name!")
            mtk.entry_err_blink(self.refEntry)
            return

        for i in range(0, self.starListDim):
            if ref_name != self.starListWindow.starEntries[i]:
                continue

            # Set reference star
            print("Setting the reference star...")
            self.refName = ref_name

            mtk.clear_Entry(self.refEntry)

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

        print("Error: invalid reference star name!")
        mtk.entry_err_blink(self.refEntry)
        return

    def set_spec(self, mode):
        print("SET SPEC")

        if (mode != MOD) and (mode != ADD):
            print("Error: invalid mode!")
            return

        self.specLabel.configure(state=tk.DISABLED)
        self.specOptions.configure(state=tk.DISABLED)
        self.addSpecButton.configure(state=tk.DISABLED)
        self.modSpecButton.configure(state=tk.DISABLED)
        self.delSpecButton.configure(state=tk.DISABLED)

        print("Opening spectrograph window...")
        spec_info = None
        if mode == MOD:
            spec_info = get_spec_info(self.specVal.get())
        self.specWindow = SpecWindow(self, mode, spec_info)
        return

    def del_spec(self):
        print("DEL SPEC")

        spec_name = self.specVal.get()
        message = "The selected spectrograph (" + spec_name + ") will be removed, do you want to proceed?"
        if not messagebox.askokcancel("Delete Spectrograph", message):
            print("Spectrograph hasn't been deleted")
            return

        print("Opening spectrograph window...")
        spec_to_delete = get_spec_info(spec_name)
        self.specWindow = SpecWindow(self, DEL, spec_to_delete)
        return

    def update_spec(self, curr_spec=None):
        from spectrographs import SPEC_INFO

        if not (curr_spec is None):
            self.specVal.set(curr_spec)

        self.specOptions["menu"].delete(0, "end")
        spec_name_list = (spec_info.name for spec_info in SPEC_INFO)
        for spec_name in spec_name_list:
            self.specOptions["menu"].add_command(label=spec_name, command=lambda name=spec_name: self.specVal.set(name))

        print("Spec options menu updated successfully")
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
            print("Checking master time...")
            if not str_is_positive_int(master_time):
                print("Error: invalid master time value!")
                err_flag = True
            else:
                master_time = int(master_time)
                if not (self.masterListWindow is None):
                    for i in range(0, self.masterListDim):
                        if self.masterListWindow.typeEntries[i].get() == BIAS:
                            continue

                        i_time = int(self.masterListWindow.timeEntries[i].get())
                        if master_time == i_time:
                            print("Error: master dark with such pose time already exists!")
                            err_flag = True
                            break

        master_poses = rm_spaces(poses_entry.get())
        print("Checking master poses...")
        if not str_is_positive_int(master_poses):
            print("Error: invalid master poses value!")
            err_flag = True
        else:
            master_poses = int(master_poses)

        if err_flag:
            mtk.entry_err_blink(poses_entry)
            if master_type == DARK:
                mtk.entry_err_blink(time_entry)
            return

        mtk.clear_Entry(poses_entry)
        if bias_flag:
            self.biasButton.configure(state=tk.DISABLED)
            self.biasPosesLabel.configure(state=tk.DISABLED)
            self.biasPosesEntry.configure(state=tk.DISABLED)
        else:
            mtk.clear_Entry(time_entry)

        self.masterListDim += 1
        self.masterFlag = True

        if self.masterListWindow is None:
            # Open dark list window
            print("Opening master list window...")
            self.masterListWindow = MasterListWindow()

        list_dim = self.masterListDim
        list_frame = self.masterListWindow.listFrame

        print("Adding the master to the list...")
        new_remove_button = mtk.make_Button(list_frame, text="-", row=list_dim, pady=1,
                                            command=lambda to_remove=list_dim: self.remove_master(to_remove))
        self.masterListWindow.removeButtons.append(new_remove_button)

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
            self.masterListWindow.close()

            print("Master removed correctly")
            return

        list_dim = self.masterListDim
        for i in range(index_to_remove, list_dim):
            new_record = self.masterListWindow.typeEntries[i].grid_info().get("row")-1
            self.masterListWindow.removeButtons[i].configure(
                command=lambda to_remove=new_record: self.remove_master(to_remove))
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
        self.starListDim = 0
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

        self.standardCheck.deselect()
        self.standardCheck.configure(state=tk.DISABLED)
        self.standardVar.set(1)

        self.curRefLabel.configure(state=tk.DISABLED)
        mtk.clear_Entry(self.curRefEntry)

        self.specLabel.configure(state=tk.DISABLED)
        self.specOptions.configure(state=tk.DISABLED)
        self.addSpecButton.configure(state=tk.DISABLED)
        self.modSpecButton.configure(state=tk.DISABLED)
        self.delSpecButton.configure(state=tk.DISABLED)

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

        return

    # Synthesis report
    def syn(self):
        std_check_flag = self.master.standardVar.get()

        syn_string = ""
        for i in range(0, self.master.starListDim):
            star_info = self.master.starList[i]

            if std_check_flag and not is_standard(star_info.name):
                std_str = " Standard: " + star_info.standard + "\n"
            else:
                std_str = "\n"

            syn_string += ("STAR: " + star_info.name +
                           " N_Poses: " + str(star_info.poses) +
                           " N_Flat: " + str(star_info.flat) +
                           " N_Neon: " + str(star_info.neon) +
                           " T_Dark: " + str(star_info.dark_time) +
                           std_str)
        syn_string += "REFERENCE: " + self.master.refName + " Pose: " + str(self.master.refPose)

        self.synText.insert("end", syn_string)
        self.synText.configure(state=tk.DISABLED)
        return
