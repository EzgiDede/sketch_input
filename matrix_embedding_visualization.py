# This creates a matrix with Quick draw categories. To find the most similar instances in a given embedding file.

import numpy as np
import os
from quickdraw import QuickDrawData
import cv2 as cv2
from scipy.spatial import distance as dstnc
import PIL.Image


embedding_file_name_endswith = "embeddings_new.npz"
number_of_categories = 345
reference_dict = dict()
centroids = dict()
matrix_info = []  # 345x345 matrix list [row_category_name, column_category_name, key_id]

categories_trial = ['arm', 'bandage', 'baseball', 'bathtub', 'bed', 'bee', 'boomerang', 'calendar', 'camera', 'castle',
              'cell phone', 'cello', 'circle', 'clarinet', 'diamond', 'dog', 'dolphin', 'duck', 'eye', 'finger',
              'fireplace', 'flashlight', 'flip flops', 'flying saucer', 'hammer', 'headphones', 'hospital',
              'hot air balloon', 'lighter', 'marker', 'matches', 'mouse', 'moustache', 'owl', 'paint can', 'paintbrush',
              'passport', 'peas', 'penguin', 'pizza', 'power outlet', 'rabbit', 'radio', 'rainbow', 'remote control',
              'sailboat', 'skateboard', 'skyscraper', 'sleeping bag', 'snowflake', 'soccer ball', 'star', 'stop sign',
              'swing set', 'syringe', 't-shirt', 'tooth', 'tree', 'underwear', 'van']


def read_embedding_file():
    directory = "./embeddings_dir/"
    for filename in os.listdir(directory):
        if filename.endswith(embedding_file_name_endswith):
            file_name = filename
            embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
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
                    reference_dict[class_name] = [[key_id], [embed_vector]]

    for key in reference_dict.keys():
        category_wise_embeddings = np.array(reference_dict[key][1])
        category_centroid = np.average(category_wise_embeddings, axis=0)
        centroids[key] = category_centroid


def distance_calculation():

    #with open('googleqd_categories') as f:
        #categories = [line.rstrip() for line in f]

    categories = categories_trial      # THIS WILL BE DELETED
    for categ_x in categories:
        row_name = categ_x
        for categ_y in categories:
            column_name = categ_y
            embedding_list = reference_dict[categ_x][1]
            current_centroid = centroids[categ_y]
            minimum_distance = 0
            minimum_idx = 0
            index = -1
            for vector in embedding_list:
                index += 1
                distance = dstnc.euclidean(vector, current_centroid)
                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_idx = index
            chosen_key_id = reference_dict[categ_x][0][minimum_idx]
            matrix_info.append([row_name, column_name, chosen_key_id])


def visualize_the_matrix(number_of_categories):

    for cell in matrix_info:
        row_source = cell[0]
        column_target = cell[1]
        the_id = cell[2]

        qd = QuickDrawData()
        doodle = qd.get_drawing(row_source)
        while not doodle.key_id == the_id:
            doodle = qd.get_drawing(row_source)
            found = True
        if found:
            DEFAULT_SIZE_WHITE_CHANNEL = (1000, 1000, 1)
            canvas = np.ones(DEFAULT_SIZE_WHITE_CHANNEL, dtype="uint8") * 255
            cv2.namedWindow('Window')
            my_stroke_list = doodle.image_data
            for N in my_stroke_list:
                x_list = N[0]
                y_list = N[1]
                for point in range((len(x_list) - 1)):
                    cv2.line(canvas, (x_list[point], y_list[point]), (x_list[point + 1], y_list[point + 1]), (0, 0, 0),
                             2)
            cv2.imwrite(
                "./png_sketches/latent_png/" + "source_" + row_source + "_" + "target_" + column_target + "_" + ".png",
                canvas)

    row_index = -1

    for source_categ in reference_dict.keys():
        row_index += 1
        column_index = -1
        for target_categ in reference_dict.keys():
            column_index += 1
            new_im = PIL.Image.new('RGB', (number_of_categories * 1000, number_of_categories * 1000), (250, 250, 250))
            img = PIL.Image.open(
                "./png_sketches/latent_png/" + "source_" + source_categ + "_" + "target_" + target_categ + "_" + ".png")
            new_im.paste(img, (column_index * 1000 +100, row_index * 1000 +100))

    new_im.save("./merged_images/" + "matrix" + ".png", "PNG")
    new_im.show()
    folder = "./png_sketches/latent_png/"
    for file in os.listdir(folder):
        os.remove(folder + file)


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
visualize_the_matrix(len(categories_trial))