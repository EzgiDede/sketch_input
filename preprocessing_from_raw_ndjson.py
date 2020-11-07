"""
 This file is created to preprocess sketch data collected by our team.
 The output will be the same as the Quick Draw simplified ndjson format.
    For our sketch data collected via Glitch interface.

"""

import numpy as np
import json as json
import time
import random
import os
import cv2
import ndjson as ndjson
import time
from rdp import rdp
import rdp as rdp_lib
import math
import datetime
from itertools import groupby



def simplification(single_sketch):
    """
    Quick draw simplification steps that are described as follows:
    Step-1: Align the drawing to the top-left corner, to have minimum values of 0.
    Step-2: Uniformly scale the drawing, to have a maximum value of 255.
    Step-3: Resample all strokes with a 1 pixel spacing. (Interpolation)
    Step-4: Simplify all strokes using the Ramer–Douglas–Peucker algorithm with an epsilon value of 2.0.
    """

    simple_output = []

    # First of all we should check if the sketch is longer than 20 points.
    sketch_length = 0
    for m in single_sketch:
        try:
            sketch_length += len(m[0])
        except:
            continue



    # For Step-1 alignment, I'll find the bounding box top-left corner coordinates to align it with the origin.
    minimum_value_x = np.amin(single_sketch[0][0])
    minimum_value_y = np.amin(single_sketch[0][1])
    for strokes in single_sketch:   # for each stroke
        if np.amin(strokes[0]) < minimum_value_x:   # find the min x of them all.
            minimum_value_x = np.amin(strokes[0])

        if np.amin(strokes[1]) < minimum_value_y:   # find the min y of them all.
            minimum_value_y = np.amin(strokes[1])

    bounding_point = [minimum_value_x, minimum_value_y]


    # Now I'll drag the image to the origin.
    dragged_image = []
    for strokes_s in single_sketch:
        dragged_stroke = [[], []]
        for point in range(len(strokes_s[0])):
            old_x = strokes_s[0][point]
            old_y = strokes_s[1][point]
            new_x = old_x - bounding_point[0]
            new_y = old_y - bounding_point[1]
            dragged_stroke[0].append(new_x)
            dragged_stroke[1].append(new_y)
        dragged_image.append(dragged_stroke)


    # For Step-2, I'm trying to find the point with the highest distance from the origin for scaling purposes.
    step_2_drawing = []
    maximum_value = 0
    for strokes in dragged_image:   # for each stroke
        if np.amax(strokes[0]) > maximum_value:     # if x array has a new maximum value, note it down.
            maximum_value = np.amax(strokes[0])
        if np.amax(strokes[1]) > maximum_value:      # if y array has a bigger value, note that down.
            maximum_value = np.amax(strokes[1])

    if maximum_value > 255:
        scale_size = maximum_value/255
        for strokes in dragged_image:
            simplified_x = []
            simplified_y = []
            for point in range(len(strokes[0])):   # scaled down to have a maximum value of 255!
                simplified_point_x = (strokes[0][point]/scale_size)
                simplified_x.append(simplified_point_x)
                simplified_point_y = (strokes[1][point]/scale_size)
                simplified_y.append(simplified_point_y)
            step_2_drawing.append([simplified_x, simplified_y])

    else:
        for strokes in dragged_image:
            simplified_x = []
            simplified_y = []
            for point in range(len(strokes[0])):   # it's not necessary to scale it down.
                simplified_point_x = (strokes[0][point])
                simplified_x.append(simplified_point_x)
                simplified_point_y = (strokes[1][point])
                simplified_y.append(simplified_point_y)
            step_2_drawing.append([simplified_x, simplified_y])

    # New Step-3 to deal with the decimals.
    copied_step_2_drawing = step_2_drawing[:]
    step_3_drawing = []
    for strokes in copied_step_2_drawing:
        step_3_x = []
        step_3_y = []
        for point in strokes[0]:
            step_3_point = round(point)
            step_3_x.append(step_3_point)
        for point in strokes[1]:
            step_3_point = round(point)
            step_3_y.append(step_3_point)
        step_3_strokes = [step_3_x,step_3_y]
        step_3_drawing.append(step_3_strokes)

    # For Step-4: Simply, apply RDP algorithm with epsilon=2.0
    # We need to convert our input to [(x0,y0),(x1,y1),...] format


    rdp_input = []
    for strokes in step_3_drawing:
        rdp_stroke = []
        for i in range(len(strokes[0])):
            x_rdp_inp = strokes[0][i]
            y_rdp_inp = strokes[1][i]
            rdp_inp_point = [x_rdp_inp, y_rdp_inp]
            rdp_stroke.append((rdp_inp_point))
        rdp_input.append(rdp_stroke)

    if sketch_length < 20:
        print("WARNING: The sketch is too short to be processed. Simplification function returns the original.")
        simplification_xy_output = rdp_input
    else:
        simplification_xy_output = []
        for strokes in rdp_input:
            rdp_output = rdp_lib.rdp(strokes, epsilon=2.0)
            simplification_xy_output.append(rdp_output)

    simplification_output = []
    for strokes in simplification_xy_output:
        output_x = []
        output_y = []
        for xy_couple in strokes:
            x_output = int(xy_couple[0])
            y_output = int(xy_couple[1])
            output_x.append(x_output)
            output_y.append(y_output)
        output_stroke = [output_x, output_y]
        simplification_output.append(output_stroke)

    simple_output.append(simplification_output)
    return simple_output


def process_raw_ndjson_from_glitch(directory):

    simplified_glitch = []

    for filename in os.listdir(directory):
        if filename.endswith(".ndjson"):
            file_name = filename.split(" ")
            file_name = file_name[4]
            raw_file = open(directory + filename, 'r')
            raw_lines_str = raw_file.readlines()[0]
            raw_lines = json.loads(raw_lines_str)
            num_drawings = len(raw_lines)
            for sketch in raw_lines:   # we have a dictionary as a sketch.
                # we'll create a key_id key for dictionaries out of time stamp info.
                time_stmp_sketch = sketch["timestamp"]  # returns str
                frac = time_stmp_sketch.split("-")
                key_id = str(frac[0]) + str(frac[1]) + str(str(frac[2])[0:2])   # 8 digits
                frac = frac[2].split(":")
                key_id = key_id + str(str(frac[0])[-2]) + str(frac[1]) + str(str(frac[2])[0:2]) + "00"  # 16 digits
                sketch["key_id"] = key_id
                # class_sketch = sketch["word"]
                coord_sketch = sketch["drawing"]
                coord_sketch = [x for x in coord_sketch if x != []]   # There shouldn't be any empty stroke.
                if coord_sketch == []:
                    continue
                sketch["drawing"] = simplification(coord_sketch)
                simplified_glitch.append(sketch)
                # For every sketch, we will create a dictionary and those will be stored in the simplified_glitch list.
                # The participant source is lost now. We should group them according to the "word" value, i.e. class.

    return simplified_glitch

def sort_simplified_input_according_to_classes(simplified_glitch):

    result = []      # result is the list of dictionaries sorted by the class.
    for k, v in groupby(sorted(simplified_glitch, key=lambda x: (x["word"], x["timestamp"])), lambda x: (x["word"], x["timestamp"])):
        temp = dict(zip(('word', 'timestamp'), k))
        sub_value = list(v)
        if len(sub_value) == 1:
            temp.update(sub_value[0])
        else:
            temp.update({'new_key': sub_value})
        result.append(temp)

    previous_class = "none"
    categ_list = []
    for sketch in result:
        current_class = sketch["word"]
        if current_class != previous_class:
            # save the previous list to an ndjson file.
            file_name = previous_class.split()[0]
            # Writing items to a ndjson file
            with open('./ndjson_files/glitch_ndjson/' + file_name + '.ndjson', 'w') as f:
                writer = ndjson.writer(f, ensure_ascii=False)
                writer.writerow(categ_list)
            # create a new list for the upcoming category.
            f.close()
            categ_list = []
            previous_class = current_class
            categ_list.append(sketch)
        else:
            categ_list.append(sketch)



directory = "./raw_ndjson_files_from_birkan/"
# Every ndjson is the collection of sketches from different classes.
# The data is a one big list with only one item. We need to clear that one first.
sort_simplified_input_according_to_classes(process_raw_ndjson_from_glitch(directory))


