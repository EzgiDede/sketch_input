"""
03.02.21 Description by Ezgi:

This file is used to create small samples out of the complete Quick Draw dataset by choosing:
1) number of classes to be included.
2) number of sketches to be selected for each class.

Or you can give a specific list of classes, instead of randomly choosing it by overwriting qd_categories_subsample.

It reads googleqd_categories.txt file which contains the names of 345 categories of Quick Draw.
The user specifies the number of classes to be used. It randomly creates a sub-category list with the specified size
The user specifies the number of drawings to be selected from each category.

The code returns ndjson file containing the requested number of sketches in simplified version.

Note that all selected sketches are correctly recognized by Google's classifier.

Written by İrem Karaca.
"""

from quickdraw import QuickDrawData
import ndjson
import random
import shutil


file_path = "./googleqd_categories"


def open_and_read(file_path):
    # file path is the path of the file as a string.
    object_list = []
    with open(file_path) as f:
        for line in f:
            if line != "\n":
                new_line = line.rstrip("\n")
                object_list.append(new_line)

    return object_list

def get_random_qd_categories_subsample(number_of_drawings):
    qd_categories_subsample = random.sample(open_and_read(file_path), 10)
    print("The selected categories are:")
    print(qd_categories_subsample)
#qd_categories = open_and_read(file_path)
#number_of_categories_to_subsample = 10

#qd_categories_subsample = random.sample(qd_categories, number_of_categories_to_subsample)
#print("The selected categories are:")
#print(qd_categories_subsample)

    for category in qd_categories_subsample:
        sketch_name = category
        #number_of_drawings = 20
        qd = QuickDrawData()
        doodle = qd.get_drawing(sketch_name)
        drawing_list = []
        all_keys = []
        with open("./ndjson_files/" + sketch_name + "_simplified_qd.ndjson", 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for i in range(number_of_drawings):
                while doodle.recognized is False or doodle.key_id in all_keys:
                # while doodle in drawing_list:
                    doodle = qd.get_drawing(sketch_name)
                drawing_list.append(doodle)
                drawing_map = {"word": sketch_name, "key_id": doodle.key_id, "drawing": doodle.image_data}
                if len(all_keys) > 0:
                    all_keys.append(doodle.key_id)
                else:
                    all_keys = [doodle.key_id]
                writer.writerow(drawing_map)

def get_selected_qd_categories_subsample(categories, number_of_drawings):
    print("The selected categories are:")
    print(categories)

    for cat in categories:
        sketch_name = cat
        qd = QuickDrawData()
        doodle = qd.get_drawing(sketch_name)
        drawing_list = []
        all_keys = []
        with open("./ndjson_files/" + sketch_name + "_simplified_qd.ndjson", 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for i in range(number_of_drawings):
                while doodle.recognized is False or doodle.key_id in all_keys:
                # while doodle in drawing_list:
                    doodle = qd.get_drawing(sketch_name)
                drawing_list.append(doodle)
                drawing_map = {"word": sketch_name, "key_id": doodle.key_id, "drawing": doodle.image_data}
                if len(all_keys) > 0:
                    all_keys.append(doodle.key_id)
                else:
                    all_keys = [doodle.key_id]
                writer.writerow(drawing_map)

    # Furkan's code:
    shutil.copyfile("./ndjson_files/" + sketch_name + "_simplified_qd.ndjson", "./interface_ndjson_files/" + sketch_name + "_simplified_qd.ndjson")