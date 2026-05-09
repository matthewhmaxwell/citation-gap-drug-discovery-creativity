"""
Patch the few cases where author lookup failed.

Strategy: for each broken row, do a stricter Authors search and pick the
first candidate whose works contain at least one of the figure's known_works
(by title substring). Replaces the canonical_works for that row.
"""

import json
import re
import sys
import time
from pathlib import Path

import pyalex
from pyalex import Authors, Works

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"

sys.path.insert(0, str(ROOT))


def normalize(s: str) -> str:
    return re.sub(r"[^\w\s]", " ", (s or "").lower()).strip()


# Targeted overrides: row_id -> {search_names, must_match_titles}
OVERRIDES = {
    "F06": {
        "search_names": ["Mihaly Csikszentmihalyi"],
        "must_match_titles": [
            "flow", "creativity", "psychology of optimal", "society culture and person",
            "society, culture, and person", "good business", "the systems model",
        ],
        "min_works_count": 30,
    },
    "F09b": {
        "search_names": ["Thomas B. Ward"],
        "must_match_titles": [
            "structured imagination", "creative cognition", "structure of category",
        ],
        "min_works_count": 30,
        "exclude_concepts": ["ergodic theory", "number theory", "dynamical systems"],
    },
    "F09c": {
        "search_names": ["Steven M. Smith"],
        "must_match_titles": [
            "incubation", "creative cognition", "fixation", "memory and creativity",
        ],
        "min_works_count": 30,
        "exclude_concepts": ["spinopelvic", "spine", "glioma", "cervical"],
    },
    "F11": {
        "search_names": ["Michael Levin"],
        "must_match_titles": [
            "bioelectric", "regeneration", "morphogenesis", "tame",
            "planarian", "xenopus", "left right asymmetry", "nongenetic",
            "patterning", "ion channel",
        ],
        "min_works_count": 30,
        "affiliations": ["tufts"],
    },
    "F19": {
        "search_names": ["Christopher Alexander"],
        "must_match_titles": [
            "pattern language", "notes on the synthesis", "timeless way of building",
            "nature of order",
        ],
        "min_works_count": 5,
        "exclude_concepts": ["renal", "urology", "nephrectomy"],
    },
    "F26": {
        "search_names": ["Thomas S. Kuhn", "Thomas Kuhn"],
        "must_match_titles": [
            "structure of scientific revolutions", "essential tension",
            "scientific revolutions", "paradigm",
        ],
        "min_works_count": 5,
    },
}


def works_for_author(author_id: str, top_n: int = 15) -> list[dict]:
    return (
        Works()
        .filter(authorships={"author": {"id": author_id}})
        .sort(cited_by_count="desc")
        .get(per_page=top_n)
    )


def slim(work: dict) -> dict:
    return {
        "id": work.get("id"),
        "doi": work.get("doi"),
        "title": work.get("title") or work.get("display_name"),
        "publication_year": work.get("publication_year"),
        "cited_by_count": work.get("cited_by_count") or 0,
        "type": work.get("type"),
        "authorships": [
            {
                "name": (a.get("author") or {}).get("display_name"),
                "author_id": (a.get("author") or {}).get("id"),
                "position": a.get("author_position"),
            }
            for a in (work.get("authorships") or [])
        ][:8],
        "host_venue": ((work.get("primary_location") or {}).get("source") or {}).get("display_name"),
    }


def find_correct_author(row_id: str, override: dict, last_name: str) -> tuple[str | None, list[dict]]:
    must_titles = [normalize(t) for t in override["must_match_titles"]]
    excl_concepts = [normalize(t) for t in override.get("exclude_concepts", [])]
    affil_must = [normalize(a) for a in override.get("affiliations", [])]
    min_wc = override.get("min_works_count", 0)

    candidates = []
    for sn in override["search_names"]:
        try:
            authors = Authors().search(sn).get(per_page=50)
        except Exception as e:
            print(f"  [err] {sn}: {e}")
            continue
        for a in authors:
            display = normalize(a.get("display_name") or "")
            if normalize(last_name) not in display:
                continue
            wc = a.get("works_count") or 0
            if wc < min_wc:
                continue
            concepts = [normalize(c.get("display_name") or "") for c in (a.get("x_concepts") or [])]
            if any(any(ec in c for c in concepts) for ec in excl_concepts):
                continue
            insts = []
            for ai in a.get("affiliations", []) or []:
                inst = (ai.get("institution") or {}).get("display_name") or ""
                insts.append(normalize(inst))
            last_inst = normalize(((a.get("last_known_institution") or {}) or {}).get("display_name") or "")
            if last_inst:
                insts.append(last_inst)
            if affil_must and not any(am in inst for am in affil_must for inst in insts):
                continue
            candidates.append((a, insts, concepts))
            time.sleep(0.05)

    # For each candidate, fetch top works and check whether any title matches our must_titles
    print(f"  candidates after pre-filter: {len(candidates)}")
    best_author = None
    best_works = []
    best_match_score = -1
    for a, insts, concepts in candidates[:8]:
        try:
            wks = works_for_author(a["id"], top_n=15)
        except Exception as e:
            print(f"  [werr] {a.get('display_name')}: {e}")
            continue
        match_count = 0
        matched_titles_seen = []
        for w in wks:
            tnorm = normalize(w.get("title") or w.get("display_name") or "")
            for mt in must_titles:
                if mt and mt in tnorm:
                    match_count += 1
                    matched_titles_seen.append(mt)
                    break
        score = match_count + (a.get("cited_by_count") or 0) / 100000
        print(f"    {a.get('display_name'):40} wc={a.get('works_count'):>5} cc={a.get('cited_by_count'):>7} matches={match_count}")
        if match_count >= 1 and score > best_match_score:
            best_match_score = score
            best_author = a
            best_works = wks

    return (best_author["id"] if best_author else None), best_works


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())

    for row_id, override in OVERRIDES.items():
        if row_id not in canon:
            print(f"!! {row_id} not found in canonical_papers.json")
            continue
        rec = canon[row_id]
        last_name = rec["individual_name"].split()[-1]
        print(f"\n=== Re-disambiguating {row_id} {rec['individual_name']} ===")
        author_id, wks = find_correct_author(row_id, override, last_name)
        if not author_id:
            print(f"  ** STILL no good match for {row_id}; leaving as-is **")
            continue
        slimmed = [slim(w) for w in wks]
        for s in slimmed:
            s["source_strategy"] = "author-lookup-fixed"
        slimmed.sort(key=lambda x: -(x.get("cited_by_count") or 0))
        rec["selected_author_id"] = author_id
        rec["canonical_works"] = slimmed[:5]
        rec["fix_applied"] = True
        print(f"  selected new author: {author_id}")
        for w in slimmed[:5]:
            print(f"    {w['cited_by_count']:>6}  {w['publication_year']}  {(w['title'] or '')[:80]}")
        time.sleep(0.2)

    (RAW / "canonical_papers.json").write_text(json.dumps(canon, indent=2, ensure_ascii=False))
    print("\nwrote raw/canonical_papers.json")


if __name__ == "__main__":
    main()
