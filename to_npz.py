"""
03.02.21 Description by Ezgi:

This file uses util_npz.py from Google and converts the simplified ndjson files to npz files containing the sketch
as stroke-3 format.

Currently it iterates over the files in ndjson_files directory.

"""


import numpy as np
import json as json
import time
import random
import os
import util_npz as util

np.set_printoptions(precision=8, edgeitems=6, linewidth=200, suppress=True)
directory = "./ndjson_files/"

# WARNING: Class name is taken from the file name of the ndjson file.

# Multiple input option
for filename in os.listdir(directory):
    if filename.endswith(".ndjson"):
        file_name = filename.split(".")
        file_name = file_name[0]
        raw_file = open(directory + filename, 'r')
        raw_lines = raw_file.readlines()
        num_drawings = len(raw_lines)
        # print("Number of " + file_name + " that'll be converted to npz:" + str(num_drawings))

        for i in range(num_drawings):
            all_strokes = []
            raw_drawing = json.loads(raw_lines[i])['drawing']
            keys = json.loads(raw_lines[i])['key_id']
            lines = util.raw_to_lines(raw_drawing)  # stroke = [[x0,y0], [x1,y1],... [xM,yM]]  list of strokes
            strokes = util.lines_to_strokes(lines)  # strokes = [[x0, y0, p0], [x1, y1, p1],... [xM, yM, pM]] -eos.
            strokes[0, 0] = 0
            strokes[0, 1] = 0
            all_strokes.append(strokes)
            # random.shuffle(all_strokes)    # Shuffles the order of drawings (not strokes or points) to exclude ordering bias
            # saves every drawing as a separate file
            np.savez_compressed("./npz_files/" + file_name + str(keys) + ".npz", drawing=all_strokes, key_id=keys, word=file_name)

""" For Single input:

NAME = "new_drawing"
raw_file = open("./ndjson_files/" + NAME + '.ndjson' , 'r')
raw_lines = raw_file.readlines()
num_drawings = len(raw_lines)
print("Number of drawings that'll be converted to npz:" + str(num_drawings))


all_strokes = []
all_keys = []

for i in range(num_drawings):
    raw_drawing = json.loads(raw_lines[i])['drawing']
    keys = json.loads(raw_lines[i])['key_id']
    lines = util.raw_to_lines(raw_drawing)   # stroke = [[x0,y0], [x1,y1],... [xM,yM]]  list of strokes
    strokes = util.lines_to_strokes(lines)     # strokes = [[x0, y0, p0], [x1, y1, p1],... [xM, yM, pM]] -eos.
    strokes[0, 0] = 0
    strokes[0, 1] = 0
    all_strokes.append(strokes)
    all_keys.append(keys)
    # random.shuffle(all_strokes)    # Shuffles the order of drawings (not strokes or points) to exclude ordering bias
    print(all_strokes)

np.savez_compressed("./npz_files/" + NAME + ".npz", drawing=all_strokes, key_id=all_keys)


"""
