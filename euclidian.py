import numpy as np
from scipy.spatial import distance
import os


directory = "./embeddings_dir"

# file_name = "./embeddings_dir/embeddings_flower.npz"

all_embeddings = [] # a list of tuples (key_id , embedding_vector)
for filename in os.listdir(directory):
    if filename.endswith(".npz"):
        file_name = filename
        embeddings = np.load(file_name, allow_pickle=True, encoding="latin1")
        # The outputted embedding of sketch-former will include the embedding of the sketch as well as the key_id.
        key_id = embeddings["key_id"]
        embedding = embeddings["embeddings"]
        all_embeddings.append(key_id, embedding)


"""

embedding_one = (1, 2, 3)
embedding_two = (4, 5, 6)
dst = distance.euclidean(embedding_one, embedding_two)

"""