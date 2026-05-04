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
