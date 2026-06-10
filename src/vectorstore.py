"""Milestone 4 — embedding + vector store + retrieval.

Embeds the chunks from documents/chunks.jsonl with all-MiniLM-L6-v2 and stores them
in a persistent ChromaDB collection together with source metadata (used later for
attribution). Provides a top-k semantic ``search`` over that collection.

ChromaDB notes:
- PersistentClient writes the index to disk (``chroma_db/``) so we embed once.
- The collection is created with ``hnsw:space = cosine`` so query distances are
  cosine distances in [0, 2]; ~0 means near-identical, lower is better.
- We compute embeddings ourselves with sentence-transformers (normalized) and hand
  them to Chroma, rather than letting Chroma pick a model, so the embedding model
  stays exactly the one named in planning.md.

Build the index:  .venv/bin/python -m src.vectorstore
"""

import json
from functools import lru_cache
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_PATH = ROOT / "documents" / "chunks.jsonl"
PERSIST_DIR = ROOT / "chroma_db"
COLLECTION = "ucsd_housing"
MODEL_NAME = "all-MiniLM-L6-v2"

_META_KEYS = ("source_id", "source_name", "url", "kind", "n_tokens")


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def load_chunks(path=CHUNKS_PATH):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def embed(texts, model=None):
    model = model or get_model()
    return model.encode(list(texts), normalize_embeddings=True,
                        show_progress_bar=False).tolist()


def build_collection(client, chunks, model=None):
    """(Re)create the collection and add all chunks. Returns the collection."""
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embed([c["text"] for c in chunks], model),
        documents=[c["text"] for c in chunks],
        metadatas=[{k: c[k] for k in _META_KEYS} for c in chunks],
    )
    return collection


def search(query, k=5, *, collection=None, model=None):
    """Return the top-k chunks for ``query`` as a list of result dicts."""
    model = model or get_model()
    collection = collection or get_persistent_collection()
    res = collection.query(
        query_embeddings=embed([query], model),
        n_results=k,
    )
    out = []
    for rank, (doc, meta, dist) in enumerate(
        zip(res["documents"][0], res["metadatas"][0], res["distances"][0]), start=1
    ):
        out.append({
            "rank": rank,
            "distance": dist,
            "text": doc,
            "source_name": meta["source_name"],
            "url": meta["url"],
            "source_id": meta["source_id"],
        })
    return out


def get_persistent_collection():
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    return client.get_collection(COLLECTION)


def main():
    chunks = load_chunks()
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    collection = build_collection(client, chunks)
    print(f"Embedded {collection.count()} chunks with {MODEL_NAME} "
          f"into ChromaDB collection '{COLLECTION}' at {PERSIST_DIR}")


if __name__ == "__main__":
    main()
