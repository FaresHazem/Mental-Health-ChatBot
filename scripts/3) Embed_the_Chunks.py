import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load data
df = pd.read_csv("data\cleaned_chunked_data.csv")
texts = df['text_chunk'].tolist()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed all chunks
embeddings = model.encode(texts, show_progress_bar=True)

# Save embeddings and metadata
np.save("Embeddings\embeddings.npy", embeddings)
df.to_csv("data\chunk_metadata.csv", index=False)

print(f"✅ Saved {len(embeddings)} embeddings to 'embeddings.npy'")
print("✅ Metadata saved to 'chunk_metadata.csv'")
