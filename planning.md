# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I decided to choose the domain of off-campus housing for my college, UCSD, as it can be hard to navigate through as a sophomore transitioning into their 3rd year, or for a transfer student just arriving to the school, or for anybody who has to find housing off-campus. Current knowledge is outdated. It's harder to navigate through random online sources that may or may not be valid, finding on-campus resources, and getting word-of-mouth; therefore, an unofficial guide would fill this knowledge gap and make it easier for any student to obtain that information ungatekept.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

All URLs verified to resolve (HTTP 200) on 2026-06-09. Reddit (r/UCSD), Yelp, ApartmentRatings, and Niche were dropped because they hard-block automated fetching — the two sources below (VeryApt resident reviews + findmyplace student-housing guides) extract cleanly and together span 6 complexes, 4 neighborhoods, and cost/commute/roommate topics.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | VeryApt — Costa Verde Village reviews | Resident reviews of the UTC complex: roaches, thin walls/noise, parking shortage and car vandalism, near the UTC trolley (13 reviews, 5.3/10) | https://www.veryapt.com/ApartmentReview-a25717-costa-verde-village-san-diego |
| 2 | VeryApt — Nobel Court reviews | Renter experiences on Nobel Dr / UTC: management, amenities, walkability to Trader Joe's/Ralph's and shuttle stops | https://www.veryapt.com/ApartmentReview-a5512-nobel-court-san-diego |
| 3 | VeryApt — Regents La Jolla reviews | Student reviews: ~10-min bike to UCSD, gated security, rising rents, crowding (4–8 people per unit) | https://www.veryapt.com/ApartmentReview-a5544-regents-la-jolla-san-diego |
| 4 | VeryApt — La Regencia reviews | One of the cheapest La Jolla student complexes: good value/maintenance vs. nightmare parking, night noise, older interiors, safety concerns | https://www.veryapt.com/ApartmentReview-a5483-la-regencia-san-diego |
| 5 | VeryApt — La Jolla del Sol reviews | Budget UCSD-adjacent complex: well-kept pools/tennis/gym, quiet, but annual rent hikes and management communication issues | https://www.veryapt.com/ApartmentReview-a24827-la-jolla-del-sol-san-diego |
| 6 | VeryApt — Solazzo / Villa La Jolla reviews | Lower-rent older Villa La Jolla Dr complex within walking distance of campus | https://www.veryapt.com/ApartmentReview-a5573-solazzo-apartments-homes-san-diego |
| 7 | VeryApt — La Jolla apartments index (19 complexes) | Aggregated ratings/review links for 19 La Jolla/UCSD-area complexes — supports "which complex" comparison questions | https://www.veryapt.com/Apartments-L5628-san-diego-la-jolla |
| 8 | VeryApt — La Jolla neighborhood guide | Living-in-La-Jolla overview: median rent, transit, walkability to UCSD, resident satisfaction scores | https://www.veryapt.com/guides/neighborhood/465-san-diego-la-jolla/ |
| 9 | VeryApt — University City neighborhood guide | Prime student neighborhood next to campus: rent (studio $1,900 / 1BR $2,100 / 2BR $2,500), transit/shuttle access, 7.4/10 | https://www.veryapt.com/guides/neighborhood/507-san-diego-university-city/ |
| 10 | VeryApt — Mira Mesa neighborhood guide | Lower-cost suburban area along I-5: rent (studio $1,400 / 1BR $1,800 / 2BR $2,000), value/amenity ratings | https://www.veryapt.com/guides/neighborhood/464-san-diego-mira-mesa/ |
| 11 | VeryApt — Clairemont Mesa neighborhood guide | More affordable, car-dependent alternative under University City, <3 miles from campus | https://www.veryapt.com/guides/neighborhood/509-san-diego-clairemont-mesa/ |
| 12 | findmyplace — Best Neighborhoods for UCSD Off-Campus Housing | Where UCSD students actually live and why — La Jolla/UTC vs. Clairemont vs. Mira Mesa, with commute tradeoffs | https://findmyplace.co/blog/best-neighborhoods-near-ucsd-for-students/ |
| 13 | findmyplace — San Diego Student Housing Costs (2026) | Cost breakdown: $800–$1,600/mo per person, shared vs. private room pricing, +$150–$300 utilities/parking, $2,000–$4,000 move-in | https://findmyplace.co/blog/san-diego-student-housing-costs-2026/ |
| 14 | findmyplace — UCSD Off-Campus Housing Timeline | Month-by-month search timeline, roommate planning, and advice on checking sublease/lease-transfer policies before signing | https://findmyplace.co/blog/ucsd-off-campus-housing-timeline/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do residents complain about most at Costa Verde Village? | Recurring roaches/pests, thin walls and noise, a parking shortage, and reports of car break-ins/vandalism — overall a low ~5/10 rating despite the convenient UTC location. |
| 2 | How does median 1-bedroom rent in University City compare to Mira Mesa? | University City is more expensive (~$2,100/mo for a 1BR) than Mira Mesa (~$1,800/mo); Mira Mesa is the budget tradeoff but is more car-dependent and farther from campus. |
| 3 | How crowded do students say Regents La Jolla units get? | Students report units packed with 4–8 people, alongside rising rents — though it's gated and only about a 10-minute bike to campus. |
| 4 | Which neighborhood should a budget-conscious UCSD student consider, and what's the tradeoff? | Mira Mesa (or Clairemont) — lower rent than La Jolla/UTC, but you'll need a car and accept a longer commute to campus. |
| 5 | Is La Regencia a good cheap option near campus, and what are the downsides? | It's one of the cheapest La Jolla student complexes with decent value/maintenance, but downsides include nightmare parking, nighttime noise, older interiors, and some safety concerns. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Source concentration → thin coverage on some subtopics.** Because Reddit, Yelp, ApartmentRatings, and Niche all block automated fetching, the corpus draws from only two sites (VeryApt + findmyplace). Specific complex reviews, the four main neighborhoods, and cost are well covered, but Pacific Beach / North Park and authentic Reddit-style student discussion are thin. A query like "What do students say about living in Pacific Beach?" may retrieve loosely-related La Jolla content and produce a weakly-grounded or hallucinated answer — a strong candidate for the required evaluation failure case.

2. **Conflicting / outdated facts across documents.** Rent figures and resident opinions disagree between sources and over time (e.g., a guide's "median 1BR" vs. an individual review's quoted rent; a 2026 cost article vs. older review text). Retrieval may surface two chunks that contradict each other, so the generation step must attribute each claim to its source rather than averaging them into one confident-but-wrong number.

3. **Reviews split key info across chunk boundaries.** Individual reviews bundle several distinct points (parking, noise, management, safety) into one short blurb. If chunking is too aggressive it can separate a complaint from the complex name it refers to, breaking attribution; if too coarse it dilutes the relevant sentence within unrelated text — informing the chunking decisions in Milestone 2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
