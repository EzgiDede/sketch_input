"""
03.02.21 Description by Ezgi:

This is the final method that we used to see the feature extraction abilities of our model.
It creates an excel file with category names on column 1.
At column 2-3-4 we see the most similar sketches to the category at column 1, which doesn't belong to that category.
For example, column-1 says "tree" column 2 is the sketch that resembles a tree most but it belongs to the class "flower"
At column 5, we have a sketch belongs to the source category (column 1) that resembles to the sketch at column-2.
With the same example, at column-5 we have a tree that resembles most to the flower presented in column-2.
Thus, the column 6, resembles column 3. Column 7, resembles column 4.
It also creates a tagets.txt file, by taking that as a guide, you can see the origin category of sketches presented in column 2-3-4.
P.S. I highly recommend to run this on a PC with relatively high computational power.
"""

import numpy as np
import os
from quickdraw import QuickDrawData
import cv2 as cv2
from scipy.spatial import distance as dstnc
import xlsxwriter

embedding_file_name_endswith = ".npz"
number_of_categories = 345
reference_dict = dict()
centroids = dict()
matrix_info = []  # 345x345 matrix list [row_category_name, column_category_name, key_id]

def read_embedding_file():
    global reference_dict

    directory = "./embeddings_dir/QD_150_samples_embeddings"
    for filename in os.listdir(directory):
        if filename.endswith(embedding_file_name_endswith):
            file_name = filename
            embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")  # can be optimized with
            for embedding in embeddings["embeddings"]:
                embed_vector = embedding[0]
                key_id = embedding[1]
                class_name_raw = embedding[2]
                class_name = class_name_raw.split(str(key_id))[0]
                if class_name in reference_dict.keys():
                    current_list = reference_dict[class_name]
                    current_list[0].append(key_id)
                    current_list[1].append(embed_vector)
                    reference_dict[class_name] = current_list
                else:
                    reference_dict[class_name] = [[key_id], [embed_vector]]   # This is the structure of ref_dict.

    for key in reference_dict.keys():
        category_wise_embeddings = reference_dict[key][1]
        category_centroid = np.average(category_wise_embeddings, axis=0)
        centroids[key] = category_centroid      # {class_name: centroid vector, ... }


def distance_calculation():
    with open('./googleqd_categories') as f:
        categories = [line.rstrip() for line in f]

    for categ_x in categories:
        row_name = categ_x
        current_centroid = centroids[categ_x]

        min_dis_one = 9223372036854775807
        min_dis_two = 9223372036854775807
        min_dis_three = 9223372036854775807

        minimum_idx_three = -1
        minimum_idx_two = -1
        minimum_idx_one = -1

        minimum_categ_three = categ_x
        minimum_categ_two = categ_x
        minimum_categ_one = categ_x

        for categ_y in categories:
            if categ_y != categ_x:
                column_name = categ_y
                embedding_list = (reference_dict[categ_y])[1]

                index = -1
                for vector in embedding_list:
                    index += 1
                    distance = dstnc.euclidean(vector, current_centroid)

                    if distance < min_dis_one:

                        min_dis_three = min_dis_two
                        min_dis_two = min_dis_one
                        min_dis_one = distance

                        minimum_categ_three = minimum_categ_two
                        minimum_categ_two = minimum_categ_one
                        minimum_categ_one = categ_y

                        minimum_idx_three = minimum_idx_two
                        minimum_idx_two = minimum_idx_one
                        minimum_idx_one = index


                    elif distance < min_dis_two:

                        min_dis_three = min_dis_two
                        min_dis_two = distance

                        minimum_categ_three = minimum_categ_two
                        minimum_categ_two = categ_y

                        minimum_idx_three = minimum_idx_two
                        minimum_idx_two = index

                    elif distance < min_dis_three:

                        min_dis_three = distance

                        minimum_idx_three = index

                        minimum_categ_three = categ_y

        chosen_key_id_one = ((reference_dict[minimum_categ_one])[0])[minimum_idx_one]

        chosen_key_id_two = ((reference_dict[minimum_categ_two])[0])[minimum_idx_two]

        chosen_key_id_three = ((reference_dict[minimum_categ_three])[0])[minimum_idx_three]

        chosen_key_ids = [chosen_key_id_one, chosen_key_id_two, chosen_key_id_three]

        minimum_categ_name = [minimum_categ_one, minimum_categ_two, minimum_categ_three]

        # Now I need to find most similar sketches to those minimum ones from categ_x sketches.
        # That was the confusing one:

        target_vector_list = []

        m = -1
        for target_name in minimum_categ_name:
            m += 1
            m_idx = -1
            for i in (reference_dict[target_name])[0]:
                m_idx += 1
                if chosen_key_ids[m] == i:      # found the index m_idx
                    target_vector = (reference_dict[target_name])[1][m_idx]
                    target_vector_list.append(target_vector)

        similar_source_sketch_ids = []   # contains three key_ids of categ_x (source) category sketches.

        for target_point in target_vector_list:     # target_point is the vector of one of the most similar sketch to categ_x.
            min_distance = 9223372036854775807
            minimum_idx_target = -1
            index_target = -1
            for sketch in ((reference_dict[categ_x])[1]):  # iterate over all source catgories to find the most similar one to the target point.
                index_target += 1
                target_distance = dstnc.euclidean(sketch, target_point)
                if target_distance < min_distance:
                    min_distance = target_distance
                    minimum_idx_target = index_target

            target_id = (reference_dict[categ_x])[0][minimum_idx_target]
            similar_source_sketch_ids.append(target_id)

        # matrix_info.append([row_name, column_name, chosen_key_id])
        matrix_info.append([row_name, minimum_categ_name, chosen_key_ids, similar_source_sketch_ids])

        content_file = "./targets.txt"
        f = open(content_file, "a")
        f.write(str([row_name, minimum_categ_name, chosen_key_ids, similar_source_sketch_ids]) + "\n")
        f.close()


def visualize_the_matrix(number_of_categories):
    for obj in matrix_info:
        row_source = obj[0]
        for i in range(3):
            column_target = (obj[1])[i]
            the_id = (obj[2])[i]
            most_similar_source_id = (obj[3])[i]

            # Find the most similar target sketches.
            qd = QuickDrawData()
            doodle = qd.get_drawing(column_target)
            while not doodle.key_id == the_id:
                doodle = qd.get_drawing(column_target)
            found = True
            if found:
                DEFAULT_SIZE_WHITE_CHANNEL = (300, 300, 1)
                canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255
                cv2.namedWindow('Window')
                my_stroke_list = doodle.image_data
                for N in my_stroke_list:
                    x_list = N[0]
                    y_list = N[1]
                    for point in range((len(x_list) - 1)):
                        cv2.line(canvas, (x_list[point], y_list[point]), (x_list[point + 1], y_list[point + 1]),
                                 (0, 0, 0),
                                 2)
                cv2.imwrite(
                    "./png_sketches/trial_pngs" + "source_" + row_source + "_" + str(
                        i) + ".png",
                    canvas)

        for i in range(3):
            column_target = (obj[1])[i]
            the_id = (obj[2])[i]
            most_similar_source_id = (obj[3])[i]

            # Find the most similar target sketches.
            qd = QuickDrawData()
            doodle = qd.get_drawing(row_source)
            while not doodle.key_id == most_similar_source_id:
                doodle = qd.get_drawing(row_source)
            found = True
            if found:
                DEFAULT_SIZE_WHITE_CHANNEL = (300, 300, 1)
                canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255
                cv2.namedWindow('Window')
                my_stroke_list = doodle.image_data
                for N in my_stroke_list:
                    x_list = N[0]
                    y_list = N[1]
                    for point in range((len(x_list) - 1)):
                        cv2.line(canvas, (x_list[point], y_list[point]), (x_list[point + 1], y_list[point + 1]),
                                 (0, 0, 0),
                                 2)
                cv2.imwrite(
                    "./png_sketches/trial_pngs" + "source_" + row_source + "_" + str(
                        i) + "_sourceimage.png",
                    canvas)

    excel = xlsxwriter.Workbook(
        "./png_sketches/" + "matrix_six_with_targets" + ".xlsx")
    worksheet = excel.add_worksheet()
    worksheet.set_default_row(300)
    worksheet.set_column('A:ZZ', 50)

    row_index = -1
    column_empty = True

    for source_categ in reference_dict.keys():
        row_index += 1
        column_index = -1
        for ordered in range(6):
            column_index += 1
            if ordered <3:
                pic = "./png_sketches/trial_pngs" + "source_" + source_categ + "_" + str(
                    ordered) + ".png"
                worksheet.insert_image(row_index + 1, column_index + 1, pic)

                if column_empty:
                    worksheet.write(0, column_index + 1, ("target_similar" + str(ordered+1)))
            else:
                pic = "./png_sketches/trial_pngs" + "source_" + source_categ + "_" + str(
                    ordered-3) + "_sourceimage.png"
                worksheet.insert_image(row_index + 1, column_index + 1, pic)

                if column_empty:
                    worksheet.write(0, column_index + 1, ("source_similar_to" + str(ordered -2)))

        column_empty = False
        worksheet.write(row_index + 1, 0, source_categ)

    excel.close()


""" Old version of the matrix.

    for source_categ in reference_dict.keys():
        row_index += 1
        column_index = -1
        for target_categ in reference_dict.keys():
            column_index += 1
            new_im = PIL.Image.new('RGB', (number_of_categories * 300, number_of_categories * 300), (250, 250, 250))
            img = PIL.Image.open(
                "./png_sketches/latent_png/" + "source_" + source_categ + "_" + "target_" + target_categ + "_" + ".png")
            new_im.paste(img, (column_index * 300 +100, row_index * 300 +100))

    new_im.save("./merged_images/" + "matrix" + ".png", "PNG")
    new_im.show()
    folder = "./png_sketches/latent_png/"
    for file in os.listdir(folder):
        os.remove(folder + file)
"""

"""
categories = ['arm', 'bandage', 'baseball', 'bathtub', 'bed', 'bee', 'boomerang', 'calendar', 'camera', 'castle',
              'cell phone', 'cello', 'circle', 'clarinet', 'diamond', 'dog', 'dolphin', 'duck', 'eye', 'finger',
              'fireplace', 'flashlight', 'flip flops', 'flying saucer', 'hammer', 'headphones', 'hospital',
              'hot air balloon', 'lighter', 'marker', 'matches', 'mouse', 'moustache', 'owl', 'paint can', 'paintbrush',
              'passport', 'peas', 'penguin', 'pizza', 'power outlet', 'rabbit', 'radio', 'rainbow', 'remote control',
              'sailboat', 'skateboard', 'skyscraper', 'sleeping bag', 'snowflake', 'soccer ball', 'star', 'stop sign',
              'swing set', 'syringe', 't-shirt', 'tooth', 'tree', 'underwear', 'van']

"""

read_embedding_file()
distance_calculation()
visualize_the_matrix(number_of_categories)