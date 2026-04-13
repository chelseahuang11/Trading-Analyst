# Project Proposal: RMBS Market Intelligence Dashboard

**Student:** Chelsea  
**Course:** ISBA 4715 — Analytics Engineering 
**Date:** April 13, 2026  
**GitHub Repo:** [trading-analyst-fintech](https://github.com/chelseaisba/trading-analyst-fintech)

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

---

## Transferability

This project transfers to: Fixed Income Analyst, Credit Analyst, BI Analyst at mortgage companies or banks, Structured Products Analyst. The FRED API pipeline and dbt star schema pattern applies to any role requiring financial time-series analytics.
