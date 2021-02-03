"""
03.02.21 Description by Ezgi:

We are NOT using this one anymore, yet we can keep it. - 03.02.21

It visualizes the distances between embedding vectors in the latent space to see how they are located.
This file helps visualizing the ability of the feature extraction of the model,
Yet it's not a good measure since we're using a different model to decrease the dimensionality from 128 to 2

This one was designed for embeddings extracted from Tok_dict input.
"""

import numpy as np
from sklearn.manifold import TSNE
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


directory = "./embeddings_dir/"

all_embeddings = []     # a list of tuples (key_id , embedding_vector, class_name)
latent_space = np.zeros((1, 128))
class_list = []
latent_dictionary = dict()

for filename in os.listdir(directory):
    if filename.endswith("glitch_full_tok_dict_embeddings.npz"):
        file_name = filename
        tok_dict = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        for embeddings in tok_dict["embeddings"]:
            embed_vector = embeddings[0]
            key_id = embeddings[1]
            class_name_raw = embeddings[2]
            class_name = class_name_raw.split(str(key_id))[0]
            latent_space = np.concatenate((latent_space, embed_vector))
            class_list.append(class_name)


latent_space = latent_space[1:, :]

# Now the latent space variable has NxD data in it. N: number of sketches. D: dimensions. D=128 in this case
latent_space_tsne = TSNE(n_components=2).fit_transform(latent_space)


for i in range(len(class_list)):
    label = class_list[i]
    x_float = (latent_space_tsne[i, :])[0]
    y_float = (latent_space_tsne[i, :])[1]
    if label not in latent_dictionary.keys():
        latent_dictionary[label] = [[x_float], [y_float]]
    else:
        old_value_list = latent_dictionary[label]
        old_value_list[0].append(x_float)
        old_value_list[1].append(y_float)
        latent_dictionary[label] = old_value_list

class_keys = latent_dictionary.keys()

legend_list = list()
scatter_input = tuple()   # (plt.scatter(np.zeros((1, 2)), np.zeros((1, 2))),)
recur = 0

# hard_categs = ["drug", "hole", "board", "insect", "molecules", "seed", "stone", "valley", "snowboard", "creditcard"]

for categ_names in class_keys:
    #recur += 1
    #if recur < 11:
        #continue
    #elif recur < 21:
    x_y_list = latent_dictionary[categ_names]
    x_array = np.array(x_y_list[0])
    y_array = np.array(x_y_list[1])
    legend_list.append(categ_names)
    scatter_input += (plt.scatter(x_array, y_array),)

legend_tuple = tuple(legend_list)

fontP = FontProperties()
fontP.set_size('x-small')
plt.legend(scatter_input,
           legend_tuple,
           scatterpoints=1,
           bbox_to_anchor=(1.05, 1),
           loc='upper left',
           prop=fontP,
           ncol=2)


plt.tight_layout()

plt.show()





