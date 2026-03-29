import numpy as np
from numpy.linalg import norm

vocab = {
    "yash": 0,
    "coding": 1,
    "gym": 2
}

# random embeddings (3 words, 4D vector)
embedding_matrix = np.random.rand(3, 4)

def get_embedding(word):
    idx = vocab[word]
    return embedding_matrix[idx]


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

print(cosine_similarity(get_embedding("yash"), get_embedding("coding")))


# print(get_embedding("yash"))