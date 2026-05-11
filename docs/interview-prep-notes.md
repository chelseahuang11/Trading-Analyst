# Interview Prep Notes
**Role:** Trading Analyst, Asset-Backed Finance — Apollo Global Management
**Format:** 20-minute in-person, Hilton 114. Whiteboard required.

---

## What to Bring Into the Room
- Marker for the whiteboard
- Nothing else. No notes. No laptop.

---

## Phase 1 — "Tell Me About Yourself" (60 seconds)

> "I'm a junior at LMU studying Finance and Business Analytics — 3.85 GPA, with coursework
> in investments, financial statement analysis, and SQL.
>
> Last summer at AfterQuery, I analyzed 20+ Fortune 500 10-Ks to identify investment
> opportunities and surface insights for AI-driven analysis tools — so I understand what it
> means to screen investments and turn data into a decision.
>
> On my own time, I built an end-to-end pipeline tracking residential mortgage-backed
> securities indicators — mortgage rates, delinquency rates, housing starts — using Python,
> Snowflake, and SQL, with a live dashboard that surfaces the macro signals this role
> monitors every day.
>
> I'm also bilingual in English and Chinese, which has made me comfortable operating fast
> across very different contexts.
>
> That RMBS pipeline is exactly what I want to walk you through — because it was built
> around the asset-backed finance market."

**Five targets hit:**
- **Education:** LMU Finance + Business Analytics, 3.85, investments/SQL coursework
- **Initiative:** RMBS pipeline built on own time — Python, Snowflake, SQL, live dashboard
- **Relevant work:** AfterQuery — 20+ 10-K filings, investment screening, AI-driven analysis
- **Personal tidbit:** Bilingual English and Chinese
- **Segue:** "That RMBS pipeline… built around the asset-backed finance market"

**Stack words landed:** residential mortgage-backed securities, SQL, Snowflake, Python,
delinquency rates, asset-backed finance, screening investments

---

## Phase 2 — Project Walkthrough (14 minutes at whiteboard)

### Open with the Elevator Pitch (say this first, before drawing anything)

> "I built an end-to-end analytics pipeline that tracks RMBS market indicators — mortgage
> rates, delinquency rates, housing starts, and home prices — pulled from the Federal Reserve
> FRED API, transformed in Snowflake via dbt, and surfaced through a live Streamlit
> dashboard. The goal: give a Trading Analyst at Apollo the same macro signals they need to
> monitor residential mortgage-backed securities collateral performance."

---

### Draw Pipeline 1 — Structured Data (left side of whiteboard)

Draw boxes left to right, label every arrow with the tool name:

```
FRED API  →  extract_fred.py  →  GitHub Actions  →  Snowflake RAW
                                (runs weekly,           RMBS.RAW.FRED_OBSERVATIONS
                                 Monday 6AM)

Snowflake RAW  →  dbt staging  →  dbt mart  →  Streamlit dashboard
                  stg_fred_obs    3 tables        (live, Community Cloud)
                                  dim_date
                                  dim_indicator
                                  fact_rmbs_indicators
```

**What to say as you draw:**
"The FRED API is the Federal Reserve's free data service. I pull 9 economic series going
back to 2000 — three mortgage rate series, two delinquency rate series, two housing supply
series, and two home price indices. My Python script `extract_fred.py` hits the API, cleans
the data, and loads it into Snowflake. GitHub Actions runs this automatically every Monday
at 6 AM — I don't touch it. The credentials — API keys, Snowflake passwords — are stored
as secrets in GitHub, never in the code.

In Snowflake, the raw table has just three columns: series ID, date, value. dbt then
transforms that into a star schema — a fact table of every data point, joined to a date
dimension and an indicator dimension. The Streamlit dashboard reads directly from the mart
and displays it as interactive charts."

---

### Draw Pipeline 2 — Knowledge Base (right side of whiteboard)

```
16 web sources  →  scrape.py  →  GitHub Actions  →  knowledge/raw/
(Apollo, SIFMA,    (Firecrawl)                       16 .md files
MBA, NY Fed,
KBRA, Freddie Mac)

knowledge/raw/  →  Claude Code synthesis  →  knowledge/wiki/
                                              3 summary pages
                                              + knowledge/index.md
```

**What to say as you draw:**
"The second pipeline is the knowledge base. I used Firecrawl — a web scraping service — to
pull 16 financial research sources: Apollo's strategy pages, SIFMA MBS statistics, MBA
delinquency surveys, NY Fed data, KBRA Non-QM research, Freddie Mac outlooks. Each source
gets saved as a text file in `knowledge/raw/`.

Claude Code then synthesized those 16 files into 3 wiki pages in `knowledge/wiki/`. There's
also an index file that maps every raw source to its wiki page. When I query the knowledge
base, I read the index first to find the right wiki page, then drill into raw only if I
need an exact quote or figure."

---

### Technical Deep Dives

#### Data Ingestion

**The load pattern — why DELETE then INSERT:**
For each series, the script deletes all existing rows for that series, then re-inserts
everything. This is called an idempotent load — you can run it twice and get the same
result. The reason: FRED sometimes revises historical data retroactively. If I only added
new rows, I'd miss corrections to old data.

**Secrets handling:**
API keys and Snowflake passwords live in GitHub's "Secrets" vault (Settings → Secrets →
Actions). The GitHub Actions workflow pulls them as environment variables at runtime.
They are never written in any file in the repo.

**The `"."` filter:**
FRED uses a literal period `"."` to represent missing data. The script checks for this and
skips those rows before loading.

#### Snowflake and dbt

**Raw table — `RMBS.RAW.FRED_OBSERVATIONS`:**

| Column | What it is |
|--------|-----------|
| series_id | Which indicator, e.g. "MORTGAGE30US" |
| observation_date | The date of the data point |
| value | The actual number, e.g. 7.08 |
| loaded_at | Timestamp auto-set by Snowflake when the row was inserted |

Primary key is `(series_id, observation_date)` — no duplicate data points.

**dbt staging — `stg_fred_observations.sql`:**
Just type casting. Makes sure `observation_date` is stored as a proper date and `value` as
a float. No joins, no business logic. Staging is always just cleaning.

**dbt mart — star schema:**

`dim_date` — a calendar table. Every date, with year, quarter, month, day of week,
is_weekend. Lets the dashboard filter by Q3 2022 or "show me monthly" without doing math.

`dim_indicator` — a lookup table for the 9 series. Built from a hard-coded VALUES() list
in SQL because the 9 series never change. Has the human-readable name, category, unit,
frequency.

`fact_rmbs_indicators` — the main table. Every single data point, joined to dim_date and
dim_indicator. One row = one observation. This is what the dashboard queries.

**Why star schema?** It makes filtering fast and intuitive. You can ask "show me all
Mortgage Rates data in Q3 2022" by joining one fact table to two dimension tables. It's the
standard pattern for analytical dashboards.

**dbt tests run:**
- `not_null` on `fact_rmbs_indicators.observation_date`, `series_id`, `value`
- `not_null` on `dim_indicator.series_id`, `dim_date.full_date`
- `unique` on `dim_date.full_date`, `dim_indicator.series_id`

#### Knowledge Base

**Three wiki pages:**

| Page | What it covers | Raw sources |
|------|---------------|-------------|
| `apollo-abf-platform.md` | Apollo's ABF strategy, $44B+ deployed, origination platform, global expansion | 01, 02, 16 |
| `non-qm-market.md` | Non-QM securitization history, 3.8% CDR / 0.03% loss rate on 475K loans / $216.7B | 09, 10, 11 |
| `rmbs-market-conditions.md` | MBS issuance ($1.6T in 2024), delinquency (Cotality 3.2%, MBA 4.26%), housing supply, home prices | 03–08, 12–15 |

**How to answer a knowledge base question in the interview:**
1. "I'd go to `knowledge/index.md` first to identify which wiki page is relevant."
2. "Then open that wiki page — it synthesizes across multiple sources."
3. "If you need an exact figure, I'd drill into the specific raw file it cites."

**Example the instructor will likely ask:**
*"What does your knowledge base say about Non-QM default risk?"*
→ Index points to `non-qm-market.md`
→ Wiki cites `09-kbra-non-qm-default-study.md`: 475K loans, $216.7B face value, 3.8%
cumulative default rate, 0.03% loss rate
→ Business translation: even when Non-QM loans default, loss severities are extremely low —
this supports Apollo's conviction in the asset class

#### Streamlit Dashboard

Four tabs — sketch each on the whiteboard:

| Tab | What's in it |
|-----|-------------|
| Mortgage Rates | Trend line (30Y / 15Y / ARM) + diagnostic: 30Y rate vs. SF delinquency on dual axes, shaded Fed tightening region 2022–2024 |
| Delinquency Rates | Trend line (SF delinquency + real estate delinquency) + latest values table |
| Housing Supply | Trend line (housing starts + building permits) + latest values table |
| Home Price Index | Trend line (Case-Shiller + USSTHPI) + latest values table |

Sidebar: year-range slider (2000–2026), live KPI metrics (latest 30Y rate, SF delinquency,
Case-Shiller HPI).

---

### Two Specific Insights (memorize both)

**Insight 1 — Rate spike, no delinquency spike yet:**
"30-year fixed rates peaked at ~7.8% in October 2023 — the highest since 2000 — following
the Fed tightening cycle from 0.25% in early 2022. But single-family delinquency has stayed
near historic lows. For Apollo, this is the key watch indicator: delinquency typically lags
rate increases by 4–6 quarters, so the question is whether rising rates eventually translate
into collateral stress on existing RMBS vintages."

**Insight 2 — Home prices still elevated, supply still constrained:**
"The Case-Shiller National HPI rose ~45% from 2020 to mid-2022 — the fastest appreciation
on record. Price growth has slowed but stayed positive. Building permits declined faster
than housing starts, which is a leading indicator that new supply will stay constrained.
For RMBS collateral, that means strong home price appreciation cushion on current
vintages — borrowers have equity."

---

### Challenge, Improvement, Lesson (have one of each ready)

**One significant challenge:**
"Mixed-frequency data. My 9 FRED series report at different cadences — weekly, monthly,
quarterly. They all land in the same raw table, which means a quarterly delinquency reading
and a weekly mortgage rate exist side by side. The star schema solved this: `dim_date`
covers every date, and the fact table joins on the exact observation date each series
reported. Plotly then handles the gaps naturally when charting."

**One future improvement:**
"I'd add prepayment speed data — CPR — alongside the FRED indicators. Delinquency tells
the credit story, but prepayment tells the duration story. For pricing RMBS at the deal
level, you need both. The pipeline is already structured for it: I'd add a new extract
script, a new row in `dim_indicator`, and a new dashboard tab."

**One lesson learned:**
"Set up secrets management before you write the first line of extraction code, not after.
I nearly committed a `.env` file early on. The right order: create `.gitignore` for `.env`,
configure GitHub Secrets, then write the code. That pattern transfers to any project that
touches external APIs or databases."

---

## Likely Probe Questions

**"Why GitHub Actions over Airflow?"**
GitHub Actions is built into the repo — no extra infrastructure, free, has manual
`workflow_dispatch` trigger. Airflow would require running a separate server to manage a
pipeline that runs once a week. If this were a production pipeline with dozens of dependent
jobs, Airflow would be the right call.

**"Why DELETE + INSERT instead of just adding new rows?"**
FRED revises historical data retroactively. A full reload per series captures any upstream
corrections, not just new dates. If I only appended, I'd miss those revisions.

**"What breaks at 100x data volume?"**
The `executemany` loop in `extract_fred.py` does single-row inserts — it would get slow.
Fix: switch to Snowflake's `write_pandas` function or a COPY INTO command that bulk-loads
from a staged file. The dbt models and Snowflake itself are fine at scale.

**"Why is `dim_indicator` hard-coded instead of read from a table?"**
The 9 series and their metadata are static — they don't change unless I add a new FRED
series. Hard-coding them as a VALUES() list in dbt means the dimension always stays in
sync with the extract script. If it were dynamic, I'd need another load step for a table
that almost never changes.

**"Tell me about the knowledge base layers."**
`knowledge/raw/` = 16 unedited source files from Firecrawl scrapes.
`knowledge/wiki/` = 3 synthesized pages Claude Code wrote from those sources.
`knowledge/index.md` = the catalog that maps every raw file to its wiki page.
The two-layer design means I never have to read 16 documents to answer one question —
the wiki is the fast path, raw is the citation backup.

---

## Plain English Glossary

| Term | What it actually is |
|------|-------------------|
| **FRED API** | The Federal Reserve's free data service. You ask it for economic data automatically instead of downloading it manually. |
| **Python script** | Code you wrote that fetches, cleans, and moves data. |
| **GitHub Actions** | A timer inside GitHub that runs your code on a schedule automatically. |
| **GitHub Secrets** | A vault inside GitHub where passwords and API keys are stored safely — never in code. |
| **Snowflake** | A cloud database (runs on Amazon's servers, not your laptop). Like a very powerful Excel that's always online. |
| **dbt** | A tool that lets you write SQL to transform and reorganize data inside Snowflake. |
| **Staging layer** | The first transformation step — just type cleaning. No business logic. |
| **Mart layer** | The second transformation step — the final, analysis-ready tables the dashboard reads. |
| **Star schema** | A way of organizing tables: one big fact table in the middle, smaller dimension tables connected to it. Makes filtering fast. |
| **Fact table** | The main data table. One row = one data point (date + indicator + value). |
| **Dimension table** | A lookup table that adds context to the fact table (e.g., what month is this? what is this indicator called?). |
| **Streamlit** | A Python library that turns Python code into a website with charts. No web design needed. |
| **Community Cloud** | Streamlit's free hosting service. Makes your app accessible at a public URL. |
| **Firecrawl** | A service that reads websites and converts them to plain text. Handles modern sites that load content with JavaScript. |
| **knowledge/raw/** | 16 text files — one per scraped financial source. The unedited originals. |
| **knowledge/wiki/** | 3 summary pages written by Claude Code, synthesizing across the raw sources. |
| **knowledge/index.md** | The table of contents for the knowledge base. Maps every raw file to its wiki page. |
| **Markdown (.md)** | A simple text format. Like a Word document but plain text with simple formatting like # for headers. All the knowledge base files are in this format. |
| **RMBS** | Residential Mortgage-Backed Securities. Bundles of home mortgages packaged into bonds that investors can buy. Apollo trades these. |
| **Non-QM** | Non-Qualified Mortgage. Home loans that don't meet standard government lending criteria — self-employed borrowers, investors, etc. A sub-sector Apollo focuses on. |
| **Delinquency rate** | The percentage of borrowers who are behind on mortgage payments. A key signal for RMBS collateral health. |
| **HPI (Home Price Index)** | A measure of how much home prices have changed over time. Case-Shiller is the most widely cited one. |
| **Case-Shiller** | The S&P/Case-Shiller National Home Price Index — the standard benchmark for U.S. home price appreciation. |
| **CDR** | Cumulative Default Rate — the total percentage of loans in a pool that have defaulted over time. |
