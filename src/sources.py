"""The 14 source documents for the UCSD off-campus housing corpus (see planning.md).

`kind` selects which cleaner runs in ingest.py:
  review = VeryApt apartment-review page (targeted DOM extraction of each review)
  guide  = VeryApt neighborhood guide (description + median rents + resident reviews)
  index  = VeryApt multi-complex listing page (generic main-content extraction)
  blog   = findmyplace article (generic main-content extraction)
"""

SOURCES = [
    {"id": "01_costa_verde_village", "kind": "review",
     "name": "Costa Verde Village (UTC) — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a25717-costa-verde-village-san-diego"},
    {"id": "02_nobel_court", "kind": "review",
     "name": "Nobel Court (UTC) — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a5512-nobel-court-san-diego"},
    {"id": "03_regents_la_jolla", "kind": "review",
     "name": "Regents La Jolla — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a5544-regents-la-jolla-san-diego"},
    {"id": "04_la_regencia", "kind": "review",
     "name": "La Regencia — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a5483-la-regencia-san-diego"},
    {"id": "05_la_jolla_del_sol", "kind": "review",
     "name": "La Jolla del Sol — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a24827-la-jolla-del-sol-san-diego"},
    {"id": "06_solazzo_villa_la_jolla", "kind": "review",
     "name": "Solazzo / Villa La Jolla — resident reviews",
     "url": "https://www.veryapt.com/ApartmentReview-a5573-solazzo-apartments-homes-san-diego"},
    {"id": "07_la_jolla_apartments_index", "kind": "index",
     "name": "La Jolla / UCSD-area apartments index (19 complexes)",
     "url": "https://www.veryapt.com/Apartments-L5628-san-diego-la-jolla"},
    {"id": "08_la_jolla_guide", "kind": "guide",
     "name": "La Jolla neighborhood guide",
     "url": "https://www.veryapt.com/guides/neighborhood/465-san-diego-la-jolla/"},
    {"id": "09_university_city_guide", "kind": "guide",
     "name": "University City neighborhood guide",
     "url": "https://www.veryapt.com/guides/neighborhood/507-san-diego-university-city/"},
    {"id": "10_mira_mesa_guide", "kind": "guide",
     "name": "Mira Mesa neighborhood guide",
     "url": "https://www.veryapt.com/guides/neighborhood/464-san-diego-mira-mesa/"},
    {"id": "11_clairemont_mesa_guide", "kind": "guide",
     "name": "Clairemont Mesa neighborhood guide",
     "url": "https://www.veryapt.com/guides/neighborhood/509-san-diego-clairemont-mesa/"},
    {"id": "12_best_neighborhoods", "kind": "blog",
     "name": "findmyplace — Best Neighborhoods for UCSD Off-Campus Housing",
     "url": "https://findmyplace.co/blog/best-neighborhoods-near-ucsd-for-students/"},
    {"id": "13_housing_costs_2026", "kind": "blog",
     "name": "findmyplace — San Diego Student Housing Costs (2026)",
     "url": "https://findmyplace.co/blog/san-diego-student-housing-costs-2026/"},
    {"id": "14_housing_timeline", "kind": "blog",
     "name": "findmyplace — UCSD Off-Campus Housing Timeline",
     "url": "https://findmyplace.co/blog/ucsd-off-campus-housing-timeline/"},
]
