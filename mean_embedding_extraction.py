import numpy as np
import os


directory = "./embeddings_dir/"

class_list = []  # string names of all classes in the data.
latent_dictionary = dict()  # class_name: np array every row is a different sketch's embedding.

for filename in os.listdir(directory):
    if filename.endswith("glitch_full_cont_embeddings.npz"):
        file_name = filename
        embeddings = np.load(directory + filename, allow_pickle=True, encoding="latin1")
        for embedding in embeddings["embeddings"]:
            embed_vector = embedding[0]
            key_id = embedding[1]
            class_name_raw = embedding[2]
            class_name = class_name_raw.split(str(key_id))[0]
            class_list.append(class_name)
            if class_name in latent_dictionary.keys():
                class_vectors = latent_dictionary[class_name]
                latent_dictionary[class_name] = np.vstack([class_vectors, embed_vector])
            else:
                latent_dictionary[class_name] = embed_vector


mean_embeddings = np.zeros((1, 3))
for categ in latent_dictionary.keys():
    categ_embedd = latent_dictionary[categ]
    categ_mean = np.mean(categ_embedd, axis=0, dtype=np.float32)
    mean_embeddings = np.vstack([mean_embeddings, np.array([categ_mean, 0000000000000000, categ])])

new_file_name = "mean_embeddings_" + file_name
np.savez_compressed("./embeddings_dir/" + new_file_name, embeddings=mean_embeddings)


