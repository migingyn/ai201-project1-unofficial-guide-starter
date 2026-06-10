"""Tests for the grounding orchestration in src.generate.ask().

The LLM and the retriever are injected so we can test the grounding guarantees
(relevance gating, declining on no-context, programmatic source attribution)
without calling Groq or building an index.
"""

from src.generate import ask, NO_INFO


def make_hit(name, dist, url="https://example.com/x", text="some text"):
    return {"rank": 1, "distance": dist, "text": text,
            "source_name": name, "url": url, "source_id": name}


def test_declines_when_all_chunks_above_threshold():
    calls = []
    hits = [make_hit("A", 0.8), make_hit("B", 0.9)]
    result = ask("anything", max_distance=0.6,
                 search_fn=lambda q, k: hits,
                 llm_fn=lambda q, chunks: calls.append(1) or "should not run")
    assert result["answer"] == NO_INFO
    assert result["sources"] == []
    assert calls == [], "LLM must not be called when there is no relevant context"


def test_passes_only_relevant_chunks_to_llm():
    seen = {}
    hits = [make_hit("Close", 0.30), make_hit("Far", 0.70)]

    def fake_llm(q, chunks):
        seen["names"] = [c["source_name"] for c in chunks]
        return "answer"

    ask("q", max_distance=0.6, search_fn=lambda q, k: hits, llm_fn=fake_llm)
    assert seen["names"] == ["Close"]


def test_sources_are_deduped_from_relevant_chunks():
    hits = [make_hit("Costa Verde", 0.30, url="u1"),
            make_hit("Costa Verde", 0.31, url="u1"),
            make_hit("Regents", 0.32, url="u2")]
    result = ask("q", max_distance=0.6, search_fn=lambda q, k: hits,
                 llm_fn=lambda q, chunks: "answer")
    names = [s["name"] for s in result["sources"]]
    assert names == ["Costa Verde", "Regents"]


def test_returns_llm_answer_when_grounded():
    hits = [make_hit("A", 0.20)]
    result = ask("q", search_fn=lambda q, k: hits,
                 llm_fn=lambda q, chunks: "grounded answer from context")
    assert result["answer"] == "grounded answer from context"
    assert result["sources"] == [{"name": "A", "url": "https://example.com/x"}]


def test_clears_sources_when_llm_declines_despite_context():
    # Chunks were close enough to pass the gate, but the LLM judged them
    # insufficient and returned the decline string -> don't cite sources.
    hits = [make_hit("A", 0.30), make_hit("B", 0.40)]
    result = ask("q", search_fn=lambda q, k: hits,
                 llm_fn=lambda q, chunks: NO_INFO)
    assert result["answer"] == NO_INFO
    assert result["sources"] == []
    assert result["grounded"] is False
