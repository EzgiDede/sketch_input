
import numpy as np
import json as json
import time
import random
import os
import util_npz as util

import numpy as np
from scipy.spatial import distance


filename = "./embeddings_dir/embeddings_flower.npz"
#filename = "./npz_files/flower_trial_new.npz"

embeddings = np.load(filename, allow_pickle=True, encoding="latin1")
# input = embeddings["sketches"]
recon_img = embeddings["recon_sketches"]
recons_vector = recon_img * 255.0
print(recons_vector)


def get_bounds(data):
    # Return bounds of data
    print("Printing data: \n")
    print(data)
    reconed_x_stepone = []
    reconed_y_stepone = []
    recon_sketch_step_one = []
    abs_x = 0
    abs_y = 0
    for i in range(len(data)):
        if data[i,2] != 255:
            temp = data[i,0]
            x = float(data[i, 0])
            y = float(data[i, 1])
            abs_x += x
            abs_y += y
            reconed_x_stepone.append(abs_x)
            reconed_y_stepone.append(abs_y)
        else:
            temp = data[i,0]
            x = float(data[i, 0])
            y = float(data[i, 1])
            abs_x += x
            abs_y += y
            reconed_x_stepone.append(abs_x)
            reconed_y_stepone.append(abs_y)
            recon_sketch_step_one.append([reconed_x_stepone, reconed_y_stepone])
            reconed_x_stepone = []
            reconed_y_stepone = []
            
    print (recon_sketch_step_one)

    return recon_sketch_step_one

get_bounds(recons_vector[0])