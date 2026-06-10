"""Milestone 5 — grounded answer generation.

ask() retrieves the top-k chunks, drops any that aren't relevant enough (cosine
distance gate), and asks Groq's llama-3.3-70b-versatile to answer using ONLY that
context. Grounding is enforced two ways:

1. Relevance gate: if no retrieved chunk is close enough, we return the "not enough
   information" answer WITHOUT calling the LLM, so out-of-corpus questions can't be
   answered from the model's training knowledge.
2. Strict system prompt: the model is told to answer only from the numbered context
   and to say it lacks information otherwise.

Source attribution is programmatic — result["sources"] is built from the metadata of
the chunks actually passed to the model, not from whatever the LLM chooses to cite.
"""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from src.vectorstore import search

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

MODEL = "llama-3.3-70b-versatile"
NO_INFO = "I don't have enough information on that."
MAX_DISTANCE = 0.6   # cosine distance above this = not relevant enough to ground on

SYSTEM_PROMPT = (
    "You are the Unofficial Guide to UCSD off-campus housing. "
    "Answer the user's question using ONLY the information in the numbered context "
    "documents provided in the user message. Do not use any outside or prior knowledge. "
    "Do not guess or generalize beyond what the context states. "
    f"If the context does not contain enough information to answer, reply with exactly: "
    f"\"{NO_INFO}\" and nothing else. "
    "When you do answer, be concise and mention which complex or neighborhood the "
    "information is about."
)


@lru_cache(maxsize=1)
def _client():
    from groq import Groq
    key = os.getenv("GROQ_API_KEY")
    if not key or key == "your_key_here":
        raise RuntimeError("GROQ_API_KEY is not set in .env")
    return Groq(api_key=key)


def _format_context(chunks):
    blocks = []
    for i, c in enumerate(chunks, start=1):
        blocks.append(f"[{i}] (source: {c['source_name']})\n{c['text']}")
    return "\n\n".join(blocks)


def _groq_answer(question, chunks):
    user_msg = (
        f"Context documents:\n\n{_format_context(chunks)}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )
    resp = _client().chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    return resp.choices[0].message.content.strip()


def ask(question, *, k=5, max_distance=MAX_DISTANCE, search_fn=search, llm_fn=None):
    """Return {answer, sources, hits, grounded} for a question."""
    hits = search_fn(question, k)
    relevant = [h for h in hits if h["distance"] <= max_distance]

    if not relevant:
        return {"answer": NO_INFO, "sources": [], "hits": [], "grounded": False}

    answer = (llm_fn or _groq_answer)(question, relevant)

    # The model may judge the (gated-in) context still insufficient and decline.
    # Don't cite sources for a non-answer.
    if answer.strip().rstrip(".").lower() == NO_INFO.rstrip(".").lower():
        return {"answer": NO_INFO, "sources": [], "hits": [], "grounded": False}

    sources, seen = [], set()
    for h in relevant:
        key = (h["source_name"], h["url"])
        if key not in seen:
            seen.add(key)
            sources.append({"name": h["source_name"], "url": h["url"]})

    return {"answer": answer, "sources": sources, "hits": relevant, "grounded": True}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "What do residents complain about at Costa Verde Village?"
    result = ask(q)
    print(f"Q: {q}\n")
    print(result["answer"], "\n")
    if result["sources"]:
        print("Sources:")
        for s in result["sources"]:
            print(f"  • {s['name']} — {s['url']}")
