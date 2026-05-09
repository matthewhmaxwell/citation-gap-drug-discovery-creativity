"""
Second-pass fix for cases that still failed: F06 Csikszentmihalyi and F26 Kuhn.

For these we use **title-based lookup only** — find the works first, then
record the modal author_id across them as the figure's author_id.
"""

import json
import re
import sys
import time
from pathlib import Path

import pyalex
from pyalex import Works

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"


def normalize(s: str) -> str:
    return re.sub(r"[^\w\s]", " ", (s or "").lower()).strip()


TITLE_FIXES = {
    "F06": {
        "last_name": "Csikszentmihalyi",
        "title_searches": [
            "Flow: The Psychology of Optimal Experience",
            "Creativity: Flow and the Psychology of Discovery and Invention",
            "Beyond Boredom and Anxiety",
            "Society, Culture, and Person: A Systems View",
            "The Systems Model of Creativity",
            "Good Business: Leadership, Flow, and the Making of Meaning",
            "The art of seeing",
            "Optimal experience psychological studies of flow",
        ],
    },
    "F26": {
        "last_name": "Kuhn",
        "title_searches": [
            "The Structure of Scientific Revolutions",
            "The Essential Tension",
            "The Copernican Revolution",
            "Black-Body Theory and the Quantum Discontinuity",
        ],
    },
}


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
        "source_strategy": "title-lookup-only",
    }


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    for row_id, cfg in TITLE_FIXES.items():
        rec = canon.get(row_id)
        if not rec:
            continue
        print(f"\n=== Title-only fix for {row_id} {rec['individual_name']} ===")
        last_name = normalize(cfg["last_name"])
        works_by_id: dict[str, dict] = {}
        author_id_votes: dict[str, int] = {}
        for ts in cfg["title_searches"]:
            try:
                results = Works().search(ts).get(per_page=10)
            except Exception as e:
                print(f"  [err] {ts!r}: {e}")
                continue
            for w in results:
                tnorm = normalize(w.get("title") or w.get("display_name") or "")
                if normalize(ts.split(":")[0]) not in tnorm and len(tnorm) < 4:
                    continue
                # Verify last-name matches at least one author
                authorships = w.get("authorships") or []
                authors_norm = [normalize((a.get("author") or {}).get("display_name") or "") for a in authorships]
                if not any(last_name in a for a in authors_norm):
                    continue
                wid = w.get("id")
                if wid and wid not in works_by_id:
                    works_by_id[wid] = slim(w)
                # vote on author id
                for a in authorships:
                    aobj = a.get("author") or {}
                    aname = normalize(aobj.get("display_name") or "")
                    if last_name in aname:
                        aid = aobj.get("id")
                        if aid:
                            author_id_votes[aid] = author_id_votes.get(aid, 0) + 1
            time.sleep(0.15)

        if not works_by_id:
            print(f"  ** still no matches **")
            continue

        works_sorted = sorted(works_by_id.values(), key=lambda x: -(x.get("cited_by_count") or 0))
        modal_author = max(author_id_votes, key=lambda k: author_id_votes[k]) if author_id_votes else None
        rec["selected_author_id"] = modal_author
        rec["canonical_works"] = works_sorted[:5]
        rec["fix_applied"] = "title-only-v2"
        print(f"  modal author id: {modal_author}  (votes: {author_id_votes})")
        for w in works_sorted[:5]:
            print(f"    {w['cited_by_count']:>6}  {w['publication_year']}  {(w['title'] or '')[:80]}")

    (RAW / "canonical_papers.json").write_text(json.dumps(canon, indent=2, ensure_ascii=False))
    print("\nwrote raw/canonical_papers.json")


if __name__ == "__main__":
    main()
