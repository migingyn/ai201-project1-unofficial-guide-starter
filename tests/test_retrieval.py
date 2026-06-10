"""Integration test for embedding + retrieval (Milestone 4).

Builds a tiny in-memory ChromaDB collection from a few chunks and checks that a
semantic query returns the right source with a low cosine distance. Uses the real
all-MiniLM-L6-v2 model (loaded once, cached) and an EphemeralClient so the
persistent chroma_db/ index is untouched.
"""

import chromadb

from src.vectorstore import build_collection, search

CHUNKS = [
    {"chunk_id": "cv__0", "source_id": "costa", "source_name": "Costa Verde Village",
     "url": "https://example.com/costa", "kind": "review", "n_tokens": 12,
     "text": "Costa Verde Village: there are always roaches coming from the drains, "
             "and there is never any parking available."},
    {"chunk_id": "reg__0", "source_id": "regents", "source_name": "Regents La Jolla",
     "url": "https://example.com/regents", "kind": "review", "n_tokens": 12,
     "text": "Regents La Jolla is only a 10 minute bike to UCSD, gated and secure, "
             "but the units can get crowded with several roommates."},
    {"chunk_id": "mm__0", "source_id": "mira", "source_name": "Mira Mesa guide",
     "url": "https://example.com/mira", "kind": "guide", "n_tokens": 10,
     "text": "Median rents in Mira Mesa: Studio $1400, 1 Bedroom $1800, 2 Bedroom $2000."},
]


def _collection():
    return build_collection(chromadb.EphemeralClient(), CHUNKS)


def test_retrieval_returns_relevant_source_with_low_distance():
    col = _collection()
    res = search("pest and roach problems at Costa Verde", k=1, collection=col)
    assert res[0]["source_name"] == "Costa Verde Village"
    assert res[0]["distance"] < 0.5


def test_retrieval_attaches_source_metadata():
    col = _collection()
    res = search("how much is rent in Mira Mesa", k=1, collection=col)
    assert res[0]["source_name"] == "Mira Mesa guide"
    assert res[0]["url"] == "https://example.com/mira"


def test_search_respects_k():
    col = _collection()
    assert len(search("apartments near UCSD", k=2, collection=col)) == 2
