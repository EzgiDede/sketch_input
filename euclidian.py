import numpy as np
from scipy.spatial import distance
import os


directory = "./embeddings_dir"

# file_name = "./embeddings_dir/embeddings_flower.npz"

all_embeddings = [] # a list of tuples (key_id , embedding_vector, class_name)
latent_space = {} # a dictionary. Keys are

for filename in os.listdir(directory):
    if filename.endswith(".npz"):
        file_name = filename
        embeddings = np.load(file_name, allow_pickle=True, encoding="latin1")
        # The outputted embedding of sketch-former will include the embedding of the sketch as well as the key_id.
        key_id = embeddings["key_id"]
        embedding = embeddings["embeddings"]
        class_name = embeddings["class_name"]
        all_embeddings.append((key_id, embedding, class_name))

for i in range(len(all_embeddings)):
    for j in range(len(all_embeddings)):
        embedding_one = all_embeddings[i][1]
        key_id_one = all_embeddings[i][0]
        class_name_one = all_embeddings[i][2]
        embedding_two = all_embeddings[j][1]
        key_id_two = all_embeddings[j][0]
        class_name_two = all_embeddings[j][2]
        euc_distance = distance.euclidean(embedding_one, embedding_two)
        current_key = [[class_name_one, key_id_one], [class_name_two, key_id_two]]
        if current_key not in latent_space.keys():
            latent_space[current_key] = euc_distance


