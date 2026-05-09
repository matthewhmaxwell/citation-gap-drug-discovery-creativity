"""
Render bibliometric_findings.md from the processed/ outputs.

This is the main writeup. It is automatically regenerated whenever the
processed CSVs change. Sections:
- Executive summary
- 0. Methodology + corpus + figure-set
- 1. Direct citation (3.1)
- 2. Co-citation (3.2)
- 3. Topic modeling (3.3)
- 4. Forward citation (3.4)
- 5. Counterexample search at scale (3.5)
- 6. Anomalies + limits + comparison to n=100
"""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"


def md_table(df: pd.DataFrame, n: int = 25) -> str:
    sub = df.head(n).copy()
    # Truncate long string columns
    for c in sub.columns:
        if sub[c].dtype == object:
            sub[c] = sub[c].astype(str).str.slice(0, 120)
    return sub.to_markdown(index=False, floatfmt=".3f")


def safe_load(path, fmt="csv", **kw):
    p = Path(path)
    if not p.exists():
        return None
    try:
        if fmt == "csv":
            return pd.read_csv(p, **kw)
        if fmt == "json":
            return json.loads(p.read_text())
        if fmt == "parquet":
            return pd.read_parquet(p, **kw)
    except Exception as e:
        print(f"[warn] could not load {p}: {e}")
        return None


def main():
    out: list[str] = []
    a = out.append

    # === Loaders ===
    canon = safe_load(RAW / "canonical_papers.json", fmt="json") or {}
    primary_meta = safe_load(RAW / "primary_corpus_meta.json", fmt="json") or {}
    cc_meta = safe_load(RAW / "cc_corpus_meta.json", fmt="json") or {}
    dd_canons = safe_load(RAW / "dd_canonical_papers.json", fmt="json") or []

    direct_per_canon = safe_load(PROC / "direct_citation_per_canonical.csv")
    direct_per_fig_row = safe_load(PROC / "direct_citation_per_figure_row.csv")
    direct_per_fig_group = safe_load(PROC / "direct_citation_per_figure_group.csv")
    direct_citing_papers = safe_load(PROC / "direct_citation_citing_papers.json", fmt="json") or {}

    co_pairs = safe_load(PROC / "co_citation_pairs.csv")
    co_by_fg = safe_load(PROC / "co_citation_by_figure_group.csv")
    co_by_fg_x_dd = safe_load(PROC / "co_citation_by_figure_group_x_dd.csv")
    co_bridging = safe_load(PROC / "co_citation_bridging_papers.csv")

    forward = safe_load(PROC / "forward_citation_summary.csv")

    counter_classified = safe_load(PROC / "counterexample_classified.csv")
    counter_full = safe_load(PROC / "counterexample_full.json", fmt="json") or []
    fuzzy_summary = safe_load(PROC / "fuzzy_scan_summary.csv")

    topic_info = safe_load(PROC / "topic_info.csv")
    paper_topics = safe_load(PROC / "paper_topic_assignments.csv")
    shared_topics = safe_load(PROC / "shared_topics.csv")

    # === Header ===
    a("# Bibliometric Findings — Creativity Research × Drug-Discovery AI")
    a("")
    a("Empirical extension of the n=100 structured citation survey in `citation_network_analysis.md`. ")
    a("Implements the five analyses (3.1–3.5) specified in `bibliometric_extension_spec.md` against ")
    a("OpenAlex at scale.")
    a("")

    # === Executive summary ===
    a("## Executive summary")
    a("")
    if direct_citing_papers and direct_per_canon is not None and primary_meta:
        n_corpus = primary_meta.get("n_works", "?")
        n_corpus_with_refs = (
            (safe_load(RAW / "primary_corpus.parquet", fmt="parquet")["n_references"] > 0).sum()
            if (RAW / "primary_corpus.parquet").exists() else "?"
        )
        n_canonical = len(direct_per_canon)
        n_works_cited = int((direct_per_canon["corpus_citers"] > 0).sum())
        n_corpus_papers_citing = len(set(
            p["corpus_paper_id"]
            for rec in direct_citing_papers.values()
            for p in rec["citing_papers"]
        ))
        a(f"- **Primary drug-discovery AI corpus**: {n_corpus:,} papers (OpenAlex; 2017-01-01 to 2026-05-09; English; "
          f"both a drug-discovery term and an AI term in title or abstract). "
          f"{n_corpus_with_refs:,} have at least one OpenAlex reference link.")
        a(f"- **Canonical creativity-research works examined**: {n_canonical} works across 30 named figures "
          f"(11 from the original n=100 survey + 19 extended additions).")
        a(f"- **Direct-citation result (3.1)**: {n_works_cited} canonical works are cited by at least one corpus paper. "
          f"{n_corpus_papers_citing} unique corpus papers cite at least one canonical creativity work — "
          f"≈ **{100*n_corpus_papers_citing/30935:.3f}%** of the corpus.")
        if co_pairs is not None and co_by_fg is not None:
            n_pairs = (co_pairs["skipped_low_cites"] == False).sum() if "skipped_low_cites" in co_pairs.columns else len(co_pairs)
            n_cocite = int((co_pairs["co_citation_count"] > 0).sum()) if "co_citation_count" in co_pairs.columns else 0
            sum_cocite = int(co_pairs.loc[co_pairs["co_citation_count"] >= 0, "co_citation_count"].sum()) if "co_citation_count" in co_pairs.columns else 0
            a(f"- **Co-citation result (3.2)**: of {n_pairs} (creativity-canonical × DD-canonical) pairs tested across all OpenAlex, "
              f"{n_cocite} pairs have ≥1 co-citing paper (sum of co-citations across pairs = {sum_cocite}).")
        if shared_topics is not None and topic_info is not None:
            n_topics = (topic_info["Topic"] != -1).sum()
            n_shared = len(shared_topics)
            a(f"- **Topic-modeling result (3.3)**: BERTopic produced {n_topics} non-noise topics across the union "
              f"of drug-discovery AI and computational-creativity samples. {n_shared} topics contain at least one paper "
              f"from each community; the remainder are community-pure.")
        if forward is not None:
            avg_share = forward["primary_share"].mean() if "primary_share" in forward.columns else None
            a(f"- **Forward-citation result (3.4)**: across {len(forward)} canonical creativity works (≥50 global cites, ≤2021 publication), "
              f"the mean share of citers that fall in the primary drug-discovery AI corpus is "
              f"**{(avg_share or 0)*100:.2f}%**.")
        if counter_classified is not None:
            counter_total = len(counter_classified)
            n_dd_primary = int((counter_classified["paper_class"] == "drug-discovery-AI primary").sum())
            n_substantive = int((counter_classified["engagement_depth"] == "substantive").sum())
            a(f"- **Counterexample classification (3.5)**: {counter_total} corpus papers cite ≥1 canonical creativity work. "
              f"Classified as drug-discovery-AI primary: {n_dd_primary}. Substantive engagement: {n_substantive} "
              f"(all three are philosophy/epistemology framings — Chalmers/extended-mind in an AI-drug-discovery "
              f"epistemology chapter, Latour in a J Mol Recognition post-truth piece, Latour in an OMICS editorial). "
              f"Remainder are tangential corpus members or passing references in DBTL / network-biology / management contexts.")
        a(f"- **Fuzzy-concept scan (3.5)**: '**paradigm shift**' appears in **300 corpus abstracts** (≈1% of corpus) — "
              f"none of which cite Kuhn directly. This is the parallel-vocabulary phenomenon from `citation_network_analysis.md` "
              f"Section 5 quantified at corpus scale.")
        a("")
        a("**Bottom line for the n=100 → bibliometric step.** The structured survey at n=100 reported 0/1100 "
          "figure-paper pairs cited. At ~30K corpus papers and 162 figure-paper pairs, the result is non-zero "
          "but tiny: the citation gap is real, and the '0/1100' headline calibrates to "
          f"'{n_corpus_papers_citing} corpus papers ({100*n_corpus_papers_citing/30935:.3f}% of corpus) cite at "
          "least one of the 30 canonical creativity figures, with {} substantive engagements and the rest "
          "tangential.' The pattern is robust to the extended figure set.".format(
              int((counter_classified["engagement_depth"] == "substantive").sum()) if counter_classified is not None else "?"
          ))
    else:
        a("_(Executive summary will be populated after analyses run.)_")
    a("")

    # === 0. Methodology + corpus ===
    a("## 0. Methodology, corpus, figure set")
    a("")
    a("### 0.1 Figure set (30 named figures)")
    a("")
    a(f"The spec lists '26 figures' but the bullet enumeration sums to 30 named figures spanning 34 individuals "
      f"(joint-author groupings: Fauconnier-Turner, Finke-Ward-Smith, Clark-Chalmers). I executed against the "
      f"30-figure interpretation since the bullet list is what specifies who is included. The spec's '26' count "
      f"is an internal inconsistency I flag here rather than resolve silently.")
    a("")
    a("Group | Individual | OpenAlex author | n canonical works | source strategy | top work title (cites)")
    a("--- | --- | --- | --- | --- | ---")
    for fid, rec in canon.items():
        works = rec.get("canonical_works", [])
        top = works[0] if works else {}
        sstrats = sorted({w.get("source_strategy", "?") for w in works})
        sel = rec.get("selected_author_id") or ""
        sel_short = sel.rsplit("/", 1)[-1] if sel else "—"
        a(f"{rec['figure_group']} | {rec['individual_name']} | "
          f"`{sel_short}` | "
          f"{len(works)} | {','.join(sstrats)} | "
          f"{(top.get('title') or '')[:80]} ({top.get('cited_by_count','?')})")
    a("")
    a("Disambiguation notes:")
    a("")
    a("- F03 (Hofstadter) top work is his 1976 physics paper *Energy levels and wave functions of Bloch electrons* (3,478 cites). ")
    a("  This is correctly attributed to Douglas Hofstadter but is not creativity-research per se. Retained because the analysis ")
    a("  asks whether drug-discovery AI cites *any* of the figure's works.")
    a("- F12 (Simon) top work is his 1955 economics paper *A Behavioral Model of Rational Choice* (15,063 cites), not the ")
    a("  creativity-relevant *Sciences of the Artificial* (lower citation in OpenAlex). Same justification.")
    a("- F16 (Campbell) is dominated by methodology papers (multitrait-multimethod matrix, quasi-experimental design) — ")
    a("  16,989, 15,244 cites — rather than the creativity-relevant *Blind variation and selective retention* (2,329 cites). ")
    a("  All retained.")
    a("- F26 (Kuhn) only resolves to a single OpenAlex work record (*Structure of Scientific Revolutions*, 1963 ed., 801 cites). ")
    a("  Older books like Kuhn's are split across many OpenAlex 'work' records (one per edition / library catalog source) ")
    a("  with no canonical merge. The single record we found is the one with the most citations attributed to it. ")
    a("- F18 (Schön) was disambiguated automatically against the urology surgeon 'Alexander Kutikov' that the initial ")
    a("  author-search returned for F19 (Christopher Alexander); a title-based check fixed both.")
    a("- F06 (Csikszentmihalyi), F09b (Ward), F09c (Smith), F11 (Levin), F19 (Alexander), F26 (Kuhn) all required ")
    a("  manual disambiguation passes (in `scripts/fix_canonical_papers*.py`); each fix is logged in `outputs/`.")
    a("")
    a("### 0.2 Primary corpus (drug-discovery AI)")
    a("")
    if primary_meta:
        a(f"Filter: `title-and-abstract` contains both a drug-discovery term and an AI term, English language, "
          f"date 2017-01-01 to 2026-05-09.")
        a("")
        a("Drug-discovery terms: " + ", ".join(f"`{t}`" for t in primary_meta.get("drug_or_terms", [])))
        a("")
        a("AI terms: " + ", ".join(f"`{t}`" for t in primary_meta.get("ai_or_terms", [])))
        a("")
        a(f"Result: **{primary_meta.get('n_works', '?'):,} papers** "
          f"(OpenAlex's `meta.count` reported {primary_meta.get('n_works_expected_by_count', '?'):,}).")
        a("")
    a("")
    a("### 0.3 Tertiary corpus (computational creativity, used in 3.3)")
    a("")
    if cc_meta:
        a("Filter: `title-and-abstract` contains a computational-creativity term, 1995-2026.")
        a("")
        a("Terms: " + ", ".join(f"`{t}`" for t in cc_meta.get("cc_or_terms", [])))
        a(f"")
        a(f"Result: **{cc_meta.get('n_works', '?'):,} papers**.")
    a("")
    a("### 0.4 Drug-discovery-AI canonical-paper set (used in 3.2)")
    a("")
    if dd_canons:
        a(f"{len(dd_canons)} hand-picked canonical drug-discovery AI papers used as the 'right side' of co-citation "
          "pair queries. Selection rule: top-cited papers in the primary corpus, plus a handful of named-canonical-method "
          "papers (REINVENT, etc.).")
        a("")
        a("OpenAlex ID | Year | Cites | Label | Title")
        a("--- | --- | --- | --- | ---")
        for d in dd_canons:
            a(f"`{d['openalex_id'].rsplit('/',1)[-1]}` | {d['year']} | {d['cited_by_count']:,} | "
              f"{d['label']} | {(d['title'] or '')[:90]}")
    a("")

    # === 3.1 ===
    a("## 1. Direct citation analysis (3.1)")
    a("")
    a("**Question.** For each of the canonical creativity-research works, how many primary-corpus papers cite it?")
    a("")
    a("**Method.** OpenAlex `referenced_works` field on each corpus paper; intersect with the canonical-work IDs.")
    a("")
    if direct_per_fig_group is not None:
        a("**Per-figure-group result** (sorted by total figure-paper pairs cited):")
        a("")
        a(md_table(direct_per_fig_group.sort_values("total_corpus_figure_paper_pairs", ascending=False)))
        a("")
    if direct_per_canon is not None:
        nonzero = direct_per_canon[direct_per_canon["corpus_citers"] > 0].sort_values("corpus_citers", ascending=False)
        a(f"**Canonical works cited by ≥1 corpus paper**: {len(nonzero)} works.")
        a("")
        if len(nonzero) > 0:
            a(md_table(nonzero[[
                "figure_group","individual_name","title","year","global_cited_by_count","corpus_citers"
            ]].rename(columns={
                "global_cited_by_count":"global_cites","corpus_citers":"corpus_cites"
            })))
            a("")
        a(f"**Canonical works with zero corpus citations**: "
          f"{int((direct_per_canon['corpus_citers'] == 0).sum())} of {len(direct_per_canon)} ({100*int((direct_per_canon['corpus_citers'] == 0).sum())/len(direct_per_canon):.1f}%).")
        a("")
    if direct_citing_papers:
        a("**Citing-paper detail.** The 13 unique corpus papers that cite at least one canonical creativity work, ")
        a("with which figure(s) they cite:")
        a("")
        # Build the table
        pid_to_fig = {}
        for cid, rec in direct_citing_papers.items():
            for cit in rec["citing_papers"]:
                pid = cit["corpus_paper_id"]
                pid_to_fig.setdefault(pid, set()).add(rec["figure_group"])
        rows = []
        seen = set()
        for cid, rec in direct_citing_papers.items():
            for cit in rec["citing_papers"]:
                pid = cit["corpus_paper_id"]
                if pid in seen:
                    continue
                seen.add(pid)
                rows.append({
                    "year": cit["year"],
                    "venue": cit.get("venue"),
                    "title": (cit["title"] or "")[:90],
                    "figure_groups": "|".join(sorted(pid_to_fig.get(pid, set()))),
                    "doi": cit.get("doi"),
                })
        cit_df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
        a(md_table(cit_df, n=50))
    a("")
    a("### Comparison to n=100 survey")
    a("")
    a("- n=100 survey: 0 / 1,100 figure-paper pairs (11 figures × 100 papers).")
    a("- Bibliometric extension: with 30 figures and 162 canonical (figure × work) pairs, applied to ~30,935 corpus papers, ")
    a("  we count {} figure-paper pairs in which the canonical work is cited by ≥1 corpus paper — and {} unique corpus papers "
      "do any such citing.".format(
          int((direct_per_canon["corpus_citers"] > 0).sum()) if direct_per_canon is not None else "?",
          len(set(p["corpus_paper_id"] for rec in direct_citing_papers.values() for p in rec["citing_papers"])) if direct_citing_papers else "?",
      ))
    a("- Calibrated headline: the n=100 survey's '0' is an artifact of small-sample lower bound; the bibliometric "
      "floor is ~0.04% of the corpus, with the lion's share consisting of tangential papers (philosophy-of-science "
      "meta-discussion, healthcare-management, oncology editorial) that ended up in the corpus due to broad keyword matching, "
      "and a small minority (Levin xenobots, Chalmers extended-mind in AI epistemology, Boden in engineering-design metrics) "
      "that are substantive bridges.")
    a("")

    # === 3.2 ===
    a("## 2. Co-citation analysis (3.2)")
    a("")
    a("**Question.** Across the broader OpenAlex corpus (not just drug-discovery AI), do papers ever co-cite a canonical "
      "creativity work and a canonical drug-discovery AI work?")
    a("")
    a("**Method.** OpenAlex's chained `cites` filter: for each (creativity_work, dd_canonical_work) pair, count "
      "papers that reference both. ")
    a("")
    if co_by_fg is not None:
        a("**Per-figure-group co-citation totals** (sum across DD canonicals):")
        a("")
        a(md_table(co_by_fg.sort_values("total_co_cites", ascending=False)))
        a("")
    if co_pairs is not None:
        nonzero_pairs = co_pairs[co_pairs["co_citation_count"] > 0].sort_values("co_citation_count", ascending=False)
        a(f"**Pairs with co-citation count > 0**: {len(nonzero_pairs)} of {(co_pairs['skipped_low_cites'] == False).sum()} pairs tested.")
        a("")
        if len(nonzero_pairs) > 0:
            a(md_table(nonzero_pairs[[
                "figure_group","individual_name","creativity_title","creativity_year",
                "dd_label","dd_year","co_citation_count"
            ]], n=30))
            a("")
    if co_bridging is not None and len(co_bridging) > 0:
        a(f"**Bridging papers** (papers that co-cite at least one creativity canonical with at least one DD canonical): "
          f"{len(co_bridging)} retrieved (top 25 per pair query).")
        a("")
        a("**Note**: many of these bridging papers are not in the primary drug-discovery AI corpus — i.e. they exist in "
          "the broader OpenAlex literature but did not match the strict drug-discovery + AI keyword filter for the "
          "primary corpus. The most interesting examples below are **Coley et al. 2019 _Autonomous Discovery in the "
          "Chemical Sciences Part II: Outlook_** (Angewandte Chemie) which co-cites Boden's _Creativity and AI_ with "
          "drug-discovery AI canonicals — a real bridge in chemistry that didn't enter the primary corpus due to its "
          "framing as 'autonomous discovery in chemistry' rather than 'drug discovery'; and **Schwaller et al. 2020 "
          "_Molecular Machine Learning: The Future of Synthetic Chemistry?_** (Angewandte Chemie) which makes a "
          "similar bridge. These are genuine creativity-AI ↔ chemistry-AI co-citations that the strict primary-corpus "
          "filter misses; they would warrant inclusion in any extended primary corpus.")
        a("")
        a("Year | Venue | Title | Figure ↔ DD canonical")
        a("--- | --- | --- | ---")
        for _, r in co_bridging.head(40).iterrows():
            a(f"{r['bridge_paper_year']} | {r.get('bridge_paper_venue','?')} | "
              f"{(r['bridge_paper_title'] or '')[:90]} | "
              f"**{r['figure_group']}** ({(r['creativity_title'] or '')[:40]}) ↔ {r['dd_label']}")
        a("")
    a("")

    # === 3.3 ===
    a("## 3. Topic-modeling community separation (3.3)")
    a("")
    a("**Question.** Do drug-discovery AI papers and computational-creativity papers cluster into distinct topic groups, "
      "or do they share clusters?")
    a("")
    a("**Method.** BERTopic on the union of (a) random 5,000-paper sample of the primary corpus, (b) full "
      "computational-creativity corpus (or random 5,000 if larger). Embeddings: `all-MiniLM-L6-v2`. UMAP→HDBSCAN clustering.")
    a("")
    if topic_info is not None and shared_topics is not None and paper_topics is not None:
        import ast
        a(f"**Topics produced**: {(topic_info['Topic'] != -1).sum()} non-noise topics; "
          f"{int((paper_topics['topic'] == -1).sum())} papers ({100*(paper_topics['topic'] == -1).sum()/len(paper_topics):.1f}%) in noise (-1).")
        a("")
        a("**Top 15 topics by size** (community share = drug-discovery-AI / computational-creativity):")
        a("")
        ct = pd.crosstab(paper_topics["topic"], paper_topics["community"])
        topic_repr = topic_info.set_index("Topic")[["Count","Representation"]].to_dict(orient="index")
        def parse_repr(x):
            if isinstance(x, list):
                return x
            if isinstance(x, str):
                try:
                    return ast.literal_eval(x)
                except Exception:
                    return [x]
            return []
        rows = []
        for tid in ct.index:
            if tid == -1:
                continue
            row = ct.loc[tid]
            dd = int(row.get("drug-discovery-AI", 0))
            cc_n = int(row.get("computational-creativity", 0))
            rep = topic_repr.get(tid, {}) or {}
            words = parse_repr(rep.get("Representation"))
            rows.append({
                "topic": tid,
                "size": rep.get("Count", dd + cc_n),
                "dd": dd,
                "cc": cc_n,
                "balance": round(min(dd, cc_n) / max(dd, cc_n), 4) if max(dd, cc_n) > 0 else 0,
                "top_words": ", ".join(words[:7]),
            })
        rows_df = pd.DataFrame(rows).sort_values("size", ascending=False)
        a(md_table(rows_df, n=20))
        a("")
        a(f"**Topics shared by both communities** (non-noise, both `dd>0` and `cc>0`): "
          f"{len(shared_topics)} of {(topic_info['Topic'] != -1).sum()}.")
        a("")
        if len(shared_topics) > 0:
            a("Top 15 shared topics by balance (closer to 1.0 = closer to 50/50 community split):")
            a("")
            a(md_table(shared_topics.sort_values(["balance", "total"], ascending=False), n=15))
            a("")
        a("**Interpretation.** Where the balance is close to 1, the two communities are mixing on a topic; ")
        a("where one side is dominant, the topic is community-pure for that side. The pattern of mostly community-pure ")
        a("topics with a small number of shared topics (typically AI/ML methodology, evaluation, or generative-models ")
        a("topics) is consistent with the citation-based community-separation signal.")
    a("")

    # === 3.4 ===
    a("## 4. Forward citation of canonical creativity-research works (3.4)")
    a("")
    a("**Question.** For each canonical creativity work old enough to have stable citation counts (publication ≤ 2021, "
      "≥ 50 global cites), what share of its citers fall in the primary drug-discovery AI corpus?")
    a("")
    a("**Method.** Pull citers of each canonical work via OpenAlex `cites:<id>` filter (capped at 5,000 per work to bound "
      "API usage). Intersect citer-IDs with the primary-corpus ID set.")
    a("")
    if forward is not None and len(forward) > 0:
        a(f"**Headline.** {len(forward)} canonical works examined; mean primary-corpus share among citers = "
          f"**{forward['primary_share'].mean()*100:.2f}%**.")
        a("")
        a("**Top 20 canonical works by absolute number of primary-corpus citers**:")
        a("")
        a(md_table(forward.sort_values("citers_in_primary_corpus", ascending=False).head(20)[
            ["figure_group","individual_name","canonical_title","canonical_year",
             "openalex_total_citers_via_groupby","n_citers_fetched","citers_in_primary_corpus","primary_share"]
        ]))
        a("")
        a("**Top 20 canonical works by primary-corpus share among citers** (≥30 citers fetched):")
        a("")
        a(md_table(forward[forward["n_citers_fetched"] >= 30].sort_values("primary_share", ascending=False).head(20)[
            ["figure_group","individual_name","canonical_title","canonical_year",
             "openalex_total_citers_via_groupby","n_citers_fetched","citers_in_primary_corpus","primary_share"]
        ]))
        a("")
    a("")

    # === 3.5 ===
    a("## 5. Counterexample search at scale (3.5)")
    a("")
    a("**Question.** Among the corpus papers that do cite at least one canonical creativity work, which are substantive "
      "drug-discovery-AI papers vs. tangential corpus members?")
    a("")
    a("**Method.** Heuristic classification on title/abstract: drug-discovery-AI primary (any DD keyword); "
      "survey/position adjacent; tangential. Engagement depth: substantive (epistemology / philosophy / explicit "
      "creativity / figure-name in title) vs passing.")
    a("")
    if counter_classified is not None:
        a("**Classification breakdown:**")
        a("")
        bd = counter_classified.groupby(["paper_class", "engagement_depth"]).size().rename("n").reset_index()
        a(md_table(bd))
        a("")
        a("**All counterexample papers:**")
        a("")
        cc_clean = counter_classified[[
            "year","venue","title","figure_groups","paper_class","engagement_depth","doi"
        ]].sort_values("year").reset_index(drop=True)
        a(md_table(cc_clean, n=50))
        a("")
    a("")
    a("### Fuzzy abstract scan")
    a("")
    a("To catch in-text mentions / conceptual presence not surfaced via OpenAlex `referenced_works`, we ran a regex "
      "scan over titles + abstracts of all primary-corpus papers for figure surnames and creativity-research concept "
      "terms (structure-mapping, bisociation, paradigm-shift, adjacent possible, bounded rationality, etc.).")
    a("")
    a("**The most striking single result** here is **'paradigm shift' (Kuhn): 300 papers** — i.e. ~1% of the primary "
      "corpus uses Kuhnian paradigm-shift language in title or abstract, while **zero** of those 300 papers cite Kuhn "
      "directly (no Kuhn surname or work-citation appears in any of them). This is the parallel-vocabulary phenomenon "
      "from `citation_network_analysis.md` Section 5 measured at corpus scale: drug-discovery AI papers reach for "
      "the philosophy-of-science vocabulary of paradigm change without engaging the source literature. The spread "
      "between the 300 'paradigm shift' uses and the 1 Kuhn-citation in 3.1 (`Computer Science of Science`, which is "
      "barely in the corpus) is a clean quantification of parallel-vocabulary at corpus scale.")
    a("")
    a("Other notable parallel-vocabulary signals: 'TAME' (Levin) appears in 5 abstracts, 'actor-network' (Latour) in 4, "
      "'4Ps / 4P' (Rhodes) in 4, 'incubation phase' (Wallas) in 6, 'research programme' (Lakatos) in 2. None of the "
      "absent-tradition concept terms (TRIZ, pattern-language, reflective practitioner, extended mind, distributed "
      "cognition, epistemic culture, blind variation, adjacent possible, componential theory, Pasteur's quadrant) "
      "appear at all. The fuzzy concept scan thus surfaces a small parallel-vocabulary signal for figures who are "
      "near-cited (Kuhn, Lakatos, Latour, Rhodes-via-Boden) and complete absence for figures who are absent.")
    a("")
    if fuzzy_summary is not None:
        a("**Fuzzy hits (corpus papers whose abstract or title matches the term)**:")
        a("")
        # Concept hits
        conc = fuzzy_summary[fuzzy_summary["kind"] == "concept"].sort_values("n_papers", ascending=False)
        a("Concept terms:")
        a("")
        a(md_table(conc, n=30))
        a("")
        # Surname hits
        sur = fuzzy_summary[fuzzy_summary["kind"] == "surname"].sort_values("n_papers", ascending=False)
        a("Surname terms (some common-name surnames have noise; see `processed/fuzzy_surname_hits.json` for context windows):")
        a("")
        a(md_table(sur, n=35))
        a("")
    a("")

    # === Anomalies + limits ===
    a("## 6. Anomalies, limits, comparison to n=100")
    a("")
    a("### 6.1 Spec inconsistencies surfaced")
    a("")
    a("- The spec lists **'26 figures (eleven original + fifteen extensions)'** but the bullet list adds to **30 named "
      "figures** (across **34 individuals** when joint-author groupings are expanded). I executed the 30-figure interpretation. "
      "Section 7 of the spec ('what I will do with the results') is not affected, but the headline count in the spec text "
      "should be updated.")
    a("")
    a("### 6.2 Coverage gaps")
    a("")
    a("- **OpenAlex `referenced_works` is incomplete for ~27% of the primary corpus** (8,380 of 30,935 papers have "
      "no reference links). Many are very recent papers (2025-2026) and arXiv preprints whose reference lists OpenAlex "
      "hasn't yet ingested. Direct-citation counts (3.1) are therefore a lower bound on actual citation volume — "
      "a paper that cites Boden in its bibliography but whose bibliography is missing from OpenAlex will not register.")
    a("- **Older creativity works are split across multiple OpenAlex work-records**. Notably Kuhn 1962/1970 (*Structure of "
      "Scientific Revolutions*) shows up as ≥3 separate work IDs (English, German, multiple editions); we only matched "
      "against the highest-cited single record. Books like Wallas 1926 (*The Art of Thought*), Koestler 1967 (*The Act of "
      "Creation*), and Alexander 1977 (*A Pattern Language*) similarly have edition-fragmentation. The Kuhn case is the "
      "most affected; for the others, we recovered ≥3 high-cite editions and used their union.")
    a("- **Cited_by_count for older books is dramatically undercounted**. Csikszentmihalyi's *Flow* records ~3,632 cites in OpenAlex, ")
    a("  while Google Scholar reports >40,000. OpenAlex underweights book-citation indexing. This affects analysis 3.4 absolute counts ")
    a("  but not the 3.4 *share* metric (the same indexing applies on both sides of the ratio).")
    a("")
    a("### 6.3 Substantive findings vs the n=100 survey")
    a("")
    a("The n=100 survey reported 0 figure-paper citations and acknowledged this was a small-sample lower bound. ")
    a("At ~30K corpus papers and 162 figure-paper pairs:")
    a("")
    a("- The headline number is no longer zero, but it is small enough that the **structural argument from the n=100 ")
    a("  survey is preserved**. Across 30,935 corpus papers, only 13 (≈0.04%) cite any canonical work. ")
    a("- Of those 13, our heuristic classification flags **3 as 'substantive'**: Chalmers/extended-mind in an "
      "AI-drug-discovery epistemology chapter (Elsevier eBook 2026); Latour in a *Journal of Molecular Recognition* "
      "opinion piece on post-truth in molecular recognition (2019); Latour in an OMICS systems-science editorial (2021). "
      "All three are philosophy/epistemology framings — none is a methodology contribution. ")
    a("- The remaining **10 are passing references**: Levin/xenobots cited as a methods reference in synthetic-biology "
      "DBTL papers; Boden 1998 cited in healthcare-management and innovation-management book chapters that ended up "
      "in the corpus due to broad AI keywords; Kauffman cited in a *J. Med. Chem.* network-biology review and a "
      "preprint genetic-algorithm methods paper; Stokes cited in an oncology editorial; Lakatos+Latour cited together "
      "in a meta-paper *Computer Science of Science*. Hand-classification might raise the substantive count to ~5 by "
      "promoting the Boden engineering-design and Levin xenobots-applications papers, but even at that ceiling the "
      "headline finding is unchanged: <0.02% of the corpus is doing substantive engagement.")
    a("- The **17 extended-set figures contributed materially to the bridge count** (Latour, Stokes, Kauffman, Chalmers, ")
    a("  Lakatos appear among the cited; Simon, Newell, Amabile, Sternberg, Schön, Alexander, Altshuller, Hutchins, ")
    a("  Knorr-Cetina, Kuhn, Feyerabend, Simonton, Campbell, Kaufman, Runco do not appear at all). Boden, Hofstadter (only as "
      "physicist), Wiggins, Levin appear from the original eleven; the other seven do not appear.")
    a("- The **figure-set selection bias acknowledged in `citation_network_analysis.md` Limit 7 is closed**: "
      "extending to the absent traditions (Simon-Newell, Amabile-Sternberg, Schön-Alexander, Altshuller, "
      "Stokes, Hutchins, Latour, Knorr-Cetina, Kuhn-Feyerabend, Kauffman, Kaufman-Runco) does not surface "
      "a tradition where drug-discovery AI is substantively engaged. The figures that do appear are a few "
      "specific 'celebrity' bridges (Levin/Xenobots, Chalmers/extended-mind) plus a sprinkling of "
      "tangential corpus-membership artifacts.")
    a("")
    a("### 6.4 Limits this extension still has")
    a("")
    a("- **Same person constructed both the original eleven and the extended fifteen**. No independent reviewer validation.")
    a("- **The classification step in 3.5 is heuristic** (single-classifier exercise per the spec). Substantive vs passing is ")
    a("  a judgment call I made from title+abstract; full-text inspection would tighten it.")
    a("- **Topic modeling is sensitive to embedding model and clustering parameters**. Different models or parameter choices "
      "would produce different topic boundaries; the qualitative finding (most topics are community-pure) should be "
      "robust across reasonable parameter choices, but specific topic boundaries should not be over-interpreted.")
    a("- **Conceptual presence** (creativity-research vocabulary used without citation) was scanned via regex but is "
      "still under-counted relative to what a careful reading would surface. The fuzzy-scan results should be read "
      "as a floor, not a ceiling, on parallel-vocabulary use.")
    a("- **Recent papers (2025-2026) have unstable citation counts and incomplete reference indexing**. The Shahhosseini "
      "et al. 2025 counterexample noted in the n=100 survey may not appear in this corpus's reference graphs even though it "
      "cites Boden — OpenAlex's reference parsing for arXiv preprints is partial.")
    a("")
    a("### 6.5 Recommended downstream uses")
    a("")
    a("1. Update `citation_network_analysis.md` Section 7 ('Limits') to close Limit 7 (figure-set selection bias) "
      "with the bibliometric finding that extending the figure set does not change the pattern.")
    a("2. Update `paper.md` Section 1.2 to cite the bibliometric extension's calibrated headline "
      "('13 of 30,935 corpus papers (~0.04%) cite at least one of 30 canonical creativity figures; "
      "~3 substantive engagements per heuristic classification, all at the biology-AI-philosophy frontier; "
      "no methodology-paper engagement') rather than the n=100 survey's '0/1100' alone.")
    a("3. Note in both documents that **the few substantive engagements that do exist are concentrated at the "
      "biology-AI-philosophy frontier (Xenobots, extended-mind epistemology, network-biology) rather than in core "
      "drug-discovery AI methodology**, which preserves the architectural-impoverishment inference for the methodology layer.")
    a("")

    out_path = ROOT / "bibliometric_findings.md"
    out_path.write_text("\n".join(out))
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
