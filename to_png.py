import cv2
import ndjson as ndjson
import numpy as np
import os


## Open and read the ndjson file.
def open_and_read(file_path):
    # file path is the path of the file as a string.
    object_list = []
    with open(file_path) as f:
        for line in f:
            if line != "\n":
                stroke_dict_list = ndjson.loads(line)
                stroke_dict = stroke_dict_list[0]
                # now I have a dictionary named stroke_dict.
                my_stroke_list = stroke_dict.get("drawing")
                my_stroke_key_ids = stroke_dict.get("key_id")
                object_list.append([my_stroke_list, my_stroke_key_ids])

    return object_list


def visualize_strokes(object_input, file_name):
    # Takes the whole object info and divides it into strokes.
    ## N is the number of strokes.
    DEFAULT_SIZE_WHITE_CHANNEL = (256, 256, 1)
    canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255

    cv2.namedWindow('Window')

    for sketch in object_input:
        object_list = sketch[0]
        key_id = sketch[1]
        my_stroke_list = sketch[0]
        for N in my_stroke_list:
            ## Every stroke has 3 lists in it. X list, Y list and T list.
            x_list = N[0]
            y_list = N[1]
            # t_list = N[2] ## Reconstruction will ignore t_list.
            for point in range( ( len(x_list) - 1) ):
                cv2.line(canvas, (x_list[point], y_list[point]), (x_list[point+1], y_list[point+1]), (0, 0, 0), 2)

        ## Convert the output to png.
        cv2.imshow('Window', canvas)
        cv2.imwrite("./png_sketches/" + file_name + str(key_id) + ".png", canvas)
        canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255


def iterate_pngs():
    directory = "ndjson_files/"
    for filename in os.listdir(directory):
        if filename.endswith("chair_simplified_qd.ndjson"):
            file_name = (filename.split("_"))[0]
            file_path = ("./ndjson_files/" + filename)
            visualize_strokes(open_and_read(file_path), file_name)

iterate_pngs()

while(True):
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
cv2.destroyAllWindows()

