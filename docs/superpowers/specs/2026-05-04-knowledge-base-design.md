# Knowledge Base Wiki Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a queryable wiki from 16 scraped RMBS/ABF sources that prepares for interview questions about the Trading Analyst, Asset-Backed Finance role at Apollo Global Management, and informs the analytical decisions in the Streamlit dashboard.

**Architecture:** Three synthesized wiki pages in `knowledge/wiki/`, one index in `knowledge/index.md`, and a CLAUDE.md schema section governing ingest/query/lint. Wiki pages synthesize across sources — not summaries — and map directly to hiring-manager question categories.

**Tech Stack:** Markdown, Claude Code (generation + query engine), Firecrawl MCP (future ingestion)

---

## File Structure

```
knowledge/
├── index.md                        ← categorical catalog, raw-source → wiki map
└── wiki/
    ├── apollo-abf-platform.md      ← sources 01, 02, 16
    ├── non-qm-market.md            ← sources 09, 10, 11
    └── rmbs-market-conditions.md   ← sources 03-08, 12-15
```

Each wiki page uses this template:

```markdown
# [Title]
**Last updated:** YYYY-MM-DD
**Sources:** [list raw file slugs]

## Overview
2–3 sentence synthesis of the topic

## Key Data Points
Quantitative facts with inline source citations

## Key Insights
Analytical takeaways synthesized across sources — not per-source summaries

## Relevant to RMBS Trading
How this topic connects to the dashboard metrics and the trading analyst role

## Sources Cited
- [NN-slug.md](../raw/NN-slug.md)
```

Sourcing convention: every non-obvious claim includes an inline citation like `([KBRA](../raw/09-kbra-non-qm-default-study.md))`.

---

## Wiki Page Outlines

### Page 1: `apollo-abf-platform.md`
**Sources:** 01-apollo-abf-strategy.md, 02-apollo-abc-product.md, 16-apollo-abf-global-strategy-2024.md

**Role-focused questions it answers:**
- What is Apollo's ABF strategy and why does RMBS fit within it?
- How does Apollo source, structure, and deploy capital in residential mortgage markets?
- What is Apollo's scale in RMBS ($44B+ deployed, $200B+ origination capacity)?
- What competitive advantages does Apollo cite for private ABF vs. broadly-syndicated markets?

**Hiring-manager questions it prepares for:**
- "Why Apollo specifically?" / "What do you know about our ABF platform?"
- "How does private credit relate to securitized products at Apollo?"
- "What's the difference between agency RMBS, non-agency RMBS, and MSR financing?"

**Dashboard connection:** Frames why we track RMBS market indicators — these are the exact inputs Apollo monitors when sizing and timing residential mortgage capital deployment.

---

### Page 2: `non-qm-market.md`
**Sources:** 09-kbra-non-qm-default-study.md, 10-riskspan-non-qm-securitization-market.md, 11-morningstar-dbrs-non-qm-q4-2022.md

**Role-focused questions it answers:**
- What are Non-QM borrower profiles and how do they differ from agency-eligible loans?
- What does a decade of default data show about Non-QM credit risk (3.8% CDR, 0.03% realized loss)?
- How has Non-QM securitization evolved since 2015 and who dominates origination?
- What drives loss severity, and how do vintages and credit profiles interact?

**Hiring-manager questions it prepares for:**
- "Walk me through Non-QM credit performance" / "How does Non-QM differ from prime?"
- "What drives loss severity in residential securitizations?"
- "How did Non-QM perform through COVID vs. 2022 rate shock?"

**Dashboard connection:** Non-QM performance correlates directly with the Delinquency tab — explains why delinquency spikes in certain vintages and geographies visible in DRSFRMACBS data.

---

### Page 3: `rmbs-market-conditions.md`
**Sources:** 03-sifma-mbs-statistics-2024.md, 04-sifma-fixed-income-quarterly-1q26.md, 05-sifma-fixed-income-outstanding.md, 06-cotality-delinquency-dec2025.md, 07-mba-delinquency-q4-2025.md, 08-ny-fed-delinquency-geography-2026.md, 12-freddie-mac-outlook-nov-2024.md, 13-freddie-mac-outlook-sep-2024.md, 14-federal-reserve-household-housing-2024.md, 15-ny-fed-housing-price-expectations-2024.md

**Role-focused questions it answers:**
- What is the current MBS issuance and trading volume environment ($1.6T in 2024, +21.6% YoY)?
- Where are delinquency rates today and what is the geographic dispersion?
- What is the macro backdrop for housing: rates, starts, home prices, affordability?
- Where do housing price expectations and household balance sheets stand?

**Hiring-manager questions it prepares for:**
- "What's happening in the mortgage market right now?"
- "How does the rate environment affect RMBS valuations and prepayment speeds?"
- "What housing indicators do you watch and why?"
- "What's the risk to residential mortgage credit in the current environment?"

**Dashboard connection:** Directly supports all 4 dashboard tabs (Mortgage Rates, Delinquency, Housing Supply, Home Price Index) — this is the live market context for every chart in the Streamlit dashboard.

---

## `knowledge/index.md` Structure

Two sections:

1. **Wiki Pages** — one-line summary per page with cross-references between pages
2. **Raw Sources Table** — columns: File | Topic | Wiki Page | Notes

The index is the first file a fresh Claude Code session reads before answering any domain question.

---

## CLAUDE.md Knowledge Base Schema

Three operations to add to `CLAUDE.md`:

**Ingest:** When a new source lands in `knowledge/raw/`, read it, summarize new facts into the relevant wiki page(s), update `knowledge/index.md` raw sources table, and commit with message `docs(kb): ingest [slug]`.

**Query:** When asked about RMBS, ABF, mortgage markets, or the Apollo role — read `knowledge/index.md` first, open the relevant wiki page(s), drill into `knowledge/raw/` only when a direct quote or exact figure is needed. Cite sources for every non-obvious claim.

**Lint:** Periodically scan wiki pages for: contradictions across pages, stale data (dates superseded by newer raw sources), orphan pages (not referenced in index.md), and missing cross-references between wiki pages. Fix one finding per lint run and commit.

---

## Iterative Use Tasks (Step 14)

After wiki pages are generated, three operations demonstrate the wiki is alive:

1. **Ingest** — scrape one new source via Firecrawl, run Ingest operation, commit
2. **Lint** — run Lint operation, fix one finding, commit
3. **Query-promote** — ask a hard domain question, promote the synthesized answer into a wiki page or expansion, update index.md, commit

These three commits satisfy the M02 rubric requirement for "evidence of iterative use, visible in commit history."
