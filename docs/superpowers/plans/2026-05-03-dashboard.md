# RMBS Streamlit Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 4-tab Streamlit dashboard connected to Snowflake's `MART.fact_rmbs_indicators`, surfacing RMBS market conditions, and deploy to Streamlit Community Cloud with a public URL.

**Architecture:** Two-file dashboard (`dashboard/app.py` + `dashboard/connection.py`). All data fetched in one `@st.cache_data`-decorated query; tabs filter the resulting DataFrame in Python. Sidebar has a global year-range slider and 3 KPI metric cards. Tabs: Mortgage Rates (includes diagnostic dual-axis overlay), Delinquency Rates, Housing Supply, Home Price Index.

**Tech Stack:** Python 3.11+, Streamlit ≥1.32, Plotly ≥5.18, pandas ≥2.0, snowflake-connector-python ≥3.6, python-dotenv ≥1.0, pytest ≥8.0

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `dashboard/requirements.txt` | Create | Streamlit Cloud dependency manifest |
| `dashboard/connection.py` | Create | Snowflake connection + cached query + helper functions |
| `dashboard/app.py` | Create | Streamlit layout, sidebar, 4 tabs, charts |
| `tests/conftest.py` | Create | Adds `dashboard/` to sys.path for imports |
| `tests/test_connection_helpers.py` | Create | Unit tests for `get_latest_value` and `filter_by_category` |

**Important facts about the schema:**
- Mart table: `MART.fact_rmbs_indicators` (fully qualified: `{DATABASE}.MART.fact_rmbs_indicators`)
- Snowflake returns column names in UPPERCASE — always `.lower()` them after fetching
- Actual `indicator_category` values in the data: `'Mortgage Rates'`, `'Delinquency Rates'`, `'Housing Supply'`, `'Home Price Index'`
- Connection uses `SNOWFLAKE_ROLE` env var (defaults to `'ACCOUNTADMIN'` if missing)

---

## Task 1: Create dashboard/requirements.txt and install packages

**Files:**
- Create: `dashboard/requirements.txt`

- [ ] **Step 1: Create `dashboard/requirements.txt`**

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
snowflake-connector-python>=3.6.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

- [ ] **Step 2: Install into the project venv**

Run from the repo root:
```bash
.venv/Scripts/pip install streamlit pandas plotly pytest
```

Expected: packages install without errors. `snowflake-connector-python` and `python-dotenv` are already installed.

- [ ] **Step 3: Verify Streamlit is available**

```bash
.venv/Scripts/python -c "import streamlit; print(streamlit.__version__)"
```

Expected: prints a version string like `1.32.0` or higher.

- [ ] **Step 4: Commit**

```bash
git add dashboard/requirements.txt
git commit -m "chore: add dashboard requirements.txt"
```

---

## Task 2: Build connection.py (TDD)

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_connection_helpers.py`
- Create: `dashboard/connection.py`

- [ ] **Step 1: Create `tests/conftest.py`**

```python
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dashboard'))
```

- [ ] **Step 2: Write failing tests in `tests/test_connection_helpers.py`**

```python
import pandas as pd
import pytest
from connection import get_latest_value, filter_by_category


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'observation_date': pd.to_datetime([
            '2023-01-01', '2023-06-01', '2023-12-01', '2023-01-01'
        ]),
        'series_id': ['MORTGAGE30US', 'MORTGAGE30US', 'MORTGAGE30US', 'DRSFRMACBS'],
        'indicator_name': ['30Y Rate', '30Y Rate', '30Y Rate', 'SF Delinquency'],
        'indicator_category': [
            'Mortgage Rates', 'Mortgage Rates', 'Mortgage Rates', 'Delinquency Rates'
        ],
        'unit': ['Percent', 'Percent', 'Percent', 'Percent'],
        'value': [6.5, 7.0, 7.5, 2.1],
    })


def test_get_latest_value_returns_most_recent(sample_df):
    result = get_latest_value(sample_df, 'MORTGAGE30US')
    assert result == 7.5


def test_get_latest_value_unknown_series_returns_none(sample_df):
    result = get_latest_value(sample_df, 'NONEXISTENT')
    assert result is None


def test_filter_by_category_returns_matching_rows(sample_df):
    result = filter_by_category(sample_df, 'Mortgage Rates')
    assert len(result) == 3
    assert all(result['indicator_category'] == 'Mortgage Rates')


def test_filter_by_category_no_match_returns_empty(sample_df):
    result = filter_by_category(sample_df, 'Nonexistent')
    assert result.empty
```

- [ ] **Step 3: Run tests — expect failure (functions not defined yet)**

```bash
.venv/Scripts/pytest tests/test_connection_helpers.py -v
```

Expected: `ImportError: cannot import name 'get_latest_value' from 'connection'`

- [ ] **Step 4: Create `dashboard/connection.py`**

```python
import os
import pandas as pd
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def _get_env(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=_get_env('SNOWFLAKE_ACCOUNT'),
        user=_get_env('SNOWFLAKE_USER'),
        password=_get_env('SNOWFLAKE_PASSWORD'),
        role=_get_env('SNOWFLAKE_ROLE') or 'ACCOUNTADMIN',
        warehouse=_get_env('SNOWFLAKE_WAREHOUSE'),
        database=_get_env('SNOWFLAKE_DATABASE'),
    )


@st.cache_data(ttl=3600)
def get_data(start_date: str, end_date: str) -> pd.DataFrame:
    query = """
        SELECT
            observation_date,
            series_id,
            indicator_name,
            indicator_category,
            unit,
            value
        FROM MART.fact_rmbs_indicators
        WHERE observation_date BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY indicator_category, series_id, observation_date
    """
    conn = get_snowflake_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, {'start_date': start_date, 'end_date': end_date})
        df = cur.fetch_pandas_all()
    finally:
        cur.close()
        conn.close()
    df.columns = [c.lower() for c in df.columns]
    return df


def get_latest_value(df: pd.DataFrame, series_id: str):
    subset = df[df['series_id'] == series_id]
    if subset.empty:
        return None
    return subset.loc[subset['observation_date'].idxmax(), 'value']


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    return df[df['indicator_category'] == category].copy()
```

- [ ] **Step 5: Run tests — expect all 4 to pass**

```bash
.venv/Scripts/pytest tests/test_connection_helpers.py -v
```

Expected output:
```
PASSED tests/test_connection_helpers.py::test_get_latest_value_returns_most_recent
PASSED tests/test_connection_helpers.py::test_get_latest_value_unknown_series_returns_none
PASSED tests/test_connection_helpers.py::test_filter_by_category_returns_matching_rows
PASSED tests/test_connection_helpers.py::test_filter_by_category_no_match_returns_empty
4 passed
```

- [ ] **Step 6: Commit**

```bash
git add tests/conftest.py tests/test_connection_helpers.py dashboard/connection.py
git commit -m "feat: add connection.py with Snowflake query and helper functions"
```

---

## Task 3: Build app.py skeleton — page config, sidebar, KPI cards

**Files:**
- Create: `dashboard/app.py`

- [ ] **Step 1: Create `dashboard/app.py`**

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
from connection import get_data, get_latest_value, filter_by_category

st.set_page_config(
    page_title="RMBS Market Intelligence",
    page_icon="📈",
    layout="wide",
)

# --- Sidebar ---
st.sidebar.title("RMBS Market Intelligence")
st.sidebar.caption("Trading Analyst | Apollo Global Management")
st.sidebar.markdown("---")

year_range = st.sidebar.slider(
    "Date Range",
    min_value=2000,
    max_value=2026,
    value=(2010, 2026),
    step=1,
)

start_date = str(date(year_range[0], 1, 1))
end_date = str(date(year_range[1], 12, 31))

df = get_data(start_date, end_date)

st.sidebar.markdown("---")
st.sidebar.markdown("**Key Indicators (Latest)**")

rate_30y = get_latest_value(df, 'MORTGAGE30US')
delinq = get_latest_value(df, 'DRSFRMACBS')
hpi = get_latest_value(df, 'CSUSHPISA')

if rate_30y is not None:
    st.sidebar.metric("30Y Mortgage Rate", f"{rate_30y:.2f}%")
if delinq is not None:
    st.sidebar.metric("SF Delinquency Rate", f"{delinq:.2f}%")
if hpi is not None:
    st.sidebar.metric("Case-Shiller HPI", f"{hpi:.1f}")

# --- Main ---
st.title("RMBS Market Intelligence Dashboard")
st.markdown("*Federal Reserve FRED data · Snowflake mart · Updated weekly*")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Mortgage Rates",
    "⚠️ Delinquency Rates",
    "🏗️ Housing Supply",
    "🏠 Home Price Index",
])

with tab1:
    st.subheader("Mortgage Rates")
    st.info("**Insight:** 30-Year fixed rates peaked at ~7.8% in Oct 2023 — the highest since 2000 — following aggressive Fed tightening from 0.25% in early 2022. ARM spreads widened as the rate curve steepened.")

with tab2:
    st.subheader("Delinquency Rates")
    st.info("**Insight:** Single-family mortgage delinquency spiked above 8% in Q2 2020 (COVID forbearance) before falling to historic lows by 2022. Rising rates since 2022 have not yet translated into elevated delinquency — a key watch indicator for RMBS performance.")

with tab3:
    st.subheader("Housing Supply")
    st.info("**Insight:** Housing starts fell sharply in 2022–2023 as affordability deteriorated. Building permits declined even faster — a leading indicator of constrained future supply and continued price support.")

with tab4:
    st.subheader("Home Price Index")
    st.info("**Insight:** The Case-Shiller National HPI rose ~45% from 2020 to mid-2022, the fastest appreciation on record. Price growth has since slowed but remained positive, supported by low existing supply.")
```

- [ ] **Step 2: Run the app locally to verify sidebar and tab skeleton render**

```bash
.venv/Scripts/streamlit run dashboard/app.py
```

Expected: browser opens, sidebar shows date slider and 3 KPI metric cards, 4 tabs visible with subheadings and insight callouts. No charts yet.

If you see a Snowflake connection error, confirm `.env` is in the repo root and contains all 6–7 variables (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`).

- [ ] **Step 3: Commit**

```bash
git add dashboard/app.py
git commit -m "feat: add app.py skeleton with sidebar, KPI cards, and tab headings"
```

---

## Task 4: Mortgage Rates tab — trend chart + diagnostic dual-axis overlay

**Files:**
- Modify: `dashboard/app.py` (fill in `tab1` block)

- [ ] **Step 1: Replace the `tab1` block in `app.py` with the full content**

Replace:
```python
with tab1:
    st.subheader("Mortgage Rates")
    st.info("**Insight:** 30-Year fixed rates peaked at ~7.8% in Oct 2023 — the highest since 2000 — following aggressive Fed tightening from 0.25% in early 2022. ARM spreads widened as the rate curve steepened.")
```

With:
```python
with tab1:
    st.subheader("Mortgage Rates")
    st.info("**Insight:** 30-Year fixed rates peaked at ~7.8% in Oct 2023 — the highest since 2000 — following aggressive Fed tightening from 0.25% in early 2022. ARM spreads widened as the rate curve steepened.")

    df_rates = filter_by_category(df, 'Mortgage Rates')

    if df_rates.empty:
        st.warning("No mortgage rate data for the selected date range.")
    else:
        # Descriptive: trend line chart
        fig_trend = px.line(
            df_rates,
            x='observation_date',
            y='value',
            color='indicator_name',
            title='Mortgage Rate Trends',
            labels={
                'value': 'Rate (%)',
                'observation_date': 'Date',
                'indicator_name': 'Series',
            },
        )
        fig_trend.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        st.plotly_chart(fig_trend, use_container_width=True)

        # Latest values table
        latest = (
            df_rates.sort_values('observation_date')
            .groupby('indicator_name', as_index=False)
            .last()[['indicator_name', 'value', 'unit']]
            .rename(columns={'indicator_name': 'Indicator', 'value': 'Latest Value', 'unit': 'Unit'})
        )
        st.dataframe(latest, use_container_width=True, hide_index=True)

        # Diagnostic: dual-axis overlay — 30Y rate vs. delinquency
        st.markdown("#### Diagnostic: Rate Tightening vs. Delinquency Lag")
        st.caption("30Y mortgage rate (left axis) vs. single-family delinquency rate (right axis). Delinquency typically lags rate increases by 4–6 quarters.")

        df_30y = df[df['series_id'] == 'MORTGAGE30US'].sort_values('observation_date')
        df_delinq_diag = df[df['series_id'] == 'DRSFRMACBS'].sort_values('observation_date')

        fig_diag = make_subplots(specs=[[{'secondary_y': True}]])

        fig_diag.add_trace(
            go.Scatter(
                x=df_30y['observation_date'],
                y=df_30y['value'],
                name='30Y Rate (%)',
                line=dict(color='royalblue', width=2),
            ),
            secondary_y=False,
        )
        fig_diag.add_trace(
            go.Scatter(
                x=df_delinq_diag['observation_date'],
                y=df_delinq_diag['value'],
                name='SF Delinquency Rate (%)',
                line=dict(color='firebrick', width=2, dash='dash'),
            ),
            secondary_y=True,
        )

        # Shaded region: 2022 rate tightening → expected delinquency response window
        fig_diag.add_vrect(
            x0='2022-03-01',
            x1='2024-01-01',
            fillcolor='orange',
            opacity=0.08,
            annotation_text='Fed tightening cycle',
            annotation_position='top left',
        )

        fig_diag.update_yaxes(title_text='30Y Mortgage Rate (%)', secondary_y=False)
        fig_diag.update_yaxes(title_text='Delinquency Rate (%)', secondary_y=True)
        fig_diag.update_layout(
            title='30Y Rate vs. SF Delinquency Rate (Diagnostic)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        )
        st.plotly_chart(fig_diag, use_container_width=True)
```

- [ ] **Step 2: Rerun the app and verify the Mortgage Rates tab**

```bash
.venv/Scripts/streamlit run dashboard/app.py
```

Expected: Mortgage Rates tab shows a multi-line trend chart (3 series), a latest-values table, and a dual-axis overlay with the shaded Fed tightening region.

- [ ] **Step 3: Commit**

```bash
git add dashboard/app.py
git commit -m "feat: add Mortgage Rates tab with trend chart and diagnostic overlay"
```

---

## Task 5: Delinquency Rates tab

**Files:**
- Modify: `dashboard/app.py` (fill in `tab2` block)

- [ ] **Step 1: Replace the `tab2` block**

Replace:
```python
with tab2:
    st.subheader("Delinquency Rates")
    st.info("**Insight:** Single-family mortgage delinquency spiked above 8% in Q2 2020 (COVID forbearance) before falling to historic lows by 2022. Rising rates since 2022 have not yet translated into elevated delinquency — a key watch indicator for RMBS performance.")
```

With:
```python
with tab2:
    st.subheader("Delinquency Rates")
    st.info("**Insight:** Single-family mortgage delinquency spiked above 8% in Q2 2020 (COVID forbearance) before falling to historic lows by 2022. Rising rates since 2022 have not yet translated into elevated delinquency — a key watch indicator for RMBS performance.")

    df_delinq = filter_by_category(df, 'Delinquency Rates')

    if df_delinq.empty:
        st.warning("No delinquency data for the selected date range.")
    else:
        fig_delinq = px.line(
            df_delinq,
            x='observation_date',
            y='value',
            color='indicator_name',
            title='Mortgage Delinquency Rates',
            labels={
                'value': 'Delinquency Rate (%)',
                'observation_date': 'Date',
                'indicator_name': 'Series',
            },
        )
        fig_delinq.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        st.plotly_chart(fig_delinq, use_container_width=True)

        latest = (
            df_delinq.sort_values('observation_date')
            .groupby('indicator_name', as_index=False)
            .last()[['indicator_name', 'value', 'unit']]
            .rename(columns={'indicator_name': 'Indicator', 'value': 'Latest Value', 'unit': 'Unit'})
        )
        st.dataframe(latest, use_container_width=True, hide_index=True)
```

- [ ] **Step 2: Rerun the app and verify Delinquency tab**

```bash
.venv/Scripts/streamlit run dashboard/app.py
```

Expected: Delinquency Rates tab shows a 2-series line chart (DRSFRMACBS, DRSREACBS) and a latest-values table.

- [ ] **Step 3: Commit**

```bash
git add dashboard/app.py
git commit -m "feat: add Delinquency Rates tab"
```

---

## Task 6: Housing Supply tab

**Files:**
- Modify: `dashboard/app.py` (fill in `tab3` block)

- [ ] **Step 1: Replace the `tab3` block**

Replace:
```python
with tab3:
    st.subheader("Housing Supply")
    st.info("**Insight:** Housing starts fell sharply in 2022–2023 as affordability deteriorated. Building permits declined even faster — a leading indicator of constrained future supply and continued price support.")
```

With:
```python
with tab3:
    st.subheader("Housing Supply")
    st.info("**Insight:** Housing starts fell sharply in 2022–2023 as affordability deteriorated. Building permits declined even faster — a leading indicator of constrained future supply and continued price support.")

    df_housing = filter_by_category(df, 'Housing Supply')

    if df_housing.empty:
        st.warning("No housing supply data for the selected date range.")
    else:
        fig_housing = px.line(
            df_housing,
            x='observation_date',
            y='value',
            color='indicator_name',
            title='Housing Starts and Building Permits',
            labels={
                'value': 'Thousands of Units',
                'observation_date': 'Date',
                'indicator_name': 'Series',
            },
        )
        fig_housing.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        st.plotly_chart(fig_housing, use_container_width=True)

        latest = (
            df_housing.sort_values('observation_date')
            .groupby('indicator_name', as_index=False)
            .last()[['indicator_name', 'value', 'unit']]
            .rename(columns={'indicator_name': 'Indicator', 'value': 'Latest Value', 'unit': 'Unit'})
        )
        st.dataframe(latest, use_container_width=True, hide_index=True)
```

- [ ] **Step 2: Rerun the app and verify Housing Supply tab**

```bash
.venv/Scripts/streamlit run dashboard/app.py
```

Expected: Housing Supply tab shows a 2-series line chart (HOUST, PERMIT) and a latest-values table.

- [ ] **Step 3: Commit**

```bash
git add dashboard/app.py
git commit -m "feat: add Housing Supply tab"
```

---

## Task 7: Home Price Index tab

**Files:**
- Modify: `dashboard/app.py` (fill in `tab4` block)

- [ ] **Step 1: Replace the `tab4` block**

Replace:
```python
with tab4:
    st.subheader("Home Price Index")
    st.info("**Insight:** The Case-Shiller National HPI rose ~45% from 2020 to mid-2022, the fastest appreciation on record. Price growth has since slowed but remained positive, supported by low existing supply.")
```

With:
```python
with tab4:
    st.subheader("Home Price Index")
    st.info("**Insight:** The Case-Shiller National HPI rose ~45% from 2020 to mid-2022, the fastest appreciation on record. Price growth has since slowed but remained positive, supported by low existing supply.")

    df_hpi = filter_by_category(df, 'Home Price Index')

    if df_hpi.empty:
        st.warning("No home price data for the selected date range.")
    else:
        fig_hpi = px.line(
            df_hpi,
            x='observation_date',
            y='value',
            color='indicator_name',
            title='Home Price Indices',
            labels={
                'value': 'Index Value',
                'observation_date': 'Date',
                'indicator_name': 'Series',
            },
        )
        fig_hpi.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
        st.plotly_chart(fig_hpi, use_container_width=True)

        latest = (
            df_hpi.sort_values('observation_date')
            .groupby('indicator_name', as_index=False)
            .last()[['indicator_name', 'value', 'unit']]
            .rename(columns={'indicator_name': 'Indicator', 'value': 'Latest Value', 'unit': 'Unit'})
        )
        st.dataframe(latest, use_container_width=True, hide_index=True)
```

- [ ] **Step 2: Rerun the app and verify all 4 tabs**

```bash
.venv/Scripts/streamlit run dashboard/app.py
```

Expected: All 4 tabs render charts and latest-values tables. Date slider changes all tabs simultaneously. KPI cards in sidebar update with latest data.

- [ ] **Step 3: Commit**

```bash
git add dashboard/app.py
git commit -m "feat: add Home Price Index tab — all 4 tabs complete"
```

---

## Task 8: Deploy to Streamlit Community Cloud

**Files:**
- No file changes — this task is deployment steps only

- [ ] **Step 1: Push everything to GitHub**

```bash
git push origin main
```

- [ ] **Step 2: Open your locally running Streamlit app, click Deploy (top-right corner)**

In the modal: click **Deploy now** under **Streamlit Community Cloud**.

- [ ] **Step 3: In the deployment form, confirm these fields**

- Repository: your GitHub repo URL
- Branch: `main`
- Main file path: `dashboard/app.py`

- [ ] **Step 4: Click Advanced settings → paste these secrets in TOML format**

Replace values with your actual `.env` values:
```toml
SNOWFLAKE_ACCOUNT = "your-account-here"
SNOWFLAKE_USER = "your-user-here"
SNOWFLAKE_PASSWORD = "your-password-here"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"
SNOWFLAKE_WAREHOUSE = "your-warehouse-here"
SNOWFLAKE_DATABASE = "your-database-here"
```

- [ ] **Step 5: Click Deploy and wait 60–90 seconds for the build to complete**

Watch the build log. Common failures:
- `ModuleNotFoundError` → missing package in `dashboard/requirements.txt`
- Snowflake auth error → wrong account format (must use hyphens, e.g. `xy12345-ab12345`), wrong password, wrong role
- `Object does not exist` → wrong database name or schema — mart tables live in `{DATABASE}.MART`

- [ ] **Step 6: Verify the deployed app**

Click through all 4 tabs. Move the date slider. Confirm KPI cards show values. If any tab shows a blank chart, check the build log for query errors.

---

## Task 9: Update README with live URL

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Copy your public Streamlit URL (format: `https://yourapp.streamlit.app`)**

- [ ] **Step 2: Add the URL near the top of `README.md`**

Find the project title line and add below it:
```markdown
**Live Dashboard:** [RMBS Market Intelligence Dashboard](https://yourapp.streamlit.app)
```

- [ ] **Step 3: Commit and push**

```bash
git add README.md
git commit -m "docs: add live Streamlit dashboard URL to README"
git push origin main
```

---

## Self-Review Checklist

- [x] Spec coverage: architecture (Task 2), sidebar (Task 3), all 4 tabs (Tasks 4–7), deployment (Task 8), README (Task 9)
- [x] No placeholders or TBDs
- [x] Column names consistently lowercase (`.lower()` applied after `fetch_pandas_all()`)
- [x] Category strings match actual data: `'Mortgage Rates'`, `'Delinquency Rates'`, `'Housing Supply'`, `'Home Price Index'`
- [x] `SNOWFLAKE_ROLE` handled with fallback to `'ACCOUNTADMIN'`
- [x] Rubric: descriptive ✓ (trend charts), diagnostic ✓ (dual-axis overlay), interactive ✓ (date slider), deployed ✓
