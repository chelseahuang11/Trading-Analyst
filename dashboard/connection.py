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
