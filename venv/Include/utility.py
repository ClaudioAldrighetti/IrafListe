# Utility macros, functions and classes
from os import chdir, path, getcwd

DARK = "dark"
BIAS = "bias"

chdir(path.dirname(__file__))
CURR_DIR = str(getcwd())


def rm_spaces(this_str):
    return "".join(this_str.split())


def is_standard(this_name):
    return this_name[:2].upper() == "HR"


def str_is_positive_int(this_string):
    if (not this_string) or (not this_string.isdigit()) or (int(this_string) == 0):
        return False
    return True


def resized_window(this_window, num_record, record_dim):
    base_height = this_window.defGeometry.height
    new_height = base_height + record_dim * num_record
    base_width = this_window.defGeometry.width
    this_window.geometry(str(base_width) + "x" + str(new_height))
    return this_window


class WinGeometry:
    def __init__(self, width, height, xpos, ypos):
        self.width = width
        self.height = height
        self.xpos = xpos
        self.ypos = ypos

    def __str__(self):
        return str(self.width) + "x" + str(self.height) + "+" + str(self.xpos) + "+" + str(self.ypos)


class SpecInfo:
    def __init__(self, name, min_h_pixel, max_h_pixel, h_image, l_row):
        self.name = name
        self.min_h_pixel = min_h_pixel
        self.max_h_pixel = max_h_pixel
        self.h_image = h_image
        self.l_row = l_row

    def to_csv(self):
        return (self.name + "," +
                str(self.min_h_pixel) + "," +
                str(self.max_h_pixel) + "," +
                str(self.h_image) + "," +
                str(self.l_row))


class MasterInfo:
    def __init__(self, master_type, master_poses, master_time):
        self.master_type = master_type
        self.master_poses = master_poses
        self.master_time = master_time


class StarInfo:
    def __init__(self, name, poses, flat, neon, dark_time, standard, std_pose):
        self.name = name
        self.poses = poses
        self.flat = flat
        self.neon = neon
        self.dark_time = dark_time
        self.standard = standard
        self.std_pose = std_pose
