
# This python file creates the text files for the input of tSNE.py


import numpy as np
from scipy.spatial import distance
import os
import pickle


directory = "./embeddings_dir/"

all_embeddings = []
all_labels = []
f = open('text_embeddings_file.txt', 'w')
g = open('text_labels_file.txt', 'w')
f.close()
g.close()
f = open('text_embeddings_file.txt', 'a')
g = open('text_labels_file.txt', 'a')

for filename in os.listdir(directory):
    if filename.endswith(".npz"):
        file_name = filename
        embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        embedding = embeddings["embeddings"]
        key_id = int(embeddings["key_id"])
        np.savetxt(f, embedding)
        g.write('%d' % key_id +"\n")
"""
        all_embeddings.append(embedding)
        all_labels.append(key_id)

f = open('text_embeddings_file.txt', 'w')
f.write(str(all_embeddings))

f = open('text_labels_file.txt', 'w')
f.write(str(all_labels))
"""