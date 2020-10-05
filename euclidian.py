import numpy as np
from scipy.spatial import distance


filename = "./embeddings_dir/embedding.npz"
embeddings = np.load(filename, allow_pickle=True, encoding="latin1")
embeddings = embeddings["embeddings"]


embedding_one = (1, 2, 3)
embedding_two = (4, 5, 6)
dst = distance.euclidean(embedding_one, embedding_two)