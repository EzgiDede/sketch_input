
import numpy as np
import json as json
import time
import random
import os
import util_npz as util

np.set_printoptions(precision=8, edgeitems=6, linewidth=200, suppress=True)

NAME = "drawing"
raw_file = open("./ndjson_files/" + NAME + '.ndjson' , 'r')
raw_lines = raw_file.readlines()
num_drawings = len(raw_lines)
print("Number of drawings that'll be converted to npz:" + str(num_drawings))

all_strokes = []
for i in range(num_drawings):
    raw_drawing = json.loads(raw_lines[i])['drawing']
    lines = raw_drawing
    strokes = util.lines_to_strokes(lines)
    if i % 1000 == 0:
        pass
    if len(strokes) < 20:
        continue
    strokes[0, 0] = 0
    strokes[0, 1] = 0
    all_strokes.append(strokes)

    print(all_strokes)

np.savez_compressed("./npz_files/" + NAME + ".npz", rawdata=all_strokes)



