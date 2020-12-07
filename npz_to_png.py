
"""
author: Aslı Ağılönü
12.11.2020
Code that translates sketch arrays from npz files to png images.
The npz files consist of sketch array, the class they belong to and their id. The expected array is in stroke-3 format.
"""

import numpy as np
import cv2

#TODO Modify for multiple input
#TODO Resize canvas with sketch bounds

def resize(data):
    """
    Resizes the given data (sketch) to fit into the canvas. Default canvas assumes origin to be
    top left corner so all points have to be in the positive quadrant to be visible
    :param data: the array indicating the sketch, consists of x-y coordinates as tuples
    :return new_data: the array with x-y tuples where all values are greater than 0
    """
    min_x = 0
    min_y = 0
    offset = 5
    for point in data:
        if point[0] < min_x:
            min_x = point[0]
        if point[1] < min_y:
            min_y = point[1]
        else:
            continue
    min_x = offset + min_x * -1
    min_y = offset + min_y * -1
    new_data = []
    for point in data:
        new_x = point[0] + min_x
        new_y = point[1] + min_y
        new_data.append([new_x, new_y])
    return new_data

def convert_points(data):
    """
    Converts the sketch data given in stroke-3 format to real x-y values (instead of the change of x and y)
    :param data: sketch array in stroke-3 format. x, y and p values are given in tuples
    :return: array representation of sketch with x,y tuples
    """
    data = data[0]
    converted_data = [data[0]]
    px = data[0][0]
    py = data[0][1]
    bound_check = 0
    for point in data:
        if bound_check > 0:
            if bound_check <= len(data):
                px = px + point[0]
                py = py + point[1]
                converted_data.append([px, py])
        bound_check += 1
    converted_data = resize(converted_data)
    return converted_data

def draw_sketch(data):
    """
    Draws the given sketch representation into a canvas
    :param data: numpy object with 'drawing' key as the sketch array, 'key_id' as the id of the represented sketch and 'class' as
    the category the sketch belongs to
    """
    DEFAULT_SIZE_WHITE_CHANNEL = (256, 256, 1)
    canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255

    sketch = convert_points(data["drawing"])
    for point in range((len(sketch) - 1)):
        cv2.line(canvas, (sketch[point][0], sketch[point][1]), (sketch[point+1][0], sketch[point+1][1]), (0, 0, 0), 2)

    cv2.imshow('Window', canvas)
    cv2.imwrite("./png_sketches/steak" + ".png", canvas)
    print("Image saved")


filename = "./npz_files/steak5207397318524928.npz"
sketch = np.load(filename, allow_pickle=True, encoding="latin1")
draw_sketch(sketch)

while(True):
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
cv2.destroyAllWindows()



"""
# THIS ONE DOES NOT WORK PROPERLY - OLD CODE


import numpy as np
import json as json
import time
import random
import os
import util_npz as util

import numpy as np
from scipy.spatial import distance


#filename = "./embeddings_dir/embeddings.npz"
#filename = "./npz_files/embeddings.npz"

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

"""