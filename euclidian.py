"""
03.02.21 Description by Ezgi:

We are NOT using this one anymore, yet we can keep it. - 03.02.21

Calculates the distances between every embedding file existing in the embeddings_dir.

Returns a dictionary named "latent_space"
key: key_id_one    --> Integer. Key id of the first sketch
values: a list of lists. An item is: [key_id_two(the sketch which we compared with the key_id), euc_distance, (class_name_one, class_name_two)])

At the end, it finds the embeddings closest to each other and embeddings most distant from each other.
"""

import numpy as np
from scipy.spatial import distance
from sklearn.manifold import TSNE
import os
import matplotlib.pyplot as plt
import pandas as pd


directory = "./embeddings_dir/"

all_embeddings = []     # a list of tuples (key_id , embedding_vector, class_name)
latent_space = dict()   # a dictionary. Keys are


for filename in os.listdir(directory):
    if filename.endswith(".npz"):
        file_name = filename
        embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        for embedding in embeddings:
            embed_vector = embedding[0]
            key_id = embedding[1]
            class_name_raw = embedding[2]
            class_name = class_name_raw.split(str(key_id))[0]
            # The outputted embedding of sketch-former will include the embedding of the sketch as well as the key_id.
            all_embeddings.append((key_id, embed_vector, class_name))

for i in range(len(all_embeddings)):
    embedding_one = all_embeddings[i][1]
    key_id_one = all_embeddings[i][0]
    class_name_one = all_embeddings[i][2]
    current_key = key_id_one
    latent_space[current_key] = []
    for j in range(len(all_embeddings)):
        embedding_two = all_embeddings[j][1]
        key_id_two = all_embeddings[j][0]
        class_name_two = all_embeddings[j][2]
        euc_distance = distance.euclidean(embedding_one, embedding_two)
        current_value = latent_space[current_key]
        current_value.append([key_id_two, euc_distance, (class_name_one, class_name_two)])
        latent_space[current_key] = current_value


print(latent_space)


def find_min_max_values():
    all_values = list(latent_space.values())
    min = 10000
    max = 0
    max_id_value = []
    max_key = 0
    min_id_value = []
    min_key = 0
    for key, value in latent_space.items():
        for item in value:
            if item[1] != 0:
                if item[1] < min:
                    min = item[1]
                    min_key = key
                    min_id_value = item[2]
            if item[1] > max:
                max = item[1]
                max_key = key
                max_id_value = item[2]

    print(min, min_id_value, min_key)

    print(max, max_id_value, max_key)


