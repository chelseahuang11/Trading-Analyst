# Project Proposal Design: RMBS Market Intelligence Dashboard

**Date:** 2026-04-12
**Target Role:** Trading Analyst, Asset-Backed Finance (Apollo Global Management)
**Repo Name:** `trading-analyst-fintech`

---

## 1. Project Framing

**Project title:** RMBS Market Intelligence Dashboard

**One-line pitch:** An end-to-end analytics pipeline tracking the key indicators an Asset-Backed Finance trading desk monitors — mortgage rates, origination volumes, delinquency rates, and housing market conditions — sourced from the Federal Reserve and synthesized into a Streamlit dashboard.

**Transferability:** Ports directly to fixed income analyst, credit analyst, BI analyst at mortgage companies/banks, and structured products analyst roles at any firm that needs quantitative analytics on mortgage markets.

**Reflection paragraph angle:** The Apollo posting lists SQL and quantitative analytics as core requirements. This project demonstrates both — building a SQL-backed star schema in Snowflake, writing dbt models to transform Federal Reserve economic data, and surfacing RMBS market intelligence through a deployed dashboard. It maps directly to the "support ad-hoc analysis and reporting to facilitate investment decision-making" responsibility in the posting.

---

## 2. Data Sources & Pipeline Architecture

### Source 1 — API: FRED (Federal Reserve Economic Data)

Free, well-documented API via the `fredapi` Python library. Pulls ~8-10 time series weekly via GitHub Actions into Snowflake raw schema.

| FRED Series | Metric |
|-------------|--------|
| MORTGAGE30US | 30-year fixed mortgage rate |
| DQYR30 | Delinquency rate on residential mortgages |
| HOUST | Housing starts |
| CSUSHPINSA | Case-Shiller home price index |
| UNRATE | Unemployment rate |
| FEDFUNDS | Federal funds rate |
| MDSP | Mortgage debt service payments |
| RRVRUSQ156N | Rental vacancy rate |

### Source 2 — Web Scrape: RMBS/ABS Market Content

Scraped from 3+ sources using Firecrawl, loaded to `knowledge/raw/`, scheduled via GitHub Actions.

- Apollo Global Management — investor letters, press releases, ABF strategy pages
- SIFMA — ABS/MBS market research reports, annual fact books
- Urban Institute — housing finance research papers
- Mortgage Bankers Association — market forecasts, delinquency surveys
- Federal Reserve — working papers on residential mortgage markets

---

## 3. Star Schema & dbt Models

### Tables

**`fact_market_metrics`**
- `metric_id` (PK)
- `time_id` (FK → dim_time)
- `metric_type_id` (FK → dim_metric_type)
- `value`
- `period_over_period_change` (calculated in dbt)

**`dim_time`**
- `time_id` (PK)
- `date`, `year`, `quarter`, `month`, `week`

**`dim_metric_type`**
- `metric_type_id` (PK)
- `metric_name`
- `category` (rates / credit / housing / macro)
- `unit` (percent / index / thousands)
- `fred_series_id`

**`dim_geography`**
- `geo_id` (PK)
- `level` (national / regional)
- `region_name`

Note: Initial FRED series are national-level. `dim_geography` defaults to a single "US National" row. Regional series (e.g., Case-Shiller city indices) can be added in a later milestone without schema changes.

### dbt Layers

- `stg_fred_metrics` — clean column names, cast types, handle nulls
- `fact_market_metrics` — join staging to dimensions, calculate period-over-period change
- `dim_time`, `dim_metric_type`, `dim_geography` — dimension tables

### dbt Tests

- not-null and unique on all PKs
- accepted-values on `category`
- relationships between fact and dimension tables

---

## 4. Streamlit Dashboard

Deployed to Streamlit Community Cloud, connected to Snowflake mart tables.

### Descriptive View — "What is the current RMBS market environment?"
- Time-series charts of mortgage rates, delinquency rates, housing starts over a selectable date range
- Snapshot card row: current values vs. 1-year ago for each key metric

### Diagnostic View — "What's driving delinquency rates?"
- Overlaid line chart: delinquency rate vs. unemployment rate and Fed funds rate
- Scatter plot: home price growth vs. delinquency rate by quarter

### Interactive Elements
- Date range selector
- Metric category filter (rates / credit / housing / macro)
- Tabs separating descriptive and diagnostic views

---

## 5. Knowledge Base

### Raw Sources (`knowledge/raw/` — 15+ files from 3+ sites)

- Apollo Global Management: investor letters, press releases, ABF strategy pages
- SIFMA: ABS/MBS market research reports, annual fact books
- Urban Institute: housing finance research papers
- Mortgage Bankers Association: market forecasts, delinquency surveys
- Federal Reserve: working papers on residential mortgage markets

### Wiki Pages (`knowledge/wiki/`)

1. `overview.md` — US RMBS market structure, key loan types (Non-QM, Prime Jumbo, Agency, Re-Performing)
2. `key-entities.md` — Apollo ABF strategy, major market participants, originators, servicers, rating agencies
3. `market-themes.md` — Current themes: rate environment, credit quality trends, Non-QM growth, affordability stress
4. `synthesis.md` — Cross-source synthesis: where is risk forming in the RMBS market?

### Index & Conventions

- `knowledge/index.md` — lists all wiki pages with one-line summaries
- `CLAUDE.md` includes a section explaining how to query the knowledge base

---

## 6. Proposal Artifacts

### Files to create/rename
- `docs/job-posting.pdf` — rename from `docs/job-postings.pdf`
- `docs/proposal.pdf` — 1-page proposal exported from markdown via pandoc or weasyprint

### Proposal content
- Job posting reference: Apollo Trading Analyst, Asset-Backed Finance
- One-paragraph reflection linking Apollo requirements (SQL, quantitative analytics, financial modeling, reporting) to coursework skills (dimensional modeling, dbt, Snowflake, Streamlit)
- Project summary: RMBS Market Intelligence Dashboard

### Repo structure to initialize
```
trading-analyst-fintech/
├── .gitignore
├── CLAUDE.md
├── README.md (stub)
├── docs/
│   ├── job-posting.pdf
│   └── proposal.pdf
├── knowledge/
│   ├── raw/
│   ├── wiki/
│   └── index.md
├── pipeline/
│   └── extract_fred.py (stub)
├── dbt/
└── dashboard/
    └── app.py (stub)
```

---

## 7. Directory & Repo Setup

- Repo name: `trading-analyst-fintech`
- `.gitignore`: Python, dbt, Snowflake credentials, `.env`
- `CLAUDE.md`: project context + knowledge base query conventions
- GitHub Actions: weekly schedule for FRED extraction + dbt run
