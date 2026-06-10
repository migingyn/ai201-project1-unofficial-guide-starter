# The Unofficial Guide — Project 1

A retrieval-augmented (RAG) Q&A system over **UCSD off-campus housing experiences**. Ask about apartment complexes and neighborhoods near UC San Diego and get answers grounded only in collected resident reviews and housing guides, with the source documents cited.

## Setup & How to Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your free Groq API key into .env

# 1. Ingest + clean the 14 sources  -> documents/clean/ + manifest.json
python -m src.ingest
# 2. Chunk the cleaned docs         -> documents/chunks.jsonl (117 chunks)
python -m src.build_chunks
# 3. Embed into ChromaDB            -> chroma_db/
python -m src.vectorstore

# Ask a question (CLI):
python -m src.generate "What do residents complain about at Costa Verde Village?"
# Or launch the web UI at http://localhost:7860 :
python app.py

# Run the test suite (chunking + retrieval + grounding):
python -m pytest
# Reproduce the evaluation run:
python -m src.eval_retrieval
```

---

## Domain

**UC San Diego off-campus housing experiences.** The system makes searchable the unofficial, experience-based knowledge of what it's actually like to rent off-campus as a UCSD student — specific apartment complexes and neighborhoods (La Jolla, University City/UTC, Mira Mesa, Clairemont) covering rent, commute and parking, noise, maintenance, safety, and unit crowding.

This is hard to find through official channels because UCSD housing resources and apartment-listing sites advertise amenities and asking rents but don't reveal the candid tradeoffs — that Costa Verde Village has recurring roach and thin-wall complaints, that Regents La Jolla units routinely pack 4–8 people, or how the real parking and commute situation feels. Those details live only in scattered resident reviews and student discussion that no single official channel aggregates, so it's the kind of word-of-mouth knowledge a sophomore moving off-campus or an incoming transfer otherwise has to piece together by hand.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

All URLs verified to resolve on 2026-06-09. Reddit (r/UCSD), Yelp, ApartmentRatings, and Niche hard-block automated fetching and were excluded; the two cleanly-extractable sources below together span 6 complexes, 4 neighborhoods, and cost/commute/roommate topics.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | VeryApt — Costa Verde Village reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a25717-costa-verde-village-san-diego |
| 2 | VeryApt — Nobel Court reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a5512-nobel-court-san-diego |
| 3 | VeryApt — Regents La Jolla reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a5544-regents-la-jolla-san-diego |
| 4 | VeryApt — La Regencia reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a5483-la-regencia-san-diego |
| 5 | VeryApt — La Jolla del Sol reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a24827-la-jolla-del-sol-san-diego |
| 6 | VeryApt — Solazzo / Villa La Jolla reviews | Apartment review site | https://www.veryapt.com/ApartmentReview-a5573-solazzo-apartments-homes-san-diego |
| 7 | VeryApt — La Jolla apartments index (19 complexes) | Apartment review site | https://www.veryapt.com/Apartments-L5628-san-diego-la-jolla |
| 8 | VeryApt — La Jolla neighborhood guide | Neighborhood guide | https://www.veryapt.com/guides/neighborhood/465-san-diego-la-jolla/ |
| 9 | VeryApt — University City neighborhood guide | Neighborhood guide | https://www.veryapt.com/guides/neighborhood/507-san-diego-university-city/ |
| 10 | VeryApt — Mira Mesa neighborhood guide | Neighborhood guide | https://www.veryapt.com/guides/neighborhood/464-san-diego-mira-mesa/ |
| 11 | VeryApt — Clairemont Mesa neighborhood guide | Neighborhood guide | https://www.veryapt.com/guides/neighborhood/509-san-diego-clairemont-mesa/ |
| 12 | findmyplace — Best Neighborhoods for UCSD Off-Campus Housing | Unofficial housing guide (blog) | https://findmyplace.co/blog/best-neighborhoods-near-ucsd-for-students/ |
| 13 | findmyplace — San Diego Student Housing Costs (2026) | Unofficial housing guide (blog) | https://findmyplace.co/blog/san-diego-student-housing-costs-2026/ |
| 14 | findmyplace — UCSD Off-Campus Housing Timeline | Unofficial housing guide (blog) | https://findmyplace.co/blog/ucsd-off-campus-housing-timeline/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** One complete review (or guide paragraph) per chunk, with a fallback cap of ~200 tokens. I measured size in tokens with the same `all-MiniLM-L6-v2` tokenizer the embedder uses, since that model truncates anything past 256 tokens — 200 leaves headroom so nothing gets cut off.

**Overlap:** ~20–30 tokens, but only on the fallback splits. Whole reviews are already self-contained, so I didn't overlap between them — that would just repeat content and blur the boundaries.

**Why these choices fit your documents:** Most of my corpus is short, opinion-based reviews where the key info (the complex name, the sentiment, the specific gripe) is packed into a few sentences, so keeping a whole review together gives a clean, self-contained chunk instead of averaging several unrelated complaints into one vector. Preprocessing was kind-specific: I stripped each page to substantive text with `requests` + BeautifulSoup (targeted DOM extraction of each review for VeryApt pages, the 19-complex name/rating list for the index page) and `trafilatura` for the findmyplace blogs, removing nav, amenity checklists, ads, footers, and bylines. The one divergence from "one unit per chunk": the blogs are long-form prose, so splitting by paragraph left tiny fragments like "TL;DR" or the author byline — for blog docs only I greedily pack paragraphs up to the 200-token cap so headings bind to their text.

**Final chunk count:** 117 chunks across the 14 documents (avg ~102 tokens, max 200, 0 empty, 0 over the model's 256-token limit).

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers (384-dim, runs locally, no API key). I embed with `normalize_embeddings=True` and store the vectors in ChromaDB using cosine distance (`hnsw:space=cosine`), retrieving top-k=5.

**Production tradeoff reflection:** I picked MiniLM because it runs locally with no key and is plenty for short English housing reviews. If cost and real users weren't a constraint, the main reason I'd swap it out is domain accuracy — housing reviews are full of slang and synonyms (packed/crowded, loud/thin walls, roaches/bugs), and a stronger model like `bge-large-en-v1.5` or OpenAI's `text-embedding-3-large` would match those paraphrases more reliably (this actually bit me in Q1 — see the failure analysis). Multilingual support would only matter if I added non-English sources later, and context length barely matters since my chunks are short reviews well under the 256-token limit. The tradeoff for any upgrade is latency — bigger local models or an API round-trip are slower — but at k=5 over a small corpus that hit wouldn't be noticeable.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** Grounding is enforced two ways, not just by asking nicely. First, a structural relevance gate: I only pass chunks whose cosine distance is ≤ 0.6, and if none qualify the system returns the decline string *without ever calling the LLM*, so out-of-corpus questions can't be answered from training knowledge. Second, the system prompt is strict — the model is told: *"Answer the user's question using ONLY the information in the numbered context documents… Do not use any outside or prior knowledge. Do not guess or generalize beyond what the context states. If the context does not contain enough information to answer, reply with exactly: 'I don't have enough information on that.'"* The retrieved chunks are formatted as a numbered list, each labeled with its source name, and the model runs at temperature 0.

**How source attribution is surfaced in the response:** Programmatically, not left to the LLM. After generation I build the source list from the metadata of the chunks I actually fed the model (deduped by source name + URL), so attribution can't drift from what was retrieved. The Gradio UI shows the answer and a separate "Retrieved from" panel listing those sources. If the model declines (no usable context), I clear the source list so a non-answer never gets bogus citations.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do residents complain about most at Costa Verde Village? | Roaches/pests, thin walls and noise, parking shortage, car break-ins; low ~5/10 | "Poor management and safety concerns — poor management, noise, feelings of unsafety, including car break-ins." Cited Costa Verde reviews. Missed roaches and parking. | Partially relevant (all 5 from Costa Verde, but the detailed roach/parking review wasn't in the top-5) | **Partially accurate** |
| 2 | How does median 1-bedroom rent in University City compare to Mira Mesa? | UC ~$2,100 vs Mira Mesa ~$1,800; Mira Mesa is the cheaper/farther option | "University City 1BR is $2,100, Mira Mesa is $1,800 — UC is $300 more." Cited Mira Mesa + University City guides + findmyplace. | Relevant (both rent chunks retrieved) | **Accurate** |
| 3 | How crowded do students say Regents La Jolla units get? | Units packed with 4–8 people | "I don't have enough information on that." (declined) | Relevant source (all Regents reviews) but none mention crowding | **Inaccurate (declined)** |
| 4 | According to the guides, which neighborhood is the budget option, and what commute tradeoff? | Mira Mesa (or Clairemont) — cheaper, but car-dependent / longer commute | "Mira Mesa; needs reliable transport, ~15–25 min drive, transit takes longer." Cited findmyplace. | Relevant (all findmyplace best-neighborhoods) | **Accurate** |
| 5 | What downsides do reviewers report about La Regencia despite its low rent? | Nightmare parking, nighttime noise, older interiors, safety concerns | "Old buildings, expensive utilities, not gated (break-ins/lost packages), unresponsive management, parking-lot construction, Friday-night noise." Cited La Regencia. | Relevant (all La Regencia reviews) | **Accurate** |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

Two questions came back less than perfect (Q1 partial, Q3 declined), which I'm glad about — it means the test set actually exercises the system's limits instead of rubber-stamping it. Every answer that *was* produced stayed grounded in cited sources, and no answer pulled in outside knowledge.

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Q3 — "How crowded do students say Regents La Jolla units get?" (I'll also note a secondary partial failure on Q1 below.)

**What the system returned:** "I don't have enough information on that." It declined instead of answering, even though retrieval returned five on-topic Regents La Jolla reviews (cosine distances 0.332–0.400).

**Root cause (tied to a specific pipeline stage):** This is an **ingestion/coverage** failure, not a retrieval or generation bug. The expected "4–8 people per unit" crowding figure never made it into the corpus — the actual Regents reviews I scraped only talk about price, location (10-min bike), build quality, and management; none mentions occupancy or crowding. That detail came from an early research summary I used to *pick* sources, not from the source text I ended up ingesting. So retrieval did its job (right complex, low distances) and generation did its job too — because the system is strictly grounded, it correctly refused to invent a number rather than hallucinating one. In other words the "failure" is the system honestly reporting a gap in its own data, which is the behavior I want, just not the answer my eval expected.

A second, softer failure showed up in **Q1**: the answer captured management/safety/noise/car-break-ins but missed the *signature* complaints (roaches and the parking shortage). I checked the retrieved chunks — "roach" and "parking" aren't in any of the top-5. The cause is **retrieval ranking + chunk length**: short, punchy reviews like "Unsafe, poorly managed, and loud" embed very close to a generic "what do people complain about" query, while the long, detailed "Do not live here" review that actually lists roaches and parking dilutes its signal across ~200 tokens and ranks below the top-5 (it jumps to rank #1, distance 0.208, only when I query the explicit keywords). The answer was still fully grounded in what it got — it just didn't get the best evidence.

**What you would change to fix it:** For Q3, fix it at ingestion — pull in more Regents sources (or the original review threads that mention occupancy) so the fact actually exists in the corpus, or honestly revise the eval question to what the data supports. For Q1, raise top-k (e.g. 8–10) or add MMR re-ranking so a long detailed complaint isn't crowded out by several short generic ones, and/or move to a stronger embedding model that's less sensitive to chunk length.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Because planning.md already pinned down concrete numbers — ~200-token chunk cap, k=5, cosine distance, the embedding model, and the 5 eval questions — building each stage was a matter of implementing a clear target instead of guessing as I went. The Anticipated Challenges section was the most useful part: I'd written down that my corpus was concentrated in two sites with thin coverage on some topics, and that exact risk is what produced the Q3 failure, so when retrieval returned on-topic Regents reviews but the answer wasn't there, I already knew where to look instead of assuming the code was broken.

**One way your implementation diverged from the spec, and why:** The spec said "one complete review = one chunk, fallback-split only," but when I actually built it the findmyplace blogs (long-form prose with lots of headings) split into tiny fragment chunks like "TL;DR" and the author byline. So for blog documents only I added greedy paragraph packing up to the 200-token cap, while reviews and guides still stay one-unit-per-chunk. I also added a cosine-distance relevance gate to the grounding step that wasn't in the original spec, because I wanted out-of-corpus questions to be refused before the LLM is even called rather than relying on the prompt alone.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — ingestion + chunking**

- *What I gave the AI:* My Documents table, the Chunking Strategy section, and the pipeline diagram, and asked it to implement a script that loads the 14 HTML sources, cleans them, and produces chunks matching my token cap and overlap.
- *What it produced:* A first version that used `trafilatura` generically on every page and split everything strictly by unit.
- *What I changed or overrode:* When I actually read the cleaned output it was wrong in two ways — on VeryApt review pages it dumped the amenity/pricing checklist instead of the reviews, and the blogs produced tiny heading/byline fragment chunks. I directed it to switch to targeted DOM extraction per page type (each `div.review` for review pages, the name+rating list for the index page) and to add kind-aware paragraph packing for the blogs only. I also caught that the median-rent numbers (which my eval Q2 depends on) were getting fragmented and had it pull those with a dedicated regex.

**Instance 2 — grounded generation**

- *What I gave the AI:* My Retrieval Approach section and the grounding requirement (answer only from retrieved context, with source attribution), and asked it to wire up Groq `llama-3.3-70b-versatile` plus a Gradio interface.
- *What it produced:* A working `ask()` that retrieved chunks, prompted Groq with a grounding instruction, and returned an answer plus the retrieved sources.
- *What I changed or overrode:* I tested it and found the system still listed source citations even when the model replied "I don't have enough information" — citing sources for a non-answer. I had it clear the sources whenever the model declines, and I added a cosine-distance relevance gate so genuinely out-of-corpus questions short-circuit to the decline message before the LLM is called at all, instead of trusting the prompt by itself.
