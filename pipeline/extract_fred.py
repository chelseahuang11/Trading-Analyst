import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

FRED_SERIES = {
    "MORTGAGE30US": {
        "name": "30-Year Fixed Rate Mortgage Average",
        "category": "Mortgage Rates",
        "unit": "Percent",
        "frequency": "Weekly",
    },
    "MORTGAGE15US": {
        "name": "15-Year Fixed Rate Mortgage Average",
        "category": "Mortgage Rates",
        "unit": "Percent",
        "frequency": "Weekly",
    },
    "MORTGAGE5US": {
        "name": "5/1-Year ARM Average",
        "category": "Mortgage Rates",
        "unit": "Percent",
        "frequency": "Weekly",
    },
    "DRSFRMACBS": {
        "name": "Delinquency Rate on Single-Family Residential Mortgages",
        "category": "Delinquency Rates",
        "unit": "Percent",
        "frequency": "Quarterly",
    },
    "DRSREACBS": {
        "name": "Delinquency Rate on Real Estate Loans",
        "category": "Delinquency Rates",
        "unit": "Percent",
        "frequency": "Quarterly",
    },
    "HOUST": {
        "name": "Housing Starts: Total New Privately-Owned Units",
        "category": "Housing Supply",
        "unit": "Thousands of Units",
        "frequency": "Monthly",
    },
    "PERMIT": {
        "name": "New Private Housing Units Authorized by Building Permits",
        "category": "Housing Supply",
        "unit": "Thousands of Units",
        "frequency": "Monthly",
    },
    "CSUSHPISA": {
        "name": "S&P/Case-Shiller U.S. National Home Price Index",
        "category": "Home Price Index",
        "unit": "Index Jan 2000=100",
        "frequency": "Monthly",
    },
    "USSTHPI": {
        "name": "All-Transactions House Price Index for the United States",
        "category": "Home Price Index",
        "unit": "Index 1980 Q1=100",
        "frequency": "Quarterly",
    },
}


def fetch_observations(series_id):
    url = f"{FRED_BASE_URL}/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": "2000-01-01",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    rows = []
    for obs in data["observations"]:
        if obs["value"] == ".":
            continue
        rows.append((series_id, obs["date"], float(obs["value"])))
    return rows


DB = os.getenv("SNOWFLAKE_DATABASE", "RMBS")
SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
TABLE = f"{DB}.{SCHEMA}.FRED_OBSERVATIONS"


def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=DB,
    )


def setup_table(cur):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            series_id        VARCHAR(50)   NOT NULL,
            observation_date DATE          NOT NULL,
            value            FLOAT         NOT NULL,
            loaded_at        TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (series_id, observation_date)
        )
    """)


def load(cur, series_id, rows):
    cur.execute(f"DELETE FROM {TABLE} WHERE series_id = %s", (series_id,))
    if rows:
        cur.executemany(
            f"INSERT INTO {TABLE} (series_id, observation_date, value) VALUES (%s, %s, %s)",
            rows,
        )


def main():
    print(f"[{datetime.utcnow().isoformat()}] Starting FRED extraction")
    conn = get_connection()
    cur = conn.cursor()
    try:
        setup_table(cur)
        total = 0
        for series_id, meta in FRED_SERIES.items():
            print(f"  Fetching {series_id}: {meta['name']}")
            rows = fetch_observations(series_id)
            load(cur, series_id, rows)
            total += len(rows)
            print(f"    Loaded {len(rows)} rows")
        conn.commit()
        print(f"[{datetime.utcnow().isoformat()}] Done — {total} total rows loaded")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
