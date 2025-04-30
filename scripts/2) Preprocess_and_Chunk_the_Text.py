import pandas as pd
import re
import math

# Load your scraped dataset
df = pd.read_csv("data\mental_health_data.csv")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    text = re.sub(r'\n+', ' ', text)  # Remove newlines
    return text.strip()

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Process each row
chunks = []
for idx, row in df.iterrows():
    cleaned = clean_text(row['text'])
    chunked = chunk_text(cleaned, chunk_size=300)
    for chunk in chunked:
        chunks.append((row['source_url'], chunk))

# Save chunked data
chunked_df = pd.DataFrame(chunks, columns=['source_url', 'text_chunk'])
chunked_df.to_csv("data\cleaned_chunked_data.csv", index=False)

print(f"✅ Saved {len(chunks)} chunks to 'cleaned_chunked_data.csv'")
