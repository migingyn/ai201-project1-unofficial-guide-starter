"""Milestone 4 verification — run the 5 planning.md evaluation questions through
retrieval (no generation yet) and print the top-k chunks + cosine distances so we
can eyeball whether retrieval is on-topic before wiring in the LLM.

Run:  .venv/bin/python -m src.eval_retrieval
"""

from src.vectorstore import search

QUESTIONS = [
    "What do residents complain about most at Costa Verde Village?",
    "How does median 1-bedroom rent in University City compare to Mira Mesa?",
    "How crowded do students say Regents La Jolla units get?",
    "According to the guides, which neighborhood is the budget option for UCSD students, and what commute tradeoff do they cite?",
    "What downsides do reviewers report about La Regencia despite its low rent?",
]

K = 5
PREVIEW = 220


def main():
    for i, q in enumerate(QUESTIONS, start=1):
        print("=" * 80)
        print(f"Q{i}: {q}")
        print("=" * 80)
        for r in search(q, k=K):
            flag = "  <-- weak (>0.5)" if r["distance"] > 0.5 else ""
            text = " ".join(r["text"].split())
            print(f"  [{r['distance']:.3f}] {r['source_name']}{flag}")
            print(f"          {text[:PREVIEW]}{'…' if len(text) > PREVIEW else ''}")
        print()


if __name__ == "__main__":
    main()
