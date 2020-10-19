
import numpy as np
import json as json
import time
import random
import os
import util_npz as util

np.set_printoptions(precision=8, edgeitems=6, linewidth=200, suppress=True)

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



