"""Milestone 3 — document ingestion.

Fetches each source URL, archives the raw HTML, then cleans it down to substantive
text (reviews / guide content) with site nav, amenity checklists, ads, and footers
removed. Cleaned text is written one file per source to documents/clean/, and a
manifest.json records the source metadata used later for chunk attribution.

Run:  .venv/bin/python -m src.ingest
"""

import json
import re
import time
from pathlib import Path

import requests
import trafilatura
from bs4 import BeautifulSoup

from src.sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "documents" / "raw_html"
CLEAN_DIR = ROOT / "documents" / "clean"
MANIFEST = ROOT / "documents" / "manifest.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AI201-UnofficialGuide/1.0)"}


def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def _norm(text):
    """Collapse all whitespace runs (incl. newlines) to single spaces and strip."""
    return re.sub(r"\s+", " ", text).strip()


def clean_review_page(html, name):
    """VeryApt apartment-review page -> one block per resident review."""
    soup = BeautifulSoup(html, "lxml")
    blocks = []
    for r in soup.select("div.review"):
        body_el = r.select_one(".review-text")
        if not body_el:
            continue
        for toggle in body_el.select(".see-more, .see-less"):
            toggle.extract()
        body = _norm(body_el.get_text(" ", strip=True))
        if len(body) < 15:
            continue
        title_el = r.find("h3")
        title = _norm(title_el.get_text(" ", strip=True)) if title_el else ""
        attrs_el = r.select_one(".reviewer-attrs")
        attrs = _norm(attrs_el.get_text(" ", strip=True)) if attrs_el else ""
        header = f"{name}"
        if title:
            header += f' — "{title}"'
        if attrs:
            header += f" ({attrs})"
        blocks.append(f"{header}\n{body}")
    return "\n\n".join(blocks)


def _median_rents(soup, neighborhood):
    """Pull 'Studio $X / 1 Bedroom $Y / 2 Bedroom $Z' if present on a guide page."""
    text = soup.get_text(" ", strip=True)
    pairs = re.findall(r"(Studio|1 Bedroom|2 Bedroom|3 Bedroom)\s*\$?\s*([\d,]{3,6})", text)
    if not pairs:
        return ""
    seen, parts = set(), []
    for label, amount in pairs:
        if label in seen:
            continue
        seen.add(label)
        parts.append(f"{label} ${amount}")
    return f"Median rents in {neighborhood}: " + ", ".join(parts) + "."


def clean_guide_page(html, name):
    """VeryApt neighborhood guide -> description + median rents + resident reviews."""
    soup = BeautifulSoup(html, "lxml")
    neighborhood = name.replace(" neighborhood guide", "").strip()
    blocks = []

    # The description sits in a class-less div, so select it by content: it's the
    # first long prose paragraph in trafilatura's main-content extraction.
    extracted = trafilatura.extract(html) or ""
    longs = [_norm(l) for l in extracted.splitlines() if len(l.strip()) > 150]
    if longs:
        blocks.append(f"{neighborhood} neighborhood overview\n{longs[0]}")

    rents = _median_rents(soup, neighborhood)
    if rents:
        blocks.append(rents)

    for rev in soup.select("div.review"):
        content_el = rev.select_one(".review-content")
        if not content_el:
            continue
        body = _norm(content_el.get_text(" ", strip=True))
        body = re.sub(r"\s*Keep reading\s*", " ", body).strip()
        if len(body) < 25:
            continue
        apt_el = rev.select_one(".review-apartment")
        apt = _norm(apt_el.get_text(" ", strip=True)) if apt_el else ""
        tag = f" (resident of {apt})" if apt else ""
        blocks.append(f"{neighborhood} resident review{tag}\n{body}")

    return "\n\n".join(blocks)


def clean_index_page(html, name):
    """VeryApt apartments index -> a ratings comparison list (drops amenity-filter UI)."""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for card in soup.select(".listing-apartment"):
        a = card.select_one("h3 a") or card.find("h3")
        if not a:
            continue
        complex_name = _norm(a.get_text(" ", strip=True))
        rating_el = card.select_one(".user-rating-number")
        rating = _norm(rating_el.get_text(" ", strip=True)) if rating_el else ""
        rows.append(f"- {complex_name}: {rating}/10" if rating else f"- {complex_name}: no rating yet")
    if not rows:
        return ""
    header = "La Jolla / UCSD-area apartment complexes ranked by VeryApt resident rating (out of 10):"
    return header + "\n" + "\n".join(rows)


def clean_generic(html):
    """findmyplace blogs and the apartments index: main-content extraction."""
    text = trafilatura.extract(html, include_comments=False, include_tables=True) or ""
    # Drop the repeated findmyplace footer boilerplate if present.
    text = re.split(r"Find My Place\s*[—-]\s*By Students, For Students", text)[0]
    # Drop byline metadata lines (read-time, publish date) that add no content.
    drop = re.compile(
        r"^\d+\s*min read$|"
        r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}$",
        re.IGNORECASE)
    paras = [_norm(p) for p in text.split("\n") if _norm(p) and not drop.match(_norm(p))]
    return "\n\n".join(paras)


CLEANERS = {
    "review": lambda html, name: clean_review_page(html, name),
    "guide": lambda html, name: clean_guide_page(html, name),
    "blog": lambda html, name: clean_generic(html),
    "index": lambda html, name: clean_index_page(html, name),
}


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []

    for src in SOURCES:
        print(f"[fetch] {src['id']} … ", end="", flush=True)
        try:
            html = fetch(src["url"])
        except Exception as e:
            print(f"FAILED ({type(e).__name__}: {e})")
            continue
        (RAW_DIR / f"{src['id']}.html").write_text(html, encoding="utf-8")

        clean = CLEANERS[src["kind"]](html, src["name"])
        clean_path = CLEAN_DIR / f"{src['id']}.txt"
        clean_path.write_text(clean, encoding="utf-8")

        manifest.append({
            "id": src["id"], "name": src["name"], "url": src["url"],
            "kind": src["kind"], "clean_path": str(clean_path.relative_to(ROOT)),
            "clean_chars": len(clean),
        })
        print(f"ok  ({len(html):>7,} html chars -> {len(clean):>6,} clean chars)")
        time.sleep(1)  # be polite to the source sites

    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nWrote {len(manifest)} cleaned docs + manifest.json")


if __name__ == "__main__":
    main()
