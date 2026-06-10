"""Tests for the chunking strategy described in planning.md:

- Primary unit = one complete review / paragraph (split on blank-line boundaries).
- Whole units under the token cap are kept intact, with NO overlap between them
  (they are self-contained).
- A unit larger than the cap is split into sub-chunks <= cap, and only those
  fallback splits carry overlap.
- Empty / whitespace-only units are filtered out.
"""

from src.chunker import chunk_text

# A simple, deterministic token counter for tests: 1 token per whitespace word.
# Lets us trigger the fallback split with small, readable inputs.
words = lambda s: len(s.split())


def test_single_short_unit_returned_whole():
    text = "Parking here is a nightmare and the walls are paper thin."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=2)
    assert chunks == ["Parking here is a nightmare and the walls are paper thin."]


def test_two_units_split_on_blank_line_kept_separate():
    text = "Review one about roaches.\n\nReview two about noise."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=2)
    assert chunks == ["Review one about roaches.", "Review two about noise."]


def test_whitespace_only_input_yields_no_chunks():
    assert chunk_text("   \n\n  \t ", count_tokens=words, max_tokens=50, overlap_tokens=2) == []


def test_empty_units_between_blank_lines_are_filtered():
    text = "Real review text here.\n\n\n\n   \n\nAnother real review."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=2)
    assert chunks == ["Real review text here.", "Another real review."]


def test_separate_units_under_cap_have_no_overlap():
    text = "Alpha bravo charlie.\n\nDelta echo foxtrot."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=2)
    # No word from unit 1 should leak into unit 2's chunk (self-contained, no overlap).
    assert "alpha" not in chunks[1].lower()
    assert "foxtrot" not in chunks[0].lower()


def test_oversized_unit_is_split_under_cap():
    # 12 words, cap of 5 -> must split into multiple chunks, each <= 5 tokens.
    text = "one two three four five six seven eight nine ten eleven twelve"
    chunks = chunk_text(text, count_tokens=words, max_tokens=5, overlap_tokens=0)
    assert len(chunks) >= 3
    assert all(words(c) <= 5 for c in chunks)
    # No content lost: every original word appears somewhere.
    joined = " ".join(chunks).split()
    for w in text.split():
        assert w in joined


def test_fallback_splits_carry_overlap():
    text = "one two three four five six seven eight nine ten"
    chunks = chunk_text(text, count_tokens=words, max_tokens=5, overlap_tokens=2)
    # Consecutive fallback chunks should share at least one word (overlap).
    first_words = set(chunks[0].split())
    second_words = set(chunks[1].split())
    assert first_words & second_words, "expected overlap between fallback splits"


def test_reconstructs_all_units():
    text = "first review.\n\nsecond review.\n\nthird review."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=2)
    assert len(chunks) == 3


# --- pack=True mode: greedily merge small consecutive units (for long-form prose) ---

def test_pack_merges_small_units_up_to_cap():
    # Three units of 2 words each, cap of 4 -> first two merge, third starts a new chunk.
    text = "alpha beta\n\ngamma delta\n\nepsilon zeta"
    chunks = chunk_text(text, count_tokens=words, max_tokens=4, overlap_tokens=0, pack=True)
    assert chunks == ["alpha beta\n\ngamma delta", "epsilon zeta"]


def test_pack_binds_heading_to_following_paragraph():
    # A tiny heading should not survive as its own chunk under packing.
    text = "TL;DR\n\nThis is the actual answer paragraph with real content."
    chunks = chunk_text(text, count_tokens=words, max_tokens=50, overlap_tokens=0, pack=True)
    assert len(chunks) == 1
    assert chunks[0].startswith("TL;DR")


def test_pack_still_splits_oversized_single_unit():
    text = "one two three four five six seven"
    chunks = chunk_text(text, count_tokens=words, max_tokens=3, overlap_tokens=0, pack=True)
    assert all(words(c) <= 3 for c in chunks)
    assert len(chunks) >= 3
