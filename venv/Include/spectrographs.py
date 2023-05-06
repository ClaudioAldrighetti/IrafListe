# Spectrographs stuff
import csv
import os.path as opt
import tkinter as tk

import maketk as mtk
from utility import rm_spaces, str_is_positive_int, CURR_DIR, SpecInfo
from winconfig import *

# SpecWindow modes
ADD = "add"
MOD = "mod"
DEL = "del"


# Retrieve spectrographs list and data from the corresponding csv file
def retrieve_spectrographs():
    spec_list = []
    spec_file_name = "spectrographs.csv"
    spec_file_path = opt.join(CURR_DIR, spec_file_name)
    spec_file = open(spec_file_path, 'r', newline='')
    spec_reader = csv.reader(spec_file)
    for record in spec_reader:
        spec_list.append(SpecInfo(
            record[0], int(record[1]), int(record[2]), int(record[3]), int(record[4]),
            int(record[5]), int(record[6]), int(record[7]), int(record[8])
        ))
    spec_file.close()
    return spec_list


# Return spectrograph data (if it exists in the list) by starting from its name
def get_spec_info(spec_name):
    for i_spec in SPEC_INFO:
        if i_spec.name == spec_name:
            return i_spec
    return None


def get_spec_index(spec_name):
    index = 0
    for i_spec in SPEC_INFO:
        if i_spec.name == spec_name:
            return index
        index += 1
    return -1


# Spectrographs list with data (name, min_h_pixel, max_h_pixel, h_image, l_row)
SPEC_INFO = retrieve_spectrographs()
# SPEC_INFO = [
#     SpecInfo("Alpy + ASI294", 10, 280, 281, 270),
#     SpecInfo("LHIRESS + ATIK460ex", 10, 280, 281, 270)
#     ...
# ]


class SpecWindow(tk.Toplevel):
    def __init__(self, master=None, mode=MOD, spec_info=None):
        super().__init__(master=master)
        # Mode flags
        self._mode = mode
        if self._mode == MOD:
            self.title("Modify Spectrograph")
            self._specIndex = get_spec_index(spec_info.name)
        elif self._mode == DEL:
            self.title("Delete Spectrograph")
            self._specIndex = get_spec_index(spec_info.name)
        elif self._mode == ADD:
            self.title("Add Spectrograph")
            # Empty spectrograph data entries
            spec_info = SpecInfo("", "", "", "", "")
        else:
            print("Error: invalid mode!")
            self.destroy()
            return

        self.defGeometry = SPEC_WIN_DEF_GEOM
        self.geometry(str(self.defGeometry))
        self.resizable(False, False)
        self.configure(bg=FR_BG)
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Spectrograph data frame
        self.specFrame = tk.Frame(self, bg=FR_BG)
        self.specFrame.pack()

        self.nameLabel = mtk.make_Label(self.specFrame, text="name:", sticky=tk.W)
        self.nameEntry = mtk.make_Entry(self.specFrame, text=spec_info.name, column=1)
        self.minHLabel = mtk.make_Label(self.specFrame, text="min_h_pixel:", row=1, sticky=tk.W)
        self.minHEntry = mtk.make_Entry(self.specFrame, text=spec_info.min_h_pixel, row=1, column=1)
        self.maxHLabel = mtk.make_Label(self.specFrame, text="max_h_pixel:", row=2, sticky=tk.W)
        self.maxHEntry = mtk.make_Entry(self.specFrame, text=spec_info.max_h_pixel, row=2, column=1)
        self.imageHLabel = mtk.make_Label(self.specFrame, text="h_image:", row=3, sticky=tk.W)
        self.imageHEntry = mtk.make_Entry(self.specFrame, text=spec_info.h_image, row=3, column=1)
        self.rowLabel = mtk.make_Label(self.specFrame, text="l_row:", row=4, sticky=tk.W)
        self.rowEntry = mtk.make_Entry(self.specFrame, text=spec_info.l_row, row=4, column=1)

        if self._mode == MOD:
            self.insertButton = mtk.make_Button(self, self.mod_spec,
                                                text="Modify Spectrograph", grid_flag=False, fill="x", padx=5)
        elif self._mode == ADD:
            self.insertButton = mtk.make_Button(self, self.add_spec,
                                                text="Add Spectrograph", grid_flag=False, fill="x", padx=5)
        else:
            self.del_spec()

        return

    def check_info(self):
        check_flag = True
        print("Checking inserted spectrograph data...")
        if not rm_spaces(self.nameEntry.get()):
            print("Error: insert a spectrograph name!")
            mtk.entry_err_blink(self.nameEntry)
            check_flag = False
        if not str_is_positive_int(rm_spaces(self.minHEntry.get())):
            print("Error: invalid minimum pixel height!")
            mtk.entry_err_blink(self.minHEntry)
            check_flag = False
        if not str_is_positive_int(rm_spaces(self.maxHEntry.get())):
            print("Error: invalid maximum pixel height!")
            mtk.entry_err_blink(self.maxHEntry)
            check_flag = False
        if not str_is_positive_int(rm_spaces(self.imageHEntry.get())):
            print("Error: invalid image height!")
            mtk.entry_err_blink(self.imageHEntry)
            check_flag = False
        if not str_is_positive_int(rm_spaces(self.rowEntry.get())):
            print("Error: invalid maximum file length!")
            mtk.entry_err_blink(self.rowEntry)
            check_flag = False
        return check_flag

    def add_spec(self):
        print("ADD SPEC")

        # Check spec data
        if not self.check_info():
            return

        # Retrieve spectrograph data from entries
        spec_info = SpecInfo(self.nameEntry.get(),
                             int(rm_spaces(self.minHEntry.get())),
                             int(rm_spaces(self.maxHEntry.get())),
                             int(rm_spaces(self.imageHEntry.get())),
                             int(rm_spaces(self.rowEntry.get())))

        # Add a new record in the csv file
        spec_file_name = "spectrographs.csv"
        spec_file_path = opt.join(CURR_DIR, spec_file_name)
        with open(spec_file_path, "a") as spec_file:
            spec_file.write(spec_info.to_csv() + "\n")
        spec_file.close()

        # Update spectrographs list
        self.update_spec_list(spec_info.name)

        print("Spectrograph added correctly")
        self.close()
        return

    def mod_spec(self):
        print("MOD SPEC")

        # Check spec data
        if not self.check_info():
            return

        # Retrieve spectrograph data from entries
        spec_info = SpecInfo(self.nameEntry.get(),
                             int(rm_spaces(self.minHEntry.get())),
                             int(rm_spaces(self.maxHEntry.get())),
                             int(rm_spaces(self.imageHEntry.get())),
                             int(rm_spaces(self.rowEntry.get())))

        spec_file_name = "spectrographs.csv"
        spec_file_path = opt.join(CURR_DIR, spec_file_name)
        with open(spec_file_path, "r") as spec_file:
            records = spec_file.readlines()
            # Modify only the corresponding record
            records[self._specIndex] = (spec_info.to_csv() + "\n")
        spec_file.close()

        with open(spec_file_path, "w") as spec_file:
            spec_file.writelines(records)
        spec_file.close()

        # Update spectrographs list
        self.update_spec_list(spec_info.name)

        print("Spectrograph modified correctly")
        self.close()
        return

    def del_spec(self):
        print("DEL SPEC")

        spec_file_name = "spectrographs.csv"
        spec_file_path = opt.join(CURR_DIR, spec_file_name)
        with open(spec_file_path, "r") as spec_file:
            records = spec_file.readlines()
        spec_file.close()

        with open(spec_file_path, "w") as spec_file:
            for i in range(0, len(records)):
                # Don't write the record at the specified index
                if i != self._specIndex:
                    spec_file.write(records[i])

        # Update spectrographs list
        if self._specIndex != 0:
            self.update_spec_list(SPEC_INFO[self._specIndex-1].name)
        else:
            self.update_spec_list(SPEC_INFO[1].name)

        print("Spectrograph deleted correctly")
        self.close()
        return

    def update_spec_list(self, curr_spec=None):
        # Update spectrographs list
        global SPEC_INFO
        SPEC_INFO = retrieve_spectrographs()

        # Update OptionMenu list
        if curr_spec is None:
            self.master.update_spec()
        else:
            self.master.update_spec(curr_spec=curr_spec)
        return

    def close(self):
        self.master.specLabel.configure(state=tk.NORMAL)
        self.master.specOptions.configure(state=tk.NORMAL)
        self.master.addSpecButton.configure(state=tk.NORMAL)
        self.master.modSpecButton.configure(state=tk.NORMAL)
        self.master.delSpecButton.configure(state=tk.NORMAL)

        # Close spectrographs window
        print("Closing spectrographs window...")
        self.master.specWindow = None
        self.destroy()
        return
