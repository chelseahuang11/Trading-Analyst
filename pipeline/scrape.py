import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
FIRECRAWL_URL = "https://api.firecrawl.dev/v1/scrape"

SOURCES = [
    ("01-apollo-abf-strategy", "https://www.apollo.com/strategies/asset-management/credit/asset-backed-finance"),
    ("02-apollo-abc-product", "https://www.apollo.com/wealth/strategies/products/apollo-asset-backed-credit-company"),
    ("03-sifma-mbs-statistics-2024", "https://www.sifma.org/research/statistics/us-mortgage-backed-securities-statistics"),
    ("04-sifma-fixed-income-quarterly-1q26", "https://www.sifma.org/resources/research/fixed-income-chart/"),
    ("05-sifma-fixed-income-outstanding", "https://www.sifma.org/resources/research/us-fixed-income-securities-statistics/"),
    ("06-cotality-delinquency-dec2025", "https://www.cotality.com/press-releases/u-s-mortgage-delinquency-rate-finishes-2025-flat-year-over-year"),
    ("07-mba-delinquency-q4-2025", "https://www.mba.org/news-and-research/newsroom/news/2026/02/12/mortgage-delinquencies-increase-in-the-fourth-quarter-of-2025"),
    ("08-ny-fed-delinquency-geography-2026", "https://www.newyorkfed.org/microeconomics/hhdc"),
    ("09-kbra-non-qm-default-study", "https://www.kbra.com/publications/xNwHjNRm/kbra-releases-research-non-qm-default-study-a-decade-of-insights"),
    ("10-riskspan-non-qm-securitization-market", "https://riskspan.com/non-qualified-mortgage-securitization-market/"),
    ("11-morningstar-dbrs-non-qm-q4-2022", "https://dbrs.morningstar.com/research/410131"),
    ("12-freddie-mac-outlook-nov-2024", "https://www.freddiemac.com/research/forecast/20241126-us-economy-remains-resilient-with-strong-q3-growth"),
    ("13-freddie-mac-outlook-sep-2024", "https://www.freddiemac.com/research/forecast/20240919-housing-market-faces-affordability-headwinds"),
    ("14-federal-reserve-household-housing-2024", "https://www.federalreserve.gov/publications/2024-economic-well-being-of-us-households-in-2023-housing.htm"),
    ("15-ny-fed-housing-price-expectations-2024", "https://www.newyorkfed.org/microeconomics/sce/housing"),
    ("16-apollo-abf-global-strategy-2024", "https://www.apollo.com/strategies/asset-management/credit"),
]

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "raw")


def scrape(url: str) -> str:
    resp = requests.post(
        FIRECRAWL_URL,
        headers={"Authorization": f"Bearer {FIRECRAWL_API_KEY}", "Content-Type": "application/json"},
        json={"url": url, "formats": ["markdown"]},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", {}).get("markdown", "")


def slug_to_filename(slug: str) -> str:
    return f"{slug}.md"


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    for slug, url in SOURCES:
        filepath = os.path.join(RAW_DIR, slug_to_filename(slug))
        print(f"Scraping {slug}...")
        try:
            content = scrape(url)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Source: {url}\n\n{content}")
            print(f"  Saved {filepath}")
        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()
