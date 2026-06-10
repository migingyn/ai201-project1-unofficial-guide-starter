# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

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

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
