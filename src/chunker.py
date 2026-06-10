"""Chunking strategy (see planning.md > Chunking Strategy).

Primary unit = one complete review / paragraph, found by splitting on blank-line
boundaries. A unit at or under ``max_tokens`` is kept whole and carries no overlap
with its neighbours (reviews are self-contained). Only a unit that exceeds the cap
is split into sub-chunks, and only those fallback splits carry overlap so a figure
or qualifier isn't stranded from its context across the cut.

``count_tokens`` is injected so the chunker can be unit-tested with a trivial word
counter, while production passes the real ``all-MiniLM-L6-v2`` tokenizer.
"""

import re

# Blank line (optionally with stray whitespace) separates units.
_UNIT_BOUNDARY = re.compile(r"\n\s*\n")


def chunk_text(text, *, count_tokens, max_tokens=200, overlap_tokens=25, pack=False):
    """Split ``text`` into a list of non-empty chunk strings.

    pack=False (reviews/guides): one chunk per unit; oversized units fall back-split.
    pack=True (long-form prose): greedily merge consecutive units up to the token cap
    so headings/bylines bind to their surrounding text instead of becoming fragments.
    """
    units = [u.strip() for u in _UNIT_BOUNDARY.split(text)]
    units = [u for u in units if u]

    if pack:
        return _pack_units(units, count_tokens, max_tokens, overlap_tokens)

    chunks = []
    for unit in units:
        if count_tokens(unit) <= max_tokens:
            chunks.append(unit)
        else:
            chunks.extend(_split_oversized(unit, count_tokens, max_tokens, overlap_tokens))
    return chunks


def _pack_units(units, count_tokens, max_tokens, overlap_tokens):
    """Greedily combine consecutive units into chunks of at most max_tokens."""
    chunks = []
    buf = []
    for unit in units:
        if count_tokens(unit) > max_tokens:
            if buf:
                chunks.append("\n\n".join(buf))
                buf = []
            chunks.extend(_split_oversized(unit, count_tokens, max_tokens, overlap_tokens))
            continue
        if buf and count_tokens("\n\n".join(buf + [unit])) > max_tokens:
            chunks.append("\n\n".join(buf))
            buf = [unit]
        else:
            buf.append(unit)
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


def _split_oversized(unit, count_tokens, max_tokens, overlap_tokens):
    """Greedily pack words into sub-chunks <= max_tokens, with word-level overlap."""
    words = unit.split()
    n = len(words)
    chunks = []
    i = 0
    while i < n:
        j = i
        while j < n:
            candidate = " ".join(words[i:j + 1])
            if j > i and count_tokens(candidate) > max_tokens:
                break
            j += 1
        chunks.append(" ".join(words[i:j]))
        if j >= n:
            break
        # Step the window back by ~overlap_tokens words so consecutive splits overlap,
        # but always make forward progress.
        i = max(i + 1, j - overlap_tokens) if overlap_tokens > 0 else j
    return chunks
