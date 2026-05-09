"""
3.2 v3 cross-OpenAlex co-citation — runs on VPS with fresh budget.
156 creativity × 27 DD/methodology = 4,212 pair queries.
"""

import json, time, sys
from pathlib import Path

import pyalex
from pyalex import Works
import pandas as pd
from tqdm import tqdm

pyalex.config.email = "biblio_v3@example.org"
pyalex.config.max_retries = 2
pyalex.config.retry_backoff_factor = 0.3

import requests as _requests
_orig_get = _requests.Session.get
def _patched_get(self, url, **kw):
    kw.setdefault("timeout", 30)
    return _orig_get(self, url, **kw)
_requests.Session.get = _patched_get

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)


def short_id(url):
    return url.rsplit("/", 1)[-1]


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    canonical_set = json.loads((RAW / "v3_canonical_papers.json").read_text())
    dd = canonical_set["final_27_set"]

    creat = []
    for row_id, rec in canon.items():
        for w in rec["canonical_works"]:
            creat.append({
                "id": w["id"],
                "short_id": short_id(w["id"]) if w.get("id") else None,
                "figure_row_id": row_id,
                "figure_group": rec["figure_group"],
                "individual_name": rec["individual_name"],
                "title": w["title"],
                "year": w["publication_year"],
                "global_cited_by_count": w["cited_by_count"],
            })
    seen = set()
    creat_unique = []
    for c in creat:
        if not c["id"] or c["id"] in seen:
            continue
        seen.add(c["id"])
        creat_unique.append(c)

    n_pairs = len(creat_unique) * len(dd)
    print(f"Pairs: {len(creat_unique)} × {len(dd)} = {n_pairs}")

    partial_path = PROC / "co_citation_v3_pairs.csv"
    done_keys = set()
    rows = []
    if partial_path.exists():
        try:
            existing = pd.read_csv(partial_path)
            for _, r in existing.iterrows():
                done_keys.add((r["creativity_canonical_id"], r["dd_canonical_id"]))
                rows.append(r.to_dict())
            print(f"Resuming with {len(done_keys)} pairs already complete")
        except Exception:
            pass

    pbar = tqdm(total=n_pairs, initial=len(done_keys), unit="pair")
    save_every = 200
    pairs_since_save = 0

    for c in creat_unique:
        if c["global_cited_by_count"] < 5:
            for d in dd:
                if (c["id"], d["openalex_id"]) in done_keys:
                    pbar.update(1)
                    continue
                rows.append({
                    "creativity_canonical_id": c["id"],
                    "creativity_short_id": c["short_id"],
                    "figure_group": c["figure_group"],
                    "individual_name": c["individual_name"],
                    "creativity_title": c["title"],
                    "creativity_year": c["year"],
                    "creativity_global_cites": c["global_cited_by_count"],
                    "dd_canonical_id": d["openalex_id"],
                    "dd_label": d["label"],
                    "dd_subdomain": d.get("subdomain") or d.get("selection_rationale", ""),
                    "dd_title": d["title"],
                    "dd_year": d["year"],
                    "co_citation_count": 0,
                    "skipped_low_cites": True,
                })
                pbar.update(1)
            continue
        for d in dd:
            if (c["id"], d["openalex_id"]) in done_keys:
                pbar.update(1)
                continue
            try:
                cnt = (
                    Works()
                    .filter(cites=c["short_id"])
                    .filter(cites=short_id(d["openalex_id"]))
                    .count()
                )
            except Exception as e:
                cnt = -1
                print(f"\n[err] {c['short_id']} x {short_id(d['openalex_id'])}: {e}")
            pairs_since_save += 1
            if pairs_since_save >= save_every:
                pd.DataFrame(rows).to_csv(partial_path, index=False)
                pairs_since_save = 0
            rows.append({
                "creativity_canonical_id": c["id"],
                "creativity_short_id": c["short_id"],
                "figure_group": c["figure_group"],
                "individual_name": c["individual_name"],
                "creativity_title": c["title"],
                "creativity_year": c["year"],
                "creativity_global_cites": c["global_cited_by_count"],
                "dd_canonical_id": d["openalex_id"],
                "dd_label": d["label"],
                "dd_subdomain": d.get("subdomain") or d.get("selection_rationale", ""),
                "dd_title": d["title"],
                "dd_year": d["year"],
                "co_citation_count": cnt,
                "skipped_low_cites": False,
            })
            pbar.update(1)
            time.sleep(0.05)
    pbar.close()

    df = pd.DataFrame(rows)
    df.to_csv(partial_path, index=False)

    # Aggregate
    fg = (
        df[~df["skipped_low_cites"]]
        .groupby(["figure_group"], as_index=False)
        .agg(
            total_co_cites=("co_citation_count", lambda s: int(s[s >= 0].sum())),
            n_dd_papers_with_any_co_cite=("co_citation_count", lambda s: int((s > 0).sum())),
        )
        .sort_values("total_co_cites", ascending=False)
    )
    fg.to_csv(PROC / "co_citation_v3_by_figure_group.csv", index=False)

    nonzero_pairs = df[df["co_citation_count"] > 0]
    print(f"Pairs with co-cite > 0: {len(nonzero_pairs)} of {(~df['skipped_low_cites']).sum()}")

    # Bridging papers
    bridging = []
    for _, r in tqdm(nonzero_pairs.iterrows(), total=len(nonzero_pairs), desc="bridges"):
        try:
            res = (
                Works()
                .filter(cites=r["creativity_short_id"])
                .filter(cites=short_id(r["dd_canonical_id"]))
                .select(["id","doi","title","publication_year","type","cited_by_count","primary_location"])
                .get(per_page=25)
            )
        except Exception:
            continue
        for w in res:
            primary_loc = w.get("primary_location") or {}
            src = (primary_loc.get("source") or {}) if isinstance(primary_loc, dict) else {}
            bridging.append({
                "bridge_paper_id": w.get("id"),
                "bridge_paper_doi": w.get("doi"),
                "bridge_paper_title": w.get("title"),
                "bridge_paper_year": w.get("publication_year"),
                "bridge_paper_venue": src.get("display_name"),
                "bridge_paper_type": w.get("type"),
                "bridge_paper_cites_count": w.get("cited_by_count"),
                "creativity_canonical_id": r["creativity_canonical_id"],
                "figure_group": r["figure_group"],
                "creativity_title": r["creativity_title"],
                "dd_canonical_id": r["dd_canonical_id"],
                "dd_label": r["dd_label"],
                "dd_title": r["dd_title"],
                "dd_subdomain": r["dd_subdomain"],
            })
        time.sleep(0.1)
    bp_df = pd.DataFrame(bridging)
    bp_df.to_csv(PROC / "co_citation_v3_bridging_papers.csv", index=False)
    print(f"Bridging papers: {len(bp_df)}")
    print("\nFigure groups by total co-citations (v3):")
    print(fg.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
