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
- `FRED_API_KEY` — register at fred.stlouisfed.org/docs/api/api_key.html
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_SCHEMA`

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
