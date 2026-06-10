"""Milestone 3 — chunking + inspection.

Loads the cleaned documents, applies the chunking strategy (chunk_text), attaches
source metadata to every chunk for later attribution, writes documents/chunks.jsonl,
then prints the total count, token-length stats, and 5 random chunks to inspect.

Run:  .venv/bin/python -m src.build_chunks
"""

import json
import random
from pathlib import Path

from transformers import AutoTokenizer

from src.chunker import chunk_text

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "documents" / "manifest.json"
CHUNKS_OUT = ROOT / "documents" / "chunks.jsonl"

MAX_TOKENS = 200       # fallback cap, safely under all-MiniLM-L6-v2's 256-token limit
OVERLAP_TOKENS = 25
MODEL_LIMIT = 256

_tok = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def count_tokens(text):
    return len(_tok.encode(text, add_special_tokens=False))


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    chunks = []

    for doc in manifest:
        text = (ROOT / doc["clean_path"]).read_text(encoding="utf-8")
        # Blogs are long-form prose -> pack small paragraphs/headings together.
        # Reviews/guides/index are discrete units -> keep one chunk per unit.
        pack = doc["kind"] == "blog"
        pieces = chunk_text(text, count_tokens=count_tokens,
                            max_tokens=MAX_TOKENS, overlap_tokens=OVERLAP_TOKENS, pack=pack)
        for i, piece in enumerate(pieces):
            chunks.append({
                "chunk_id": f"{doc['id']}__{i}",
                "source_id": doc["id"],
                "source_name": doc["name"],
                "url": doc["url"],
                "kind": doc["kind"],
                "text": piece,
                "n_tokens": count_tokens(piece),
            })

    with CHUNKS_OUT.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # ---- inspection ----
    tok_counts = [c["n_tokens"] for c in chunks]
    empties = [c for c in chunks if not c["text"].strip()]
    over_limit = [c for c in chunks if c["n_tokens"] > MODEL_LIMIT]

    print(f"Total chunks: {len(chunks)}  (from {len(manifest)} documents)")
    print(f"Tokens/chunk: min={min(tok_counts)} max={max(tok_counts)} "
          f"avg={sum(tok_counts)/len(tok_counts):.1f}")
    print(f"Empty chunks: {len(empties)}   Chunks over model limit ({MODEL_LIMIT}): {len(over_limit)}")
    print("\nChunks per document:")
    per_doc = {}
    for c in chunks:
        per_doc[c["source_id"]] = per_doc.get(c["source_id"], 0) + 1
    for doc in manifest:
        print(f"  {per_doc.get(doc['id'], 0):>3}  {doc['id']}")

    print("\n" + "=" * 70)
    print("5 RANDOM CHUNKS (inspect: readable? substantive? self-contained?)")
    print("=" * 70)
    rng = random.Random(42)  # fixed seed -> reproducible inspection
    for c in rng.sample(chunks, 5):
        print(f"\n[{c['chunk_id']}]  ({c['n_tokens']} tokens)  source: {c['source_name']}")
        print(c["text"])
        print("-" * 70)


if __name__ == "__main__":
    main()
