"""
rag_engine.py – Vector DB + Embedding + Retrieval
"""

import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from .file_reader import load_file

CHUNK_SIZE = 400

BASE_DIR = os.path.dirname(__file__)
VEC_PATH = os.path.join(BASE_DIR, "vector_store.faiss")
META_PATH = os.path.join(BASE_DIR, "metadata.json")

model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------
# Chunking
# ------------------------------

def chunk_text(text):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= CHUNK_SIZE:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


# ------------------------------
# Load / Save metadata
# ------------------------------

def load_metadata():
    if not os.path.exists(META_PATH):
        return []
    with open(META_PATH, "r") as f:
        return json.load(f)

def save_metadata(data):
    with open(META_PATH, "w") as f:
        json.dump(data, f, indent=2)


# ------------------------------
# Vector store ops
# ------------------------------

def initialize_vector_store(dim=384):
    if os.path.exists(VEC_PATH):
        index = faiss.read_index(VEC_PATH)
    else:
        index = faiss.IndexFlatL2(dim)
    return index

index = initialize_vector_store()

# ------------------------------
# Ingest a file
# ------------------------------

def ingest_file(path, tag):
    print("Reading:", path)
    text = load_file(path)
    chunks = chunk_text(text)

    print("Embedding", len(chunks), "chunks...")
    emb = model.encode(chunks)

    global index
    index.add(emb)

    # Save vector store
    faiss.write_index(index, VEC_PATH)

    # Save metadata
    meta = load_metadata()
    for i, c in enumerate(chunks):
        meta.append({"tag": tag, "chunk": c})
    save_metadata(meta)

    return True


# ------------------------------
# Search query
# ------------------------------

def search(query, top_k=5):
    emb = model.encode([query])
    D, I = index.search(emb, top_k)

    meta = load_metadata()
    results = []

    for idx in I[0]:
        if idx < len(meta):
            results.append(meta[idx]["chunk"])

    return results
