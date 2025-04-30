import os
import sys
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from google.genai import Client
from google.genai.types import GenerateContentConfig

# —— CONFIGURATION —— #
FAISS_INDEX_PATH     = "models/mental_health_index.faiss"
METADATA_CSV_PATH    = "data/cleaned_chunk_metadata.csv"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_API_KEY       = "AIzaSyCMYuQQp4G6MQ6taw2xGpfHtVgtH5AEp1A"
GEMINI_MODEL_NAME    = "gemini-2.0-flash"
TOP_K                = 5

# —— INITIALIZATION —— #
# 1. Load FAISS index
if not os.path.exists(FAISS_INDEX_PATH):
    print(f"ERROR: FAISS index not found at {FAISS_INDEX_PATH}", file=sys.stderr)
    sys.exit(1)
index = faiss.read_index(FAISS_INDEX_PATH)

# 2. Load metadata
if not os.path.exists(METADATA_CSV_PATH):
    print(f"ERROR: Metadata CSV not found at {METADATA_CSV_PATH}", file=sys.stderr)
    sys.exit(1)
df_meta = pd.read_csv(METADATA_CSV_PATH, dtype=str)
# Ensure the text column is correctly identified
text_column = "text_chunk"
if text_column not in df_meta.columns:
    print(f"ERROR: Expected column '{text_column}' not in metadata CSV", file=sys.stderr)
    print("Available columns:", df_meta.columns.tolist(), file=sys.stderr)
    sys.exit(1)
metadata_texts = df_meta[text_column].tolist()

# 3. Initialize embedder
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

# 4. Initialize Gemini client
client = Client(api_key=GEMINI_API_KEY)

# —— HELPERS —— #

def check_dimensions():
    """Verify that the FAISS index and embedding model agree on vector size."""
    expected_dim = index.d
    sample_vec = embedder.encode(["test"])
    actual_dim = sample_vec.shape[1]
    print(f"[DEBUG] FAISS index dimension: {expected_dim}; Embedder output dimension: {actual_dim}")
    if expected_dim != actual_dim:
        raise ValueError(f"Dimension mismatch: index expects {expected_dim}, but embedder gives {actual_dim}")

def retrieve_relevant_chunks(query: str, top_k: int = TOP_K):
    """Embed the query and return the top_k most relevant text chunks."""
    try:
        q_emb = embedder.encode([query])
    except Exception as e:
        print(f"[ERROR] Embedding failed for query '{query}': {e}", file=sys.stderr)
        return []

    distances, indices = index.search(q_emb, top_k)
    print(f"[DEBUG] Retrieved indices: {indices[0]}, distances: {distances[0]}")
    chunks = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(metadata_texts):
            print(f"[WARNING] Index {idx} out of metadata range", file=sys.stderr)
            continue
        chunks.append(metadata_texts[idx])
    return chunks

def generate_response(question: str, context: str) -> str:
    """Call Gemini API, passing in the question and retrieved context."""
    prompt = f"Question: {question}\nContext:\n{context}\nAnswer:"
    print(f"[DEBUG] Sending prompt to Gemini:\n{prompt}\n")

    try:
        resp = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=[prompt],
            config=GenerateContentConfig(response_modalities=["Text"])
        )
    except Exception as e:
        return f"ERROR: API call failed: {e}"

    # Debug-print entire response object
    print(f"[DEBUG] Raw Gemini response:\n{resp}\n")

    # Attempt to extract generated text
    text = None
    if hasattr(resp, "generated_content") and resp.generated_content:
        text = resp.generated_content[0].text
    elif hasattr(resp, "generations") and resp.generations:
        text = resp.generations[0].text
    elif hasattr(resp, "candidates") and resp.candidates:
        # Newer response format: candidates list
        candidate = resp.candidates[0]
        if hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
            text = candidate.content.parts[0].text
    
    if not text:
        return "⚠️ Could not parse Gemini response format."
    return text.strip()

def chat_loop():
    """Main REPL for the RAG chatbot."""
    check_dimensions()
    print("Welcome to your RAG-powered chatbot! (type 'exit' to quit)")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break

        chunks = retrieve_relevant_chunks(question)
        if not chunks:
            print("Bot: ❗️ I couldn't find relevant context to answer that.")
            continue

        context = "\n\n".join(chunks)
        answer = generate_response(question, context)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    chat_loop()
