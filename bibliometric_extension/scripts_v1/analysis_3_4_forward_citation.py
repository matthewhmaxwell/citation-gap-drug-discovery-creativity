"""
3.4 Forward citation of canonical creativity-research works.

Uses OpenAlex group_by to get year + venue distributions without
paginating citers. For "primary-corpus overlap" we use the data
already computed in analysis 3.1 (which counts how many primary-corpus
papers cite each canonical work).
"""

import json
import time
from pathlib import Path

import pyalex
from pyalex import Works
import pandas as pd
import requests
from tqdm import tqdm

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 5

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)

OPENALEX = "https://api.openalex.org"
EMAIL = "bibliometric_extension@example.org"


def short_id(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def group_by(filter_str: str, group_field: str) -> list[dict]:
    """Use raw HTTP for group_by — pyalex doesn't expose it cleanly."""
    r = requests.get(
        f"{OPENALEX}/works",
        params={"filter": filter_str, "group_by": group_field, "per_page": 200, "mailto": EMAIL},
        timeout=60,
    )
    r.raise_for_status()
    return r.json().get("group_by", [])


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    direct = pd.read_csv(PROC / "direct_citation_per_canonical.csv")
    direct_lookup = direct.set_index("canonical_id")["corpus_citers"].to_dict()

    # Targets: canonical works with year ≤ 2021 and global cites ≥ 50
    targets = []
    for row_id, rec in canon.items():
        for w in rec["canonical_works"]:
            year = w.get("publication_year") or 0
            cc = w.get("cited_by_count") or 0
            if year and year <= 2021 and cc >= 50:
                targets.append((row_id, rec, w))
    print(f"Targets (year ≤ 2021, global cites ≥ 50): {len(targets)}")

    rows = []
    yearly: dict[str, dict] = {}

    for row_id, rec, w in tqdm(targets):
        wid_short = short_id(w["id"])
        cflt = f"cites:{wid_short}"
        try:
            yg = group_by(cflt, "publication_year")
            time.sleep(0.05)
            vg = group_by(cflt, "primary_location.source.id")
            time.sleep(0.05)
        except Exception as e:
            print(f"  [err] {wid_short}: {e}")
            continue

        years = {int(g["key"]): g["count"] for g in yg if g["key"] and g["key"].isdigit()}
        venues = {g["key_display_name"]: g["count"] for g in vg[:20] if g.get("key_display_name")}
        total = sum(years.values()) if years else None

        post_2020 = sum(v for k, v in years.items() if k >= 2020)
        post_2024 = sum(v for k, v in years.items() if k >= 2024)
        post_2025 = sum(v for k, v in years.items() if k >= 2025)

        # Primary-corpus overlap is from 3.1's output
        primary_overlap = int(direct_lookup.get(w["id"], 0))

        # Build top venue string
        top_venues = sorted(venues.items(), key=lambda kv: -kv[1])[:5]
        top_venues_str = "; ".join(f"{k}({v})" for k, v in top_venues)

        rows.append({
            "figure_row_id": row_id,
            "figure_group": rec["figure_group"],
            "individual_name": rec["individual_name"],
            "canonical_id": w["id"],
            "canonical_title": w["title"],
            "canonical_year": w["publication_year"],
            "global_cited_by_count_meta": w["cited_by_count"],
            "openalex_total_citers_via_groupby": total,
            "citers_in_primary_corpus": primary_overlap,
            "primary_share": primary_overlap / total if total else 0.0,
            "citers_post_2020": post_2020,
            "citers_post_2024": post_2024,
            "citers_post_2025": post_2025,
            "top_5_venues": top_venues_str,
        })
        yearly[w["id"]] = years

    fdf = pd.DataFrame(rows)
    fdf["n_citers_fetched"] = fdf["openalex_total_citers_via_groupby"]
    fdf.to_csv(PROC / "forward_citation_summary.csv", index=False)
    (PROC / "forward_citation_yearly.json").write_text(json.dumps(yearly, indent=2))
    print(f"\nWrote: processed/forward_citation_summary.csv ({len(fdf)})")

    print("\nTop 15 by primary-corpus citers (absolute):")
    print(fdf.sort_values("citers_in_primary_corpus", ascending=False).head(15)[
        ["figure_group","individual_name","canonical_title","canonical_year",
         "openalex_total_citers_via_groupby","citers_in_primary_corpus","primary_share"]
    ].to_string(index=False))

    print(f"\nMean primary-share across all targets: {fdf['primary_share'].mean()*100:.3f}%")
    print(f"Median primary-share: {fdf['primary_share'].median()*100:.3f}%")

    # Top by primary-share with denominator floor
    floor = fdf[fdf["openalex_total_citers_via_groupby"] >= 100]
    print(f"\nTop 15 by primary-share (≥100 total citers):")
    print(floor.sort_values("primary_share", ascending=False).head(15)[
        ["figure_group","individual_name","canonical_title","openalex_total_citers_via_groupby","citers_in_primary_corpus","primary_share"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
