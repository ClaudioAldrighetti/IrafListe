# Spectrographs stuff
import csv
import os.path as opt

from utility import CURR_DIR, SpecInfo


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
        ))
    spec_file.close()
    return spec_list


# Spectrographs list with data (name, min_h_pixel, max_h_pixel, h_image, l_row)
SPEC_INFO = retrieve_spectrographs()
# SPEC_INFO = [
#     SpecInfo("Alpy + ASI294", 10, 280, 281, 270),
#     SpecInfo("LHIRESS + ATIK460ex", 10, 280, 281, 270)
#     ...
# ]
