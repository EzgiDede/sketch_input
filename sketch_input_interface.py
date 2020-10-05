import cv2
import ndjson as ndjson
import numpy as np
import time
from rdp import rdp
import rdp as rdp_lib
import math


""" To record the drawings to the Drive folder.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

"""

drawing = False # true if mouse is pressed
image = [] #holds the image as the array of strokes
stroke = [] #each stroke is composed of x and y values of significant points
counter = 1
simple_output = []


# mouse callback function
def interactive_drawing(event,x,y,flags,param):
    global x_start, y_start, drawing, mode, start_time, counter, stroke, image

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        x_start, y_start = x,y
        start_time = time.time_ns() #takes the time in nanoseconds
        stroke.append([x])
        stroke.append([y])
        if counter == 1:
            stroke.append([0])
        else:
            stroke.append([counter*5])

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            point1 = (x_start, y_start)
            point2 = (x,y)
            cv2.line(canvas,point1,point2,(0,0,0),2)
            time_elapsed = time.time_ns() - start_time
            if time_elapsed >= (5*10^7)/2:
                if (x_start != x) & (y_start != y):
                    stroke[0].append(x)
                    stroke[1].append(y)
                    stroke[2].append(10*counter)
                    counter += 1
            x_start, y_start = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing=False
        image.append(stroke)
        stroke = []


def simplification():
    """
    Quick draw simplification steps that are described as follows:
    Step-1: Align the drawing to the top-left corner, to have minimum values of 0.
    Step-2: Uniformly scale the drawing, to have a maximum value of 255.
    Step-3: Resample all strokes with a 1 pixel spacing. (Interpolation)
    Step-4: Simplify all strokes using the Ramer–Douglas–Peucker algorithm with an epsilon value of 2.0.
    """
    global image, simple_output

    # For Step-1 alignment, I'll find the bounding box top-left corner coordinates to align it with the origin.
    minimum_value_x = np.amin(image[0][0])
    minimum_value_y = np.amin(image[0][1])
    for strokes in image:   # for each stroke
        if np.amin(strokes[0]) < minimum_value_x:   # find the min x of them all.
            minimum_value_x = np.amin(strokes[0])

        if np.amin(strokes[1]) < minimum_value_y:   # find the min y of them all.
            minimum_value_y = np.amin(strokes[1])

    bounding_point = [minimum_value_x, minimum_value_y]


    # Now I'll drag the image to the origin.
    dragged_image = []
    for strokes_s in image:
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


    """
    # For Step-3: All strokes should include points with 1 pixel distance from each-other:
    # We may need exception handling here. - Ezgi. (What if for loop starts with range(0)?)
    interp_distance = 1
    step_3_drawing = []
    print("step 2")
    print(step_2_drawing)
    for strokes in step_2_drawing:
        x1 = strokes[0][0]
        y1 = strokes[1][0]
        x_list = []
        y_list = []
        for i in range(len(strokes[0]) - 1):
            x2 = strokes[0][i]
            y2 = strokes[1][i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            while distance > interp_distance:
                x_list.append(x1)
                y_list.append(y1)
                x_interp = (x2 - x1) / distance * interp_distance + x1
                y_interp = (y2 - y1) / distance * interp_distance + y1
                x1 = x_interp
                y1 = y_interp
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        x_list.append(x2)
        y_list.append(y2)
        step_3_drawing.append([x_list, y_list])
    print(step_3_drawing)
    """

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



def converter():
    image_string = str(simple_output[0])

    drawing_map = {"drawing": simple_output[0]}
    print(drawing_map)
    #with open('drawing.ndjson', 'w') as f:
    #   ndjson.dump(drawing_map, f)
    # Writing items to a ndjson file
    with open('./ndjson_files/drawing.ndjson', 'w') as f:
        writer = ndjson.writer(f, ensure_ascii=False)
        writer.writerow(drawing_map)
    # f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "1gF18VFQBYcSTxtQgCKxBjd46uVcMq3Yv"}]})
    # f.SetContentFile("drawing.ndjson")
    # f.Upload()



DEFAULT_SIZE_WHITE_CHANNEL = (800, 800, 1)
canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype = "uint8") * 255
cv2.namedWindow('Window')
cv2.setMouseCallback('Window',interactive_drawing)
while(1):
    cv2.imshow('Window',canvas)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        print(image)
        simplification()
        converter()

        break
cv2.destroyAllWindows()

