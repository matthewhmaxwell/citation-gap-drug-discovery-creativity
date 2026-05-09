"""
Build the v1 vs v2 comparison table that's the central deliverable.
Stand-alone so it can be regenerated independently.
"""

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
V1_RAW = ROOT.parent / "bibliometrics" / "raw"
V1_PROC = ROOT.parent / "bibliometrics" / "processed"


def main():
    v1_meta = json.loads((V1_RAW / "primary_corpus_meta.json").read_text())
    v2_meta = json.loads((RAW / "primary_corpus_v2_meta.json").read_text())
    v1_n = v1_meta["n_works"]
    v2_n = v2_meta["n_works"]

    v1_canon = pd.read_csv(V1_PROC / "direct_citation_per_canonical.csv")
    v2_canon = pd.read_csv(PROC / "direct_citation_v2_per_canonical.csv")
    v1_citing = json.loads((V1_PROC / "direct_citation_citing_papers.json").read_text())
    v2_citing = json.loads((PROC / "direct_citation_v2_citing_papers.json").read_text())
    v1_pids = set(p["corpus_paper_id"] for rec in v1_citing.values() for p in rec["citing_papers"])
    v2_pids = set(p["corpus_paper_id"] for rec in v2_citing.values() for p in rec["citing_papers"])
    v1_counter = pd.read_csv(V1_PROC / "counterexample_classified.csv")
    v2_counter = pd.read_csv(PROC / "counterexample_v2_classified.csv")
    forward_v2 = pd.read_csv(PROC / "forward_citation_v2_with_v1_compare.csv")
    fuzzy_v2 = pd.read_csv(PROC / "fuzzy_scan_v2_with_v1_compare.csv")
    shared_v2 = pd.read_csv(PROC / "shared_topics_v2.csv")
    v1_shared = pd.read_csv(V1_PROC / "shared_topics.csv")

    rows = [
        ("Corpus size", f"{v1_n:,}", f"{v2_n:,}", f"+{v2_n-v1_n:,} ({100*(v2_n-v1_n)/v1_n:.1f}%)",
         "v2 expansion much smaller than spec's 50K-150K estimate"),
        ("Direct-citation rate (corpus papers citing ≥1 canonical / corpus size)",
         f"{len(v1_pids)} ({100*len(v1_pids)/v1_n:.3f}%)",
         f"{len(v2_pids)} ({100*len(v2_pids)/v2_n:.3f}%)",
         f"+{len(v2_pids)-len(v1_pids)}",
         "citation gap survives broader corpus"),
        ("Substantive engagements (heuristic, single-classifier)",
         f"{int((v1_counter['engagement_depth']=='substantive').sum())}",
         f"{int((v2_counter['engagement_depth']=='substantive').sum())}",
         f"{int((v2_counter['engagement_depth']=='substantive').sum() - (v1_counter['engagement_depth']=='substantive').sum()):+}",
         "no new substantive engagement at methodology layer"),
        ("Chemistry-AI methodology primary class",
         "n/a (class introduced in v2)",
         f"{int((v2_counter['paper_class']=='chemistry-AI methodology primary').sum())}",
         f"+{int((v2_counter['paper_class']=='chemistry-AI methodology primary').sum())}",
         "Schwaller 2020 only; passing engagement"),
        ("Figures with non-zero corpus citations (of 30)",
         f"{(v1_canon.groupby('figure_group')['corpus_citers'].sum() > 0).sum()}",
         f"{(v2_canon.groupby('figure_group')['v2_corpus_citers'].sum() > 0).sum()}",
         f"+{(v2_canon.groupby('figure_group')['v2_corpus_citers'].sum() > 0).sum() - (v1_canon.groupby('figure_group')['corpus_citers'].sum() > 0).sum()}",
         "Alexander newly appears in v2 (1 citing paper); rest unchanged"),
        ("Mean forward-citation share among canonical creativity-work citers",
         f"{forward_v2['v1_share'].mean()*100:.4f}%",
         f"{forward_v2['v2_share'].mean()*100:.4f}%",
         f"{(forward_v2['v2_share']-forward_v2['v1_share']).mean()*100:+.4f}%",
         "negligible delta"),
        ("Fuzzy 'paradigm shift' (Kuhn) abstract hits",
         f"{int(fuzzy_v2[fuzzy_v2['label']=='paradigm shift (Kuhn)']['n_papers_v1'].iloc[0])} (0 cite Kuhn)",
         f"{int(fuzzy_v2[fuzzy_v2['label']=='paradigm shift (Kuhn)']['n_papers_v2'].iloc[0])} (0 cite Kuhn)",
         f"{int(fuzzy_v2[fuzzy_v2['label']=='paradigm shift (Kuhn)']['delta'].iloc[0]):+}",
         "parallel-vocabulary pattern reproduces"),
        ("Coley 2019 Part II (Outlook) in primary corpus", "No", "**No** (still excluded)", "—",
         "boundary leakage on this paper not closed"),
        ("Schwaller 2020 (Molecular ML) in primary corpus", "No", "**Yes**", "added",
         "one v1-bridging paper now in corpus"),
        ("Coscientist (Boiko 2023) in primary corpus", "No", "**No**", "—",
         "abstract framing 'autonomous chemical research' didn't match"),
        ("Burger 2020 (mobile robotic chemist) in primary corpus", "No", "**No**", "—",
         "no v2-term in title or abstract"),
        ("Topic-modeling community max balance",
         f"{v1_shared['balance'].max() if len(v1_shared)>0 else 0:.3f}",
         f"{shared_v2['balance'].max() if len(shared_v2)>0 else 0:.3f}",
         f"{(shared_v2['balance'].max() if len(shared_v2)>0 else 0) - (v1_shared['balance'].max() if len(v1_shared)>0 else 0):+.3f}",
         "community separation reproduces (no shared topic with balance ≥ 0.1 in either run)"),
    ]

    df = pd.DataFrame(rows, columns=["Metric", "v1 (strict drug-discovery)", "v2 (broader chemistry-AI methodology)", "Change", "Implication"])
    df.to_csv(PROC / "v1_vs_v2_comparison.csv", index=False)
    print(df.to_markdown(index=False))


if __name__ == "__main__":
    main()
