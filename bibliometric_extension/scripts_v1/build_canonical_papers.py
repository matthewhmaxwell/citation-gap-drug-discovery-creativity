"""
Build canonical-papers list per figure.

Strategy
--------
For each individual we (1) search OpenAlex authors for matching name,
(2) score candidates by match against affiliation hints + topic hints,
(3) take the top-scoring author, (4) pull their top-cited works.

Then we **also** query for each known_work title across OpenAlex's works
search (works.search()) — this is essential for older books like *The Act
of Creation*, *The Sciences of the Artificial*, *Pattern Language*,
*Structure of Scientific Revolutions* whose authors may have weak
metadata in OpenAlex but whose works are well-indexed.

We union the two sources and dedupe by OpenAlex work ID.
For each (figure_group, work) we keep:
  - openalex_id
  - title
  - publication_year
  - cited_by_count
  - authorships (display names + author ids)
  - source_strategy: "author-lookup" | "title-lookup" | "both"
  - matched_known_work: which hint string matched (if any)
"""

import json
import re
import time
import sys
from pathlib import Path

import pyalex
from pyalex import Authors, Works

# Polite pool: OpenAlex requests an email so they can throttle/contact.
pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3
pyalex.config.retry_backoff_factor = 0.5

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT))
from scripts.figures import FIGURES  # noqa: E402

# Map row id -> figure_group (the 30 named figures)
FIGURE_GROUP = {
    "F01": "Wiggins", "F02": "Boden", "F03": "Hofstadter", "F04": "Lakatos",
    "F05": "Wallas", "F06": "Csikszentmihalyi", "F07": "Gentner",
    "F08a": "Fauconnier-Turner", "F08b": "Fauconnier-Turner",
    "F09a": "Finke-Ward-Smith", "F09b": "Finke-Ward-Smith", "F09c": "Finke-Ward-Smith",
    "F10": "Koestler", "F11": "Levin",
    "F12": "Simon", "F13": "Newell", "F14": "Amabile", "F15": "Sternberg",
    "F16": "Campbell", "F17": "Simonton", "F18": "Schon", "F19": "Alexander",
    "F20": "Altshuller", "F21": "Stokes", "F22": "Hutchins",
    "F23a": "Clark-Chalmers", "F23b": "Clark-Chalmers",
    "F24": "Latour", "F25": "Knorr-Cetina", "F26": "Kuhn", "F27": "Feyerabend",
    "F28": "Kauffman", "F29": "Kaufman", "F30": "Runco",
}


def normalize(s: str) -> str:
    return re.sub(r"[^\w\s]", " ", (s or "").lower()).strip()


def find_author_id(figure: dict) -> tuple[str | None, dict]:
    """
    Return (author openalex id, candidate metadata) for the best-matching author.
    Score candidates by affiliation + topic hint matches and by works_count.
    """
    affil_hints = [normalize(a) for a in figure.get("affiliations", [])]
    topic_hints = [normalize(t) for t in figure.get("topics", [])]
    best = None
    best_score = -1
    log_candidates = []

    for sn in figure["search_names"]:
        try:
            results = Authors().search(sn).get(per_page=25)
        except Exception as e:
            print(f"    [author search err] {sn!r}: {e}", file=sys.stderr)
            continue
        for a in results:
            display = normalize(a.get("display_name") or "")
            if not display:
                continue
            # Require at least the last name to match for safety
            last_name = normalize(figure["name"]).split()[-1]
            if last_name not in display:
                continue
            score = 0
            # Works count is a strong prior
            wc = a.get("works_count") or 0
            score += min(wc, 1000) / 200  # cap influence
            # Citations indicate prominence
            cc = a.get("cited_by_count") or 0
            score += min(cc, 200000) / 20000
            # Affiliation match
            insts = []
            for ai in a.get("affiliations", []) or []:
                inst = (ai.get("institution") or {}).get("display_name") or ""
                insts.append(normalize(inst))
            last_inst = (
                normalize(((a.get("last_known_institution") or {}) or {}).get("display_name") or "")
            )
            if last_inst:
                insts.append(last_inst)
            for hint in affil_hints:
                if any(hint and hint in inst for inst in insts):
                    score += 5
                    break
            # Topic / concept match
            concepts = [normalize(c.get("display_name") or "") for c in (a.get("x_concepts") or [])]
            for hint in topic_hints:
                if any(hint and hint in c for c in concepts):
                    score += 2
            log_candidates.append({
                "id": a.get("id"),
                "display_name": a.get("display_name"),
                "works_count": wc,
                "cited_by_count": cc,
                "affiliations": insts[:5],
                "x_concepts": concepts[:5],
                "score": round(score, 3),
                "search_name": sn,
            })
            if score > best_score:
                best_score = score
                best = a
            time.sleep(0.05)
        time.sleep(0.1)

    if best is None:
        return None, {"candidates": log_candidates}
    return best.get("id"), {
        "candidates": sorted(log_candidates, key=lambda x: -x["score"])[:5],
        "selected": {
            "id": best.get("id"),
            "display_name": best.get("display_name"),
            "works_count": best.get("works_count"),
            "cited_by_count": best.get("cited_by_count"),
            "score": round(best_score, 3),
        },
    }


def works_for_author(author_id: str, top_n: int = 10) -> list[dict]:
    """Top-cited works by an author."""
    try:
        results = (
            Works()
            .filter(authorships={"author": {"id": author_id}})
            .sort(cited_by_count="desc")
            .get(per_page=top_n)
        )
        return results
    except Exception as e:
        print(f"    [author works err] {author_id}: {e}", file=sys.stderr)
        return []


def works_by_title(title_substr: str, last_name: str, top_n: int = 5) -> list[dict]:
    """Find works whose title matches a known-work hint, filtered by an author last-name token."""
    try:
        results = Works().search(title_substr).get(per_page=top_n)
    except Exception as e:
        print(f"    [title search err] {title_substr!r}: {e}", file=sys.stderr)
        return []
    out = []
    last_name_norm = normalize(last_name)
    for w in results:
        title_norm = normalize(w.get("title") or w.get("display_name") or "")
        # Confirm it's at least roughly our work (title substring should be in result)
        if normalize(title_substr) not in title_norm and len(normalize(title_substr)) > 20:
            continue
        # Confirm an author matches
        authors_norm = [normalize((a.get("author") or {}).get("display_name") or "")
                        for a in (w.get("authorships") or [])]
        if not any(last_name_norm in a for a in authors_norm):
            continue
        out.append(w)
    return out


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


def main():
    out = {}
    log = {}
    for fig in FIGURES:
        print(f"\n=== {fig['id']} {fig['name']} (group={FIGURE_GROUP[fig['id']]}) ===")
        author_id, cand_log = find_author_id(fig)
        log[fig["id"]] = cand_log
        works_by_id = {}
        if author_id:
            print(f"    selected author: {author_id} ({cand_log.get('selected',{}).get('display_name')})")
            for w in works_for_author(author_id, top_n=10):
                wid = w.get("id")
                if wid:
                    s = slim(w)
                    s["source_strategy"] = "author-lookup"
                    works_by_id[wid] = s
        # Title-based lookups (catches older books with weak author metadata)
        last_name = fig["name"].split()[-1]
        for hint in fig.get("known_works", []):
            for w in works_by_title(hint, last_name, top_n=5):
                wid = w.get("id")
                if not wid:
                    continue
                if wid in works_by_id:
                    works_by_id[wid]["source_strategy"] = "both"
                    works_by_id[wid].setdefault("matched_known_works", []).append(hint)
                else:
                    s = slim(w)
                    s["source_strategy"] = "title-lookup"
                    s["matched_known_works"] = [hint]
                    works_by_id[wid] = s
        # Pick top by citation count, cap at 5 works
        works_sorted = sorted(works_by_id.values(), key=lambda x: -(x.get("cited_by_count") or 0))
        top = works_sorted[:5]
        print(f"    top works: {len(top)} (of {len(works_sorted)} unique candidates)")
        for w in top:
            print(f"      {w['cited_by_count']:>6}  {w['publication_year']}  {(w['title'] or '')[:80]}")
        out[fig["id"]] = {
            "figure_row_id": fig["id"],
            "figure_group": FIGURE_GROUP[fig["id"]],
            "individual_name": fig["name"],
            "group": fig["group"],
            "selected_author_id": author_id,
            "search_log_keep_top5": cand_log,
            "canonical_works": top,
            "all_candidate_works_count": len(works_sorted),
        }
        time.sleep(0.2)

    (RAW / "canonical_papers.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    (RAW / "canonical_papers_search_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    # Summary
    summary = []
    for fid, rec in out.items():
        summary.append({
            "id": fid,
            "figure_group": rec["figure_group"],
            "name": rec["individual_name"],
            "n_canonical_works": len(rec["canonical_works"]),
            "selected_author_id": rec["selected_author_id"],
        })
    print("\n=== Summary ===")
    for s in summary:
        print(f"  {s['id']:5} {s['figure_group']:20} {s['name']:30} n={s['n_canonical_works']}")


if __name__ == "__main__":
    main()
