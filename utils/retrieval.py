import numpy as np
def query_topic(topic, index, chunks, client, threshold=0.6):
    k = k=min(10, len(chunks))
    # Get the embedding for the query topic
    query_vec = client.embeddings.create(input=topic, model="text-embedding-3-small")
    qvec = np.array(query_vec.data[0].embedding, dtype=np.float32).reshape(1, -1)

    # Perform vector search
    distances, indices = index.search(qvec, k)

    # Ensure indices don't exceed chunk bounds and are within distance threshold
    top_chunks = []
    for i, dist in zip(indices[0], distances[0]):
        if 0 <= i < len(chunks) and dist < threshold:
            top_chunks.append(chunks[i])

    return top_chunks
