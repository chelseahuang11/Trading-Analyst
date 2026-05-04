# Dashboard Design Spec
**Date:** 2026-05-03  
**Project:** RMBS Market Intelligence Dashboard  
**Target Role:** Trading Analyst, Asset-Backed Finance (Apollo Global Management)

---

## Goal

Build a Streamlit dashboard connected to the Snowflake mart (`fact_rmbs_indicators`, `dim_date`, `dim_indicator`) that tells a clean, interview-ready story about RMBS market conditions. Deployed to Streamlit Community Cloud with a public URL.

Audience: hiring-manager / portfolio demo — polished, guided narrative, not a dense analyst tool.

---

## Architecture

Two files in `dashboard/`:

| File | Purpose |
|------|---------|
| `app.py` | Streamlit layout, tabs, charts, KPI cards |
| `connection.py` | Snowflake connection + single cached query function |

**Packages to add to `requirements.txt`:**
- `streamlit>=1.32.0`
- `pandas>=2.0.0`
- `plotly>=5.18.0` (line charts)

Existing `snowflake-connector-python>=3.6.0` and `python-dotenv>=1.0.0` are already in `requirements.txt`.

**Credentials:**
- Local: loaded from `.env` via `python-dotenv`
- Deployed: stored in Streamlit Community Cloud secrets (TOML format)

---

## Layout

```
┌─────────────┬─────────────────────────────────────────────────────┐
│ Sidebar     │  RMBS Market Intelligence Dashboard                 │
│             ├─────────────┬─────────────┬──────────┬─────────────┤
│ Date Range  │ Mortgage    │ Delinquency │ Housing  │ Home        │
│ [2000–2026] │ Rates       │ Rates       │ Supply   │ Prices      │
│             ├─────────────┴─────────────┴──────────┴─────────────┤
│ KPI Cards   │  ⚠ Insight callout (static, hand-written per tab)  │
│ • 30Y Rate  │                                                     │
│ • Delinq %  │  Line chart — all series in this category,         │
│ • Case-     │  filtered by sidebar date range                    │
│   Shiller   │                                                     │
│   HPI       │  Latest values table (series name | value | unit)  │
└─────────────┴─────────────────────────────────────────────────────┘
```

### Sidebar
- **Year range slider:** 2000–2026, default 2010–2026
- **3 KPI cards:** latest value for `MORTGAGE30US`, `DRSFRMACBS`, `CSUSHPISA`

### Tabs (4 total)

| Tab | Series | Descriptive/Diagnostic |
|-----|--------|----------------------|
| Mortgage Rates | MORTGAGE30US, MORTGAGE15US, MORTGAGE5US | Descriptive (trend) + Diagnostic (dual-axis overlay with delinquency, 4–6Q lag annotation) |
| Delinquency Rates | DRSFRMACBS, DRSREACBS | Descriptive |
| Housing Supply | HOUST, PERMIT | Descriptive |
| Home Prices | CSUSHPISA, USSTHPI | Descriptive |

**Insight callout box** on each tab: a static `st.info()` block with a 1–2 sentence takeaway written by hand (e.g. "30Y rates peaked at 7.8% in Oct 2023 — the highest since 2000, driven by the Fed's tightening cycle.").

**Diagnostic requirement** is satisfied by the Mortgage Rates tab's dual-axis overlay: 30Y rate on the left y-axis, single-family delinquency rate (`DRSFRMACBS`) on the right y-axis (both in percent, different scales). A static shaded region or vertical line annotation marks the 4–6 quarter lag between rate peaks and delinquency increases — hardcoded, not calculated.

---

## Data Flow

Single query in `connection.py`, decorated with `@st.cache_data`. The fact table is already fully denormalized (joins to dim_date and dim_indicator happen in dbt), so no joins needed at query time:

```sql
SELECT
    observation_date,
    series_id,
    indicator_name,
    indicator_category,
    unit,
    value
FROM fact_rmbs_indicators
WHERE observation_date BETWEEN %(start_date)s AND %(end_date)s
ORDER BY indicator_category, series_id, observation_date
```

Returns a single pandas DataFrame. Each tab filters in Python:
```python
df[df['indicator_category'] == 'Mortgage Rates']
```

Cache is invalidated when the date slider changes — no extra Snowflake round-trips when switching tabs. KPI cards derive from the same DataFrame (latest value per series).

---

## Deployment

1. Push `dashboard/` to GitHub
2. Deploy via Streamlit Community Cloud (connect to repo, set main file to `dashboard/app.py`)
3. In Advanced Settings → Secrets, paste all 7 Snowflake env vars in TOML format
4. Add live URL to `README.md`

---

## Rubric Checklist

- [x] Connected to Snowflake mart tables
- [x] Descriptive analytics view — trend charts on all 4 tabs
- [x] Diagnostic analytics view — dual-axis rate vs. delinquency overlay on Mortgage Rates tab
- [x] Interactive element — global date range slider
- [x] Deployed to Streamlit Community Cloud with public URL
