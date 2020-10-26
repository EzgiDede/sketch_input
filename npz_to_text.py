
# This python file creates numpy text files.


import numpy as np
from scipy.spatial import distance
import os
import pickle


directory = "./embeddings_dir/"

all_embeddings = []
all_labels = []
f = open('some.txt', 'w')
g = open('some_other.txt', 'w')
f.close()
g.close()
f = open('some.txt', 'a')
g = open('some_other.txt', 'a')

for filename in os.listdir(directory):
    if filename.endswith(".npz"):
        file_name = filename
        embeddings = np.load(directory + file_name, allow_pickle=True, encoding="latin1")
        embedding = embeddings["embeddings"]
        key_id = int(embeddings["key_id"])
        np.savetxt(f, embedding)
        g.write('%d' % key_id +"\n")
