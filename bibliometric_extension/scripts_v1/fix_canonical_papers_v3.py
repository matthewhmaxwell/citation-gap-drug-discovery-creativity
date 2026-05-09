"""
Third-pass: now that we have correct author IDs for F06 and F26, also pull
their top-cited works directly so we have a full top-5 for each.
"""

import json
import sys
import time
from pathlib import Path

import pyalex
from pyalex import Works

pyalex.config.email = "bibliometric_extension@example.org"

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"


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
        "source_strategy": "author-lookup-v3",
    }


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    for row_id in ["F06", "F26"]:
        rec = canon.get(row_id)
        if not rec or not rec.get("selected_author_id"):
            continue
        existing = {w["id"]: w for w in rec.get("canonical_works", [])}
        author_id = rec["selected_author_id"]
        try:
            results = (
                Works()
                .filter(authorships={"author": {"id": author_id}})
                .sort(cited_by_count="desc")
                .get(per_page=15)
            )
        except Exception as e:
            print(f"  [err] {row_id}: {e}")
            continue
        for w in results:
            wid = w.get("id")
            if wid and wid not in existing:
                existing[wid] = slim(w)
        merged = sorted(existing.values(), key=lambda x: -(x.get("cited_by_count") or 0))
        rec["canonical_works"] = merged[:5]
        print(f"\n{row_id}: now {len(rec['canonical_works'])} works")
        for w in rec["canonical_works"]:
            print(f"  {w['cited_by_count']:>6}  {w['publication_year']}  {(w['title'] or '')[:80]}")
        time.sleep(0.2)

    (RAW / "canonical_papers.json").write_text(json.dumps(canon, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
