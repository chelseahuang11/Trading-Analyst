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
