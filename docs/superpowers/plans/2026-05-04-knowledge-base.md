# Knowledge Base Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a queryable RMBS/ABF knowledge base from 16 scraped sources: 3 synthesized wiki pages, a categorical index, a CLAUDE.md schema section, and 3 iterative-use commits (ingest, lint, query-promote).

**Architecture:** Markdown wiki pages in `knowledge/wiki/` synthesize across raw sources in `knowledge/raw/` (not per-source summaries). `knowledge/index.md` is the entry point for any Claude Code query. CLAUDE.md documents three operations (ingest/query/lint) that a fresh Claude Code session can follow without prior context.

**Tech Stack:** Markdown, Claude Code (generation + query engine), Git

---

## Wiki Page Template

Every wiki page in `knowledge/wiki/` follows this exact structure:

```markdown
# [Title]
**Last updated:** YYYY-MM-DD
**Sources:** [comma-separated list of raw file slugs]

## Overview
2–3 sentences synthesizing the core topic across sources — what the pattern is, not what each source says.

## Key Data Points
- Quantitative facts with inline source citations like `([KBRA](../raw/09-kbra-non-qm-default-study.md))`
- Every non-obvious number must have a citation

## Key Insights
- Analytical takeaways that emerge from reading sources together
- Where sources agree, state the consensus; where they conflict or diverge, explain why
- No "Source X says..." framing — write as an analyst brief, not a reading list

## Relevant to RMBS Trading
- How this topic connects to what a Trading Analyst at Apollo monitors
- Which dashboard tabs (Mortgage Rates / Delinquency / Housing Supply / Home Price Index) this informs and why

## Sources Cited
- [NN-slug.md](../raw/NN-slug.md) — one-line description of what this source contributed
```

**Quality checklist** (run before committing any wiki page):
- [ ] Every non-obvious claim has an inline citation
- [ ] "Key Insights" reads as synthesis, not per-source summary
- [ ] Page answers all role-focused questions listed in its task
- [ ] All cited files actually exist in `knowledge/raw/`
- [ ] No "TBD", "TODO", or placeholder text

---

## Task 1: Generate `apollo-abf-platform.md`

**Files:**
- Create: `knowledge/wiki/apollo-abf-platform.md`

**Sources to read first:**
- `knowledge/raw/01-apollo-abf-strategy.md`
- `knowledge/raw/02-apollo-abc-product.md`
- `knowledge/raw/16-apollo-abf-global-strategy-2024.md`

**Questions this page must answer:**
- What is Apollo's ABF strategy and how does RMBS fit within it?
- What is Apollo's RMBS track record ($44B+ deployed, residential mortgage loans + non-agency RMBS + agency RMBS + MSR financing)?
- What is Apollo's origination capacity and what does that imply about deal flow?
- What competitive advantages does Apollo cite for private ABF vs. broadly-syndicated markets (price certainty, lender alignment, relationship simplicity)?
- What is Apollo Asset Backed Credit Company (ABC) and who leads the ABF platform?
- What does Apollo's 2024 global expansion (UK/EU, Japan, Korea) mean for the ABF business?

- [ ] **Step 1: Read all three source files**

```bash
# Read these files before writing — do NOT write from memory
# knowledge/raw/01-apollo-abf-strategy.md
# knowledge/raw/02-apollo-abc-product.md
# knowledge/raw/16-apollo-abf-global-strategy-2024.md
```

- [ ] **Step 2: Write `knowledge/wiki/apollo-abf-platform.md`**

Use the Wiki Page Template above. Set:
- Title: `Apollo Asset-Backed Finance Platform`
- Last updated: `2026-05-04`
- Sources: `01-apollo-abf-strategy.md, 02-apollo-abc-product.md, 16-apollo-abf-global-strategy-2024.md`

Key synthesis to achieve in "Key Insights":
- Connect the $44B RMBS deployment to the broader $200B+ origination capacity — what fraction is residential?
- Contrast private origination (price certainty, proprietary access) vs. broadly-syndicated market participation — why Apollo does both
- Note the bank retrenchment opportunity: Apollo's 2024 expansion is partly filling the gap left by regulated banks pulling back from structured credit
- Leadership team (Bret Leas as Global Head of ABF, Michael Paniwozik, Stuart Rothstein) signals institutional commitment to the asset class

In "Relevant to RMBS Trading": explain that the FRED dashboard indicators (30Y rate, delinquency, housing starts, HPI) are the macro inputs Apollo monitors when deciding to add or reduce RMBS exposure.

- [ ] **Step 3: Run quality checklist**

Verify every item in the Wiki Page Template quality checklist above. Fix any failures before continuing.

- [ ] **Step 4: Commit**

```bash
git add knowledge/wiki/apollo-abf-platform.md
git commit -m "docs(kb): add apollo-abf-platform wiki page"
```

---

## Task 2: Generate `non-qm-market.md`

**Files:**
- Create: `knowledge/wiki/non-qm-market.md`

**Sources to read first:**
- `knowledge/raw/09-kbra-non-qm-default-study.md`
- `knowledge/raw/10-riskspan-non-qm-securitization-market.md`
- `knowledge/raw/11-morningstar-dbrs-non-qm-q4-2022.md`

**Questions this page must answer:**
- What are the Non-QM borrower segments (self-employed, credit-blemished, investors, foreign nationals) and what products serve them?
- What does a decade of KBRA data show: 3.8% weighted average CDR, 0.03% realized losses, ~300 involuntary liquidations, 26.5% average severity?
- How do non-prime borrower profiles affect default rates (8–10% CDR vs. 3.8% overall)?
- How did vintages differ — what drove 2019–2020 performance vs. 2022–2023?
- How did Non-QM RMBS hold up in Q4 2022 (rate shock + spread widening) per Morningstar DBRS?
- What does the structural evolution of the market tell us: senior tranche resilience, sub spread widening as entry points?

- [ ] **Step 1: Read all three source files**

```bash
# Read these files before writing — do NOT write from memory
# knowledge/raw/09-kbra-non-qm-default-study.md
# knowledge/raw/10-riskspan-non-qm-securitization-market.md
# knowledge/raw/11-morningstar-dbrs-non-qm-q4-2022.md
```

- [ ] **Step 2: Write `knowledge/wiki/non-qm-market.md`**

Use the Wiki Page Template above. Set:
- Title: `Non-QM Mortgage Market: Credit Performance & Securitization`
- Last updated: `2026-05-04`
- Sources: `09-kbra-non-qm-default-study.md, 10-riskspan-non-qm-securitization-market.md, 11-morningstar-dbrs-non-qm-q4-2022.md`

Key synthesis to achieve in "Key Insights":
- The headline finding: 3.8% CDR over a decade with only 0.03% realized losses means Non-QM has delivered equity-like risk exposure with bond-like credit losses — this is the core thesis for why Apollo participates
- The KBRA and Morningstar data agree: when underwriting is sound (high FICO, lower LTV), Non-QM performs through rate cycles; the 2022 stress showed spread widening in subs but no credit impairment in seniors
- Non-prime profiles (8–10% CDR) are the main risk driver — this is a borrower selection problem, not a structural problem
- The RiskSpan market history (2015–present) frames the regulatory context: Non-QM emerged to serve borrowers excluded by post-crisis QM standards, backed by non-bank lenders funded by asset managers

In "Relevant to RMBS Trading": connect to the Delinquency dashboard tab — delinquency rate spikes in DRSFRMACBS data are an early warning for vintage-level stress in Non-QM deals.

Add cross-reference: "See also: [rmbs-market-conditions.md](./rmbs-market-conditions.md) for current delinquency rate data."

- [ ] **Step 3: Run quality checklist**

Verify every item in the Wiki Page Template quality checklist above. Fix any failures before continuing.

- [ ] **Step 4: Commit**

```bash
git add knowledge/wiki/non-qm-market.md
git commit -m "docs(kb): add non-qm-market wiki page"
```

---

## Task 3: Generate `rmbs-market-conditions.md`

**Files:**
- Create: `knowledge/wiki/rmbs-market-conditions.md`

**Sources to read first:**
- `knowledge/raw/03-sifma-mbs-statistics-2024.md`
- `knowledge/raw/04-sifma-fixed-income-quarterly-1q26.md`
- `knowledge/raw/05-sifma-fixed-income-outstanding.md`
- `knowledge/raw/06-cotality-delinquency-dec2025.md`
- `knowledge/raw/07-mba-delinquency-q4-2025.md`
- `knowledge/raw/08-ny-fed-delinquency-geography-2026.md`
- `knowledge/raw/12-freddie-mac-outlook-nov-2024.md`
- `knowledge/raw/13-freddie-mac-outlook-sep-2024.md`
- `knowledge/raw/14-federal-reserve-household-housing-2024.md`
- `knowledge/raw/15-ny-fed-housing-price-expectations-2024.md`

**Questions this page must answer:**
- What is the current MBS issuance volume ($1.6T in 2024, +21.6% YoY; YTD 2026 $540.8B through March, +30% YoY)?
- What is the agency vs. non-agency split in issuance and outstanding?
- Where do delinquency rates stand: Cotality 3.2% overall (Dec 2025, flat YoY), MBA 4.26% (Q4 2025, +28bps YoY), FHA at 11.52%?
- What is the geographic distribution of delinquency stress (NY Fed, Cotality: Texas metros, Maryland, Nevada)?
- What does the macro housing backdrop look like: existing home sales at 30-year lows, 4.3 months supply, housing starts trends, multifamily contraction?
- Where do home prices stand: FHFA +4.2% annual, Case-Shiller trajectory?
- What are household housing expectations (NY Fed 2024)?

- [ ] **Step 1: Read all ten source files**

```bash
# Read these files before writing — do NOT write from memory
# knowledge/raw/03-sifma-mbs-statistics-2024.md
# knowledge/raw/04-sifma-fixed-income-quarterly-1q26.md
# knowledge/raw/05-sifma-fixed-income-outstanding.md
# knowledge/raw/06-cotality-delinquency-dec2025.md
# knowledge/raw/07-mba-delinquency-q4-2025.md
# knowledge/raw/08-ny-fed-delinquency-geography-2026.md
# knowledge/raw/12-freddie-mac-outlook-nov-2024.md
# knowledge/raw/13-freddie-mac-outlook-sep-2024.md
# knowledge/raw/14-federal-reserve-household-housing-2024.md
# knowledge/raw/15-ny-fed-housing-price-expectations-2024.md
```

- [ ] **Step 2: Write `knowledge/wiki/rmbs-market-conditions.md`**

Use the Wiki Page Template above. Set:
- Title: `RMBS Market Conditions: Rates, Delinquency & Housing`
- Last updated: `2026-05-04`
- Sources: all 10 source slugs listed above

Structure the page with four subsections inside "Key Insights":
1. **MBS Market Volume** — issuance and trading momentum
2. **Delinquency Picture** — current rates, trends, geographic stress
3. **Housing Supply & Construction** — starts, permits, inventory
4. **Home Prices & Affordability** — HPI trajectory, affordability squeeze

Key synthesis to achieve:
- The SIFMA and Freddie Mac sources create tension: issuance is booming (+30% YoY in early 2026) while existing home sales are at 30-year lows — reconcile this by noting that agency refinance/purchase activity can still drive issuance even in a sluggish sales market
- Cotality (3.2%, flat) and MBA (4.26%, +28bps) measure different universes — explain the difference (Cotality = servicer-reported, broader; MBA = 1-4 family residential only) so a reader can use both correctly
- The FHA delinquency spike (11.52%) is the most important stress signal: FHA borrowers are lower-income, first-time buyers whose delinquency tracks labor market stress, not just rates
- Geographic divergence (Sun Belt + Texas stress vs. coastal resilience) from NY Fed/Cotality data means national averages mask regional severity

In "Relevant to RMBS Trading": explain how each of the 4 dashboard tabs (Mortgage Rates, Delinquency Rates, Housing Supply, Home Price Index) maps to the indicators discussed on this page.

Add cross-references: "See also: [non-qm-market.md](./non-qm-market.md) for how delinquency feeds into Non-QM vintage performance. See also: [apollo-abf-platform.md](./apollo-abf-platform.md) for how Apollo positions within this market environment."

- [ ] **Step 3: Run quality checklist**

Verify every item in the Wiki Page Template quality checklist above. Fix any failures before continuing.

- [ ] **Step 4: Commit**

```bash
git add knowledge/wiki/rmbs-market-conditions.md
git commit -m "docs(kb): add rmbs-market-conditions wiki page"
```

---

## Task 4: Generate `knowledge/index.md`

**Files:**
- Create: `knowledge/index.md`

**What this file does:** It is the first file a fresh Claude Code session reads when answering any RMBS/ABF domain question. It must be scannable in seconds and tell the agent which wiki page(s) to open next.

- [ ] **Step 1: Write `knowledge/index.md`**

```markdown
# Knowledge Base Index
**Last updated:** 2026-05-04

This index is the entry point for all knowledge base queries. Read this file first, then open the relevant wiki page(s). Drill into `knowledge/raw/` only when a direct quote or exact figure is needed.

## Wiki Pages

| Page | Summary | Cross-references |
|------|---------|-----------------|
| [apollo-abf-platform.md](wiki/apollo-abf-platform.md) | Apollo's ABF strategy, RMBS track record ($44B+ deployed), origination platform, leadership, global expansion | See rmbs-market-conditions.md for the macro inputs Apollo monitors |
| [non-qm-market.md](wiki/non-qm-market.md) | Non-QM securitization history, borrower segments, decade of default data (3.8% CDR, 0.03% loss), vintage analysis, 2022 rate-stress performance | See rmbs-market-conditions.md for current delinquency rates |
| [rmbs-market-conditions.md](wiki/rmbs-market-conditions.md) | Current MBS issuance ($1.6T 2024), delinquency rates (Cotality 3.2%, MBA 4.26%), housing supply, home prices, macro backdrop | See non-qm-market.md for how delinquency maps to Non-QM vintage stress |

## Raw Sources by Wiki Page

| File | Topic | Wiki Page |
|------|-------|-----------|
| [01-apollo-abf-strategy.md](raw/01-apollo-abf-strategy.md) | Apollo ABF investment approach and solutions | apollo-abf-platform.md |
| [02-apollo-abc-product.md](raw/02-apollo-abc-product.md) | Apollo Asset Backed Credit Company, leadership team | apollo-abf-platform.md |
| [03-sifma-mbs-statistics-2024.md](raw/03-sifma-mbs-statistics-2024.md) | MBS issuance, trading volumes 2024–2026 YTD | rmbs-market-conditions.md |
| [04-sifma-fixed-income-quarterly-1q26.md](raw/04-sifma-fixed-income-quarterly-1q26.md) | Fixed income market quarterly data 1Q 2026 | rmbs-market-conditions.md |
| [05-sifma-fixed-income-outstanding.md](raw/05-sifma-fixed-income-outstanding.md) | Fixed income outstanding balances | rmbs-market-conditions.md |
| [06-cotality-delinquency-dec2025.md](raw/06-cotality-delinquency-dec2025.md) | National delinquency rate Dec 2025, geographic breakdown | rmbs-market-conditions.md |
| [07-mba-delinquency-q4-2025.md](raw/07-mba-delinquency-q4-2025.md) | MBA delinquency survey Q4 2025, FHA spike | rmbs-market-conditions.md |
| [08-ny-fed-delinquency-geography-2026.md](raw/08-ny-fed-delinquency-geography-2026.md) | Geographic distribution of delinquency stress 2026 | rmbs-market-conditions.md |
| [09-kbra-non-qm-default-study.md](raw/09-kbra-non-qm-default-study.md) | Decade of Non-QM default data (475K loans, $216.7B) | non-qm-market.md |
| [10-riskspan-non-qm-securitization-market.md](raw/10-riskspan-non-qm-securitization-market.md) | Non-QM market history, borrower segments, structure | non-qm-market.md |
| [11-morningstar-dbrs-non-qm-q4-2022.md](raw/11-morningstar-dbrs-non-qm-q4-2022.md) | Non-QM RMBS performance Q4 2022 rate-shock stress test | non-qm-market.md |
| [12-freddie-mac-outlook-nov-2024.md](raw/12-freddie-mac-outlook-nov-2024.md) | Housing and mortgage market outlook Nov 2024 | rmbs-market-conditions.md |
| [13-freddie-mac-outlook-sep-2024.md](raw/13-freddie-mac-outlook-sep-2024.md) | Housing and mortgage market outlook Sep 2024 | rmbs-market-conditions.md |
| [14-federal-reserve-household-housing-2024.md](raw/14-federal-reserve-household-housing-2024.md) | Fed household housing balance sheet data 2024 | rmbs-market-conditions.md |
| [15-ny-fed-housing-price-expectations-2024.md](raw/15-ny-fed-housing-price-expectations-2024.md) | NY Fed housing price expectations survey 2024 | rmbs-market-conditions.md |
| [16-apollo-abf-global-strategy-2024.md](raw/16-apollo-abf-global-strategy-2024.md) | Apollo credit business AUM, fee growth, RMBS track record | apollo-abf-platform.md |
```

- [ ] **Step 2: Verify the index**

Check:
- [ ] Every file in `knowledge/raw/` (except `.gitkeep`) is listed in the raw sources table
- [ ] Every wiki page in `knowledge/wiki/` is listed in the Wiki Pages table
- [ ] Cross-references are accurate (match what the wiki pages say)

- [ ] **Step 3: Commit**

```bash
git add knowledge/index.md
git commit -m "docs(kb): add knowledge base index"
```

---

## Task 5: Add Knowledge Base Schema to `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

The existing `CLAUDE.md` has a "Knowledge Base Query Conventions" section at the end (lines 48–61). Replace that section with a fuller "Knowledge Base Schema" section that covers ingest, query, and lint — and that a fresh Claude Code session with zero prior context can follow.

- [ ] **Step 1: Read `CLAUDE.md`**

Read the file at `CLAUDE.md` to confirm the current content before editing.

- [ ] **Step 2: Replace the "Knowledge Base Query Conventions" section**

Replace everything from `## Knowledge Base Query Conventions` to the end of the file with:

```markdown
## Knowledge Base Schema

The knowledge base lives in `knowledge/`. It has two layers: raw scraped sources in `knowledge/raw/` and synthesized wiki pages in `knowledge/wiki/`. `knowledge/index.md` is the catalog.

### Ingest

When a new file lands in `knowledge/raw/`:
1. Read the new source file
2. Check `knowledge/index.md` to find the most relevant wiki page(s)
3. Add new facts, data points, and insights to the relevant wiki page(s) — synthesize, don't append
4. Add the new file to the Raw Sources table in `knowledge/index.md`
5. Commit with message: `docs(kb): ingest [slug]`

### Query

When asked about RMBS markets, ABF, mortgage rates, delinquency, housing, or the Apollo role:
1. Read `knowledge/index.md` first to identify which wiki page(s) are relevant
2. Open the relevant wiki page(s) in `knowledge/wiki/`
3. Drill into `knowledge/raw/` only when a direct quote or exact figure from a specific source is needed
4. Synthesize across pages — do not just recite what each page says
5. Cite sources: name the wiki page and raw file that supports each claim

### Lint

Periodically scan the wiki for quality drift:
1. **Contradictions** — does any claim on one wiki page conflict with another?
2. **Stale data** — are any figures superseded by a newer raw source that has since been ingested?
3. **Orphan pages** — is every wiki page listed in `knowledge/index.md`?
4. **Missing cross-references** — do wiki pages that discuss overlapping topics link to each other?

Fix one finding per lint run. Commit with message: `docs(kb): lint [description of fix]`
```

- [ ] **Step 3: Verify the edit**

Read `CLAUDE.md` again and confirm:
- [ ] The old "Knowledge Base Query Conventions" section is fully replaced
- [ ] All three operations (Ingest, Query, Lint) are present with numbered steps
- [ ] A fresh session reading only `CLAUDE.md` would know how to navigate the wiki

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add knowledge base schema (ingest/query/lint) to CLAUDE.md"
```

---

## Task 6: Ingest One New Source (Step 14 — Ingest)

**Files:**
- Create: `knowledge/raw/17-[slug].md` (slug chosen based on source scraped)
- Modify: `knowledge/wiki/[relevant-page].md`
- Modify: `knowledge/index.md`

This task demonstrates the Ingest operation from the CLAUDE.md schema. Use the Firecrawl MCP to scrape a new RMBS/ABF source and integrate it.

- [ ] **Step 1: Scrape a new source with Firecrawl MCP**

Use the Firecrawl MCP `firecrawl_scrape` tool to scrape one of these URLs (pick whichever returns the richest content):
- `https://www.urban.org/research/publication/housing-finance-glance-monthly-chartbook` — Urban Institute housing finance chartbook
- `https://www.fanniemae.com/research-and-insights/forecast` — Fannie Mae housing forecast
- `https://www.blackknightinc.com/data-report/mortgage-monitor/` — ICE (Black Knight) mortgage monitor

Save the result to `knowledge/raw/17-[descriptive-slug].md` following the same format as existing raw files (first line: `Source: [URL]`, then markdown content).

- [ ] **Step 2: Run the Ingest operation from CLAUDE.md**

Follow the Ingest steps in CLAUDE.md exactly:
1. Read the new source file
2. Identify which wiki page(s) it belongs to
3. Add new facts/insights to that wiki page (synthesize, don't append)
4. Update `knowledge/index.md` raw sources table

- [ ] **Step 3: Commit**

```bash
git add knowledge/raw/17-*.md knowledge/wiki/ knowledge/index.md
git commit -m "docs(kb): ingest [slug of new source]"
```

---

## Task 7: Run Lint Operation (Step 14 — Lint)

**Files:**
- Modify: one or more files in `knowledge/wiki/` and/or `knowledge/index.md`

This task demonstrates the Lint operation from the CLAUDE.md schema.

- [ ] **Step 1: Run the Lint operation**

Follow the Lint steps in CLAUDE.md. Scan all three wiki pages for:
- Contradictions between pages
- Stale data (figures contradicted by newer sources now in raw/)
- Orphan pages (not in index)
- Missing cross-references between pages

Write down at least one finding.

- [ ] **Step 2: Fix one finding**

Make the minimal edit to fix the highest-priority finding. Common fixes:
- Adding a cross-reference link between two wiki pages that discuss related topics
- Updating a stale figure if a newer raw source has a more recent number
- Adding a missing entry to `knowledge/index.md`

- [ ] **Step 3: Commit**

```bash
git add knowledge/
git commit -m "docs(kb): lint [one-line description of fix]"
```

---

## Task 8: Query-Promote (Step 14 — Query-Promote)

**Files:**
- Modify: one wiki page in `knowledge/wiki/` (expand or create)
- Modify: `knowledge/index.md` if a new page is created

This task demonstrates the Query operation and promotion of a synthesized answer back into the wiki.

- [ ] **Step 1: Ask a hard domain question**

Ask this question using the Query operation from CLAUDE.md:

> "What does my knowledge base say about the impact of rising mortgage rates on RMBS prepayment speeds and deal performance?"

Follow the query navigation: `index.md` → relevant wiki pages → raw sources for direct evidence.

- [ ] **Step 2: Evaluate the answer**

Check if the synthesized answer:
- Draws on multiple wiki pages (rates, delinquency, Non-QM performance)
- Cites specific data points
- Would be useful in an interview answer about rate sensitivity

If yes, promote it.

- [ ] **Step 3: Promote the answer**

Add a new subsection or expand an existing section in `knowledge/wiki/rmbs-market-conditions.md` (or `non-qm-market.md` if more relevant) to capture the synthesized insight permanently.

Update `knowledge/index.md` if cross-references need updating.

- [ ] **Step 4: Commit**

```bash
git add knowledge/wiki/ knowledge/index.md
git commit -m "docs(kb): promote query answer on rate sensitivity and prepayment"
```
