# Project Proposal

**Name:** Chelsea Huang

**Project Name:** RMBS Market Intelligence Dashboard

**GitHub Repo:** https://github.com/chelseahuang11/Trading-Analyst

## Job Posting

- **Role:** Trading Analyst, Asset-Backed Finance
- **Company:** Apollo Global Management
- **Link:** https://www.indeed.com/viewjob?jk=860b106f268bddff

**SQL requirement (quote the posting):** "Mastery of Microsoft Office (Word, Excel, PowerPoint, etc.) is required; proficiency in Basic VBA and SQL is desirable but not required."

## Reflection

This posting is directly relevant to this class because it targets a trading analyst role that requires the same quantitative and data skills covered in Analytics Engineering — specifically SQL, financial modeling, and ad-hoc analysis to support investment decision-making. The coursework skills it requires include SQL querying, dimensional modeling, dbt transformations, Snowflake-based pipelines, and dashboard development, all of which map to the posting's emphasis on analytical rigor and reporting for the trading desk. To prove I can do this job, I am building an end-to-end RMBS Market Intelligence Dashboard: a pipeline that extracts Federal Reserve economic data (mortgage rates, delinquency rates by loan type, housing starts, and home price indices) via the FRED API, transforms it through raw, staging, and mart layers using dbt in Snowflake, and surfaces market insights through a deployed Streamlit dashboard, paired with a knowledge base synthesizing research from Apollo, SIFMA, and housing finance publications. This same project transfers to at least two or three similar roles — Fixed Income Analyst, Credit Analyst, or BI Analyst at a mortgage company or bank — because the FRED API pipeline, star schema design, and financial time-series dashboard pattern apply directly to any role requiring structured analytics on debt markets.
