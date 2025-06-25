import faiss
import numpy as np

def embed_chunks_openai(chunks, client):
    vectors = []
    for chunk in chunks:
        resp = client.embeddings.create(input=chunk, model="text-embedding-3-small")
        vectors.append(resp.data[0].embedding)
    return np.array(vectors, dtype=np.float32)

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index
