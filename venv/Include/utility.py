# Utility functions and classes

def rm_spaces(this_str):
    return "".join(this_str.split())


def is_standard(this_name):
    return this_name[:2].upper() == "HR"


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


class DarkInfo:
    def __init__(self, pose, dark_time):
        self.pose = pose
        self.dark_time = dark_time


class StarInfo:
    def __init__(self, name, pose, flat, neon, dark_time, standard, std_pose):
        self.name = name
        self.pose = pose
        self.flat = flat
        self.neon = neon
        self.dark_time = dark_time
        self.standard = standard
        self.std_pose = std_pose
