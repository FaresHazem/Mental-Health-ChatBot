import os
import sys
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from google.genai import Client
from google.genai.types import GenerateContentConfig
from google.genai.errors import ServerError
import streamlit as st

# —— STREAMLIT PAGE CONFIG —— #
st.set_page_config(page_title="🧠 Mental Health Chatbot", layout="centered")

# —— CONFIGURATION —— #
FAISS_INDEX_PATH     = "models/mental_health_index.faiss"
METADATA_CSV_PATH    = "data/cleaned_chunk_metadata.csv"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GEMINI_API_KEY       = "AIzaSyCMYuQQp4G6MQ6taw2xGpfHtVgtH5AEp1A"
GEMINI_MODEL_NAME    = "gemini-2.0-flash"
TOP_K                = 5

# —— CACHING INITIALIZATION —— #
@st.cache_resource
def load_faiss_index(path):
    if not os.path.exists(path):
        st.error(f"FAISS index not found at {path}")
        st.stop()
    return faiss.read_index(path)

@st.cache_data
def load_metadata(path, text_col="text_chunk"):
    if not os.path.exists(path):
        st.error(f"Metadata CSV not found at {path}")
        st.stop()
    df = pd.read_csv(path, dtype=str)
    if text_col not in df.columns:
        st.error(f"Expected column '{text_col}' not in metadata CSV. Available: {df.columns.tolist()}")
        st.stop()
    return df[text_col].tolist()

@st.cache_resource
def init_embedder(model_name):
    return SentenceTransformer(model_name)

@st.cache_resource
def init_client(api_key):
    return Client(api_key=api_key)

# Load resources
index = load_faiss_index(FAISS_INDEX_PATH)
metadata_texts = load_metadata(METADATA_CSV_PATH)
embedder = init_embedder(EMBEDDING_MODEL_NAME)
client = init_client(GEMINI_API_KEY)

# —— HELPERS —— #

def check_dimensions():
    expected = index.d
    actual = embedder.encode(["test"]).shape[1]
    if expected != actual:
        st.error(f"Dimension mismatch: index expects {expected}, embedder gives {actual}")
        st.stop()

@st.cache_data
def retrieve_relevant_chunks(query: str, top_k: int = TOP_K):
    q_emb = embedder.encode([query])
    distances, indices = index.search(q_emb, top_k)
    return [metadata_texts[idx] for idx in indices[0] if 0 <= idx < len(metadata_texts)]

@st.cache_data
def generate_response(question: str, context: str) -> str:
    prompt = f"Question: {question}\nContext:\n{context}\nAnswer:"
    try:
        resp = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=[prompt],
            config=GenerateContentConfig(response_modalities=["Text"])
        )
    except ServerError:
        return "⚠️ The generation service is currently overloaded. Please try again in a moment."
    except Exception as e:
        return f"⚠️ Error calling generation service: {e}"
    # Extract text
    if hasattr(resp, "generated_content") and resp.generated_content:
        return resp.generated_content[0].text.strip()
    if hasattr(resp, "generations") and resp.generations:
        return resp.generations[0].text.strip()
    if hasattr(resp, "candidates") and resp.candidates:
        cand = resp.candidates[0]
        if cand.content and cand.content.parts:
            return cand.content.parts[0].text.strip()
    return "⚠️ Could not parse response."

# —— STREAMLIT CHAT UI —— #
check_dimensions()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Mental Health Chatbot")
st.subheader("💬 Ask anything about mental health and get insightful answers!")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg['content'])
    else:
        # Display error messages differently
        if msg.get("content", "").startswith("⚠️"):
            st.chat_message("assistant").write(f"❗ {msg['content']}")  # could use st.error
        else:
            st.chat_message("assistant").write(msg['content'])

# Input
if prompt := st.chat_input("💡 Type your question here..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Retrieve context and generate
    chunks = retrieve_relevant_chunks(prompt)
    context = "\n\n".join(chunks)

    # Call generation
    response = generate_response(prompt, context)

    # Store and display
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
