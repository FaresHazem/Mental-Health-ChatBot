import faiss
import numpy as np
import pandas as pd

# Load embeddings and metadata
embeddings = np.load("Embeddings\embeddings.npy")
df = pd.read_csv("data/chunk_metadata.csv")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save the index
faiss.write_index(index, "models/mental_health_index.faiss")
df.to_csv("data/chunk_metadata.csv", index=False)

print(f"✅ FAISS index built with {index.ntotal} vectors and saved as 'models/mental_health_index.faiss'")
