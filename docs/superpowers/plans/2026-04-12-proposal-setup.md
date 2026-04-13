# Proposal Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete all Proposal deliverables (due Apr 13): `docs/job-posting.pdf`, `docs/proposal.pdf`, `CLAUDE.md`, proper directory structure, and updated `.gitignore`.

**Architecture:** Pure repo setup — no application code. Rename the existing job posting PDF, write proposal content in markdown, generate a PDF using `fpdf2` (pure Python, no system dependencies), create `CLAUDE.md` with project context, and scaffold the directory structure for Milestone 01.

**Tech Stack:** Python (`fpdf2`), Git, Anaconda venv at `.venv/`

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Rename | `docs/job-postings.pdf` → `docs/job-posting.pdf` | Match required filename |
| Create | `docs/proposal_content.md` | Source content for proposal (human-readable) |
| Create | `scripts/generate_proposal_pdf.py` | Converts proposal content to `docs/proposal.pdf` |
| Create | `docs/proposal.pdf` | Final 1-page proposal PDF (generated) |
| Modify | `.gitignore` | Add dbt, Snowflake, and secrets entries |
| Create | `CLAUDE.md` | Project context for Claude Code |
| Create | `knowledge/raw/.gitkeep` | Scaffold knowledge base folder |
| Create | `knowledge/wiki/.gitkeep` | Scaffold knowledge base folder |
| Create | `knowledge/index.md` | Stub index for knowledge base |
| Create | `pipeline/.gitkeep` | Scaffold pipeline folder |
| Create | `dbt/.gitkeep` | Scaffold dbt folder |
| Create | `dashboard/.gitkeep` | Scaffold dashboard folder |

---

## Task 1: Update .gitignore

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add dbt, Snowflake, and secrets entries to `.gitignore`**

Open `.gitignore` and append the following block at the end (after the existing content):

```
# Secrets and credentials
.env
*.env
snowflake_credentials.json

# dbt
dbt/profiles.yml
dbt/target/
dbt/dbt_packages/
dbt/logs/

# Snowflake
.snowflake/

# Generated files
docs/proposal_content.md
scripts/
```

- [ ] **Step 2: Verify .gitignore change**

Run:
```bash
git status
```
Expected: `.gitignore` shows as modified. No `.env` files should appear as untracked.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add dbt, Snowflake, and secrets entries to .gitignore"
```

---

## Task 2: Create CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Create CLAUDE.md with project context**

Create `CLAUDE.md` at the repo root with this exact content:

```markdown
# CLAUDE.md — Trading Analyst Fintech Project

This file provides context to Claude Code when working in this repository.

## Project Overview

**Project:** RMBS Market Intelligence Dashboard  
**Target Role:** Trading Analyst, Asset-Backed Finance (Apollo Global Management)  
**Repo:** `trading-analyst-fintech`

An end-to-end analytics pipeline tracking RMBS market indicators — mortgage rates, delinquency rates, housing starts, and home price indices — sourced from the Federal Reserve FRED API, transformed via dbt in Snowflake, and surfaced through a Streamlit dashboard.

## Tech Stack

| Layer | Tool |
|-------|------|
| Data Warehouse | Snowflake (AWS US East 1) |
| Transformation | dbt |
| Orchestration | GitHub Actions (weekly schedule) |
| Dashboard | Streamlit (deployed to Community Cloud) |
| API Source | FRED (Federal Reserve Economic Data) |
| Web Scrape | Firecrawl |
| Knowledge Base | Claude Code |

## Directory Structure

    trading-analyst-fintech/
    ├── pipeline/          # Python extraction scripts (FRED API → Snowflake)
    ├── dbt/               # dbt project (staging + mart models)
    ├── dashboard/         # Streamlit app
    ├── knowledge/
    │   ├── raw/           # Scraped source documents (15+ files)
    │   ├── wiki/          # Claude Code-generated synthesis pages
    │   └── index.md       # Index of all wiki pages
    └── docs/              # Proposals, specs, plans, job posting

## Credentials

All credentials in `.env` (never committed). Required environment variables:
- `FRED_API_KEY` — from fred.stlouisfed.org/docs/api/api_key.html
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_SCHEMA`

## Knowledge Base Query Conventions

When answering questions about the RMBS market using this knowledge base:
1. Start by reading `knowledge/index.md` to find relevant wiki pages
2. Read the relevant wiki pages in `knowledge/wiki/`
3. If more detail is needed, read the raw sources in `knowledge/raw/` cited in the wiki page
4. Synthesize across sources — do not just summarize individual documents
5. Cite which wiki pages and raw sources informed the answer

Example queries this knowledge base can answer:
- "What does my knowledge base say about Non-QM loan performance trends?"
- "What is Apollo's stated strategy for the ABF platform?"
- "What does my knowledge base say about the current rate environment's impact on RMBS?"
```

- [ ] **Step 2: Verify CLAUDE.md exists**

```bash
ls CLAUDE.md
```
Expected: file listed.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project context and knowledge base query conventions"
```

---

## Task 3: Scaffold Directory Structure

**Files:**
- Create: `knowledge/raw/.gitkeep`
- Create: `knowledge/wiki/.gitkeep`
- Create: `knowledge/index.md`
- Create: `pipeline/.gitkeep`
- Create: `dbt/.gitkeep`
- Create: `dashboard/.gitkeep`

- [ ] **Step 1: Create all directories and placeholder files**

```bash
mkdir -p knowledge/raw knowledge/wiki pipeline dbt dashboard
touch knowledge/raw/.gitkeep knowledge/wiki/.gitkeep pipeline/.gitkeep dbt/.gitkeep dashboard/.gitkeep
```

- [ ] **Step 2: Create knowledge/index.md stub**

Create `knowledge/index.md` with this content:

```markdown
# Knowledge Base Index

This index lists all wiki pages in `knowledge/wiki/`. Updated as new sources are ingested.

## Wiki Pages

| Page | Summary |
|------|---------|
| (populated during Milestone 02) | |

## Raw Sources

Raw scraped documents are in `knowledge/raw/`. See individual wiki pages for citations.
```

- [ ] **Step 3: Verify structure**

```bash
find knowledge pipeline dbt dashboard -type f
```
Expected output:
```
dashboard/.gitkeep
dbt/.gitkeep
knowledge/index.md
knowledge/raw/.gitkeep
knowledge/wiki/.gitkeep
pipeline/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add knowledge/ pipeline/ dbt/ dashboard/
git commit -m "chore: scaffold project directory structure"
```

---

## Task 4: Rename Job Posting PDF

**Files:**
- Rename: `docs/job-postings.pdf` → `docs/job-posting.pdf`

- [ ] **Step 1: Rename the file using git mv**

```bash
git mv docs/job-postings.pdf docs/job-posting.pdf
```

- [ ] **Step 2: Verify rename**

```bash
git status
```
Expected:
```
Changes to be committed:
  renamed:    docs/job-postings.pdf -> docs/job-posting.pdf
```

- [ ] **Step 3: Commit**

```bash
git commit -m "docs: rename job-postings.pdf to job-posting.pdf per project requirements"
```

---

## Task 5: Write Proposal Content

**Files:**
- Create: `docs/proposal_content.md`

- [ ] **Step 1: Create proposal_content.md**

Create `docs/proposal_content.md` with this content (this is the source for the PDF — edit the reflection if needed before generating the PDF):

```markdown
# Project Proposal: RMBS Market Intelligence Dashboard

**Student:** Chelsea  
**Course:** ISBA 4715 — Analytics Engineering  
**Date:** April 13, 2026  
**GitHub Repo:** [trading-analyst-fintech](https://github.com/[your-username]/trading-analyst-fintech)

---

## Job Posting

**Role:** Trading Analyst, Asset-Backed Finance  
**Company:** Apollo Global Management  
**Location:** El Segundo, CA  
**Source:** Indeed.com (saved as `docs/job-posting.pdf`)

---

## Reflection

This Trading Analyst role at Apollo Asset-Backed Finance requires the quantitative and analytical skills built throughout this course. The posting explicitly lists SQL as a desirable skill alongside demonstrated analytical, problem-solving, and financial modeling abilities — all of which map directly to coursework in dimensional modeling, dbt transformations, and Snowflake-based analytics pipelines. This project builds an end-to-end RMBS Market Intelligence Dashboard: a pipeline that extracts Federal Reserve economic data (mortgage rates, delinquency rates by loan type, housing starts, and home price indices) via the FRED API, transforms it through raw, staging, and mart layers using dbt in Snowflake, and surfaces market insights through a deployed Streamlit dashboard. A knowledge base synthesizes research from Apollo's investor communications, SIFMA market reports, and housing finance research to support the investment screening and ad-hoc reporting described in the posting. The skills demonstrated — SQL, pipeline engineering, dimensional modeling, dashboarding, and domain research — transfer directly to the Trading Analyst role and to similar quantitative analyst positions across fixed income, structured credit, and asset management.

---

## Project Summary

**Pipeline:** FRED API (Python) → Snowflake raw → dbt staging → dbt mart (star schema) → Streamlit dashboard  
**Knowledge Base:** Firecrawl scrape (Apollo, SIFMA, Urban Institute, MBA, Fed) → `knowledge/raw/` → Claude Code → `knowledge/wiki/`  
**Orchestration:** GitHub Actions (weekly schedule)

**Star Schema:**
- `fact_market_metrics` — one row per metric per time period
- `dim_time` — date, year, quarter, month
- `dim_metric_type` — metric name, category (rates/credit/housing/macro), unit
- `dim_geography` — national baseline, expandable to regional

**Dashboard Questions:**
- Descriptive: What is the current state of the RMBS market?
- Diagnostic: Which macroeconomic conditions drive changes in delinquency rates?
```

- [ ] **Step 2: Verify file created**

```bash
ls docs/proposal_content.md
```
Expected: file listed.

Note: `proposal_content.md` is in `.gitignore` — it's a working file, not committed. Only `proposal.pdf` is committed.

---

## Task 6: Generate proposal.pdf

**Files:**
- Create: `scripts/generate_proposal_pdf.py`
- Create: `docs/proposal.pdf` (generated output)

- [ ] **Step 1: Install fpdf2**

```bash
.venv/Scripts/pip install fpdf2
```
Expected: `Successfully installed fpdf2-...`

- [ ] **Step 2: Create the PDF generation script**

Create `scripts/generate_proposal_pdf.py`:

```python
from fpdf import FPDF

class ProposalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "ISBA 4715 — Analytics Engineering | Project Proposal", align="L")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "trading-analyst-fintech | github.com", align="C")


def build_proposal():
    pdf = ProposalPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "RMBS Market Intelligence Dashboard", align="L")
    pdf.ln(6)

    # Subtitle row
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, "Trading Analyst, Asset-Backed Finance  |  Apollo Global Management  |  April 13, 2026", align="L")
    pdf.ln(10)

    # Divider
    pdf.set_draw_color(40, 40, 40)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)

    # Section: Job Posting
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 7, "Job Posting", align="L")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6,
        "Role: Trading Analyst, Asset-Backed Finance\n"
        "Company: Apollo Global Management  |  Location: El Segundo, CA\n"
        "Source: Indeed.com (saved as docs/job-posting.pdf)"
    )
    pdf.ln(6)

    # Section: Reflection
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 7, "Reflection", align="L")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    reflection = (
        "This Trading Analyst role at Apollo Asset-Backed Finance requires the quantitative and analytical "
        "skills built throughout this course. The posting explicitly lists SQL as a desirable skill alongside "
        "demonstrated analytical, problem-solving, and financial modeling abilities — all of which map directly "
        "to coursework in dimensional modeling, dbt transformations, and Snowflake-based analytics pipelines. "
        "This project builds an end-to-end RMBS Market Intelligence Dashboard: a pipeline that extracts Federal "
        "Reserve economic data (mortgage rates, delinquency rates by loan type, housing starts, and home price "
        "indices) via the FRED API, transforms it through raw, staging, and mart layers using dbt in Snowflake, "
        "and surfaces market insights through a deployed Streamlit dashboard. A knowledge base synthesizes "
        "research from Apollo's investor communications, SIFMA market reports, and housing finance research to "
        "support the investment screening and ad-hoc reporting described in the posting. The skills demonstrated "
        "— SQL, pipeline engineering, dimensional modeling, dashboarding, and domain research — transfer directly "
        "to the Trading Analyst role and to similar quantitative analyst positions across fixed income, structured "
        "credit, and asset management."
    )
    pdf.multi_cell(0, 6, reflection)
    pdf.ln(6)

    # Section: Project Summary
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 7, "Project Summary", align="L")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)

    # Pipeline line
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Pipeline:", align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6,
        "FRED API (Python) \u2192 Snowflake raw \u2192 dbt staging \u2192 dbt mart (star schema) \u2192 Streamlit dashboard"
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Knowledge:", align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6,
        "Firecrawl scrape (Apollo, SIFMA, Urban Institute, MBA, Fed) \u2192 knowledge/raw/ \u2192 Claude Code \u2192 knowledge/wiki/"
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Schema:", align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6,
        "fact_market_metrics + dim_time + dim_metric_type + dim_geography"
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 6, "Dashboard:", align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6,
        "Descriptive: current RMBS market snapshot  |  Diagnostic: delinquency rate drivers"
    )

    pdf.ln(6)

    # Section: Transferability
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 7, "Transferability", align="L")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6,
        "This project transfers to: Fixed Income Analyst, Credit Analyst, BI Analyst at mortgage companies "
        "or banks, Structured Products Analyst. The FRED API pipeline and dbt star schema pattern applies "
        "to any role requiring financial time-series analytics."
    )

    pdf.output("docs/proposal.pdf")
    print("Generated: docs/proposal.pdf")


if __name__ == "__main__":
    build_proposal()
```

- [ ] **Step 3: Run the script to generate the PDF**

```bash
cd "C:/Users/chels/isba-4715/Trading-Analyst"
.venv/Scripts/python.exe scripts/generate_proposal_pdf.py
```
Expected output:
```
Generated: docs/proposal.pdf
```

- [ ] **Step 4: Verify the PDF exists and is non-empty**

```bash
ls -lh docs/proposal.pdf
```
Expected: file exists, size > 10KB.

Open `docs/proposal.pdf` in a PDF viewer and confirm:
- Title: "RMBS Market Intelligence Dashboard"
- Reflection paragraph is present and fits on one page
- Footer shows repo name

- [ ] **Step 5: Commit proposal.pdf**

```bash
git add docs/proposal.pdf
git commit -m "docs: add proposal.pdf for project proposal submission"
```

---

## Task 7: Final Verification & Commit

- [ ] **Step 1: Verify all required files are present**

```bash
ls docs/
```
Expected to include: `job-posting.pdf`, `proposal.pdf`, `project-requirements-README.md`, `superpowers/`

```bash
ls CLAUDE.md knowledge/ pipeline/ dbt/ dashboard/
```
Expected: all directories and CLAUDE.md exist.

- [ ] **Step 2: Verify nothing sensitive is tracked**

```bash
git status
```
Expected: working tree clean. No `.env`, no `profiles.yml`, no `*.credentials` files showing as untracked.

- [ ] **Step 3: Verify commit history is clean**

```bash
git log --oneline
```
Expected: 5-6 commits covering each task above, with meaningful messages.

- [ ] **Step 4: Push to GitHub**

```bash
git push origin main
```

- [ ] **Step 5: Confirm public repo is accessible**

Open your GitHub repo URL in a browser and verify:
- Repo is public
- `docs/proposal.pdf` is visible
- `CLAUDE.md` is visible at root
- Directory structure (knowledge/, pipeline/, dbt/, dashboard/) is visible

---

## Checklist Against Proposal Requirements

| Requirement | Deliverable | Status |
|-------------|-------------|--------|
| Job posting PDF | `docs/job-posting.pdf` | Task 4 |
| Proposal PDF with reflection | `docs/proposal.pdf` | Tasks 5–6 |
| Public repo initialized | GitHub + git push | Task 7 |
| Professional repo name | `trading-analyst-fintech` | (already named) |
| Proper `.gitignore` | dbt/Snowflake/secrets entries | Task 1 |
| Directory structure | knowledge/, pipeline/, dbt/, dashboard/ | Task 3 |
| `CLAUDE.md` with project context | `CLAUDE.md` | Task 2 |
