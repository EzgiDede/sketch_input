"""
author: Aslı Ağılönü
12.11.2020
Code that translates sketch arrays from npz files to png images.
The npz files consist of sketch array, the class they belong to and their id. The expected array is in stroke-3 format.

03.02.21 Description by Ezgi:
This file is especially useful to visualize the reconstruction output of transformer model.

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

    min_x = 400
    min_y = 400
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
    DEFAULT_SIZE_WHITE_CHANNEL = (800, 800, 1)
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
