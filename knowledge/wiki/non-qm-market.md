# Non-QM RMBS Market: Performance, Structure, and Risk
**Last updated:** 2026-05-04
**Sources:** 09-kbra-non-qm-default-study.md, 10-riskspan-non-qm-securitization-market.md, 11-morningstar-dbrs-non-qm-q4-2022.md

## Overview

Non-QM RMBS emerged post-2015 to serve borrowers excluded by post-crisis Qualified Mortgage standards — self-employed individuals, credit-blemished borrowers, real estate investors, and foreign nationals — and has built a decade-long track record that challenges its perceived risk: a 3.8% weighted average cumulative default rate across nearly 600 transactions has translated into just 0.03% in realized credit losses, demonstrating that sound underwriting can deliver near-investment-grade credit outcomes on non-agency collateral. The 2022 rate shock stress-tested the market and confirmed the structural thesis — senior tranches held while subordinated spreads widened, creating entry points for credit investors with conviction on collateral quality. The dominant risk driver is borrower selection, not market structure: non-prime profiles (8–10% CDR) diverge sharply from the overall average, making collateral composition the primary analytical variable.

## Key Data Points

- KBRA analyzed over **475,000 loans** totaling **$216.7 billion** in original balance across nearly **600 NQM transactions** issued from 2015 to April 2025 ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Weighted average cumulative default rate across all vintages: **3.8%** ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Realized credit losses averaged just **0.03%** — a figure that dramatically understates nominal default rates due to recoveries ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Of all defaulted loans, approximately **300 involuntary liquidations** resulted in meaningful losses, with average loss severity of **26.5%** ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Non-prime borrower profiles (prior credit events) exhibited CDRs of **8–10%**, roughly 2–3x the portfolio average ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- FICO below 660 correlates with ~**10% default rates**; FICO above 760 drops below **2%** ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- CLTV at 85%+ correlates with **5.5% default rates**; 65–70% CLTV narrows to **4.1%** ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Alt Doc loans defaulted at rates **12.9% higher** than Full Doc loans on average ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- Vintage CDRs (excluding COVID period): 2019 (~5.5%), 2020 (~5.0%), 2022 (~4.0%), 2023 (~4.1%) ([KBRA](../raw/09-kbra-non-qm-default-study.md))
- In Q4 2022, subordinated bonds bore the brunt of spread widening while senior tranches maintained stability driven by credit enhancement buffers ([Morningstar DBRS](../raw/11-morningstar-dbrs-non-qm-q4-2022.md))
- Non-bank financial institutions have dominated non-QM originations, backed by asset managers, hedge funds, and private equity ([RiskSpan](../raw/10-riskspan-non-qm-securitization-market.md))

## Key Insights

The headline finding from a decade of KBRA data is deceptively simple but strategically important: a 3.8% CDR translating to 0.03% realized losses means Non-QM has delivered equity-like risk exposure — borrowers outside GSE eligibility, alternative documentation, non-standard products — with bond-like credit outcomes. The mechanism is recoveries: loss severity on the roughly 300 involuntary liquidations averaged 26.5%, which implies average recovery rates near 74%. This is the core thesis for why Apollo and similar asset managers participate in Non-QM: the incremental yield premium over agency paper reflects perceived borrower risk that disciplined underwriting largely neutralizes, as long as collateral (LTV) is managed and FICO floors are enforced.

The KBRA vintage data and Morningstar DBRS Q4 2022 analysis reach a shared conclusion through different lenses: when underwriting is sound, Non-QM performs through rate cycles. The 2019–2020 vintages showed elevated CDRs (~5.0–5.5%) driven by COVID forbearance disruption rather than structural underwriting failure — these loans experienced hardship deferrals, not collateral defaults driven by underwater LTV positions. The 2022–2023 vintages, originated into a higher-rate environment with more conservative post-pandemic underwriting, tracked closer to the 4% range. The Q4 2022 Morningstar DBRS report confirms that even as the 30-year mortgage rate spiked and secondary credit spreads widened materially on subordinated bonds, rated senior tranches saw no credit impairment — deals with higher FICO and lower LTV collateral outperformed weaker-collateral deals, validating the underwriting-first framework.

The spread widening in sub tranches during 2022 is not a sign of structural fragility — it is a feature of how RMBS structures absorb macro shocks. Subordinated bonds are designed to take first-loss exposure; when macro uncertainty rises and prepayments slow (extending duration), sub investors demand more spread. This is a price discovery process, not a credit event, and it creates entry points for investors who can model expected losses with precision. The Morningstar DBRS observation that "issuers continued to bring new deals to the market despite wider credit spreads" confirms market permanence — Non-QM is not a cyclical origination program that shuts down in stress, it is a structurally necessary channel for a borrower population that cannot access agency credit.

Non-prime profiles (8–10% CDR) are the primary risk driver and the reason collateral pool composition is the most important diligence variable in Non-QM. The Alt Doc premium (+12.9% default rate over Full Doc) reflects income verification uncertainty, not borrower bad faith — bank statement programs and DSCR loans carry documentation risk that must be offset by FICO and LTV compensating factors. The RiskSpan framing of the regulatory context matters here: Non-QM emerged to serve borrowers excluded by QM standards, not to recreate pre-crisis subprime. The structural protections (credit enhancement levels, sequential pay waterfalls, post-crisis rating agency methodology) are meaningfully stronger than pre-2008 precedents, and the 0.03% realized loss figure is the empirical validation of that structural improvement.

## Relevant to RMBS Trading

A Trading Analyst monitoring Non-QM RMBS positions uses these four dashboard indicators to track the macro and credit conditions that drive deal performance:

- **Delinquency tab (DRSFRMACBS):** Early delinquency rate movements in FRED agency data are a leading indicator for vintage-level stress in Non-QM deals. The 2019–2020 COVID spike in delinquencies preceded realized losses in weaker-collateral Non-QM pools; monitoring delinquency trends helps flag whether rising forbearance reflects temporary hardship or deteriorating credit underwriting in recently originated Non-QM collateral. See also: [rmbs-market-conditions.md](./rmbs-market-conditions.md) for current delinquency rate data.

- **Mortgage Rates tab:** The rate environment directly affects Non-QM origination volume and spread dynamics. The Q4 2022 rate shock reduced origination to "a fraction of peak volumes" at some lenders, compressing new deal supply and widening sub spreads — both factors relevant to secondary market positioning. When rates fall, Non-QM prepayment speeds accelerate (particularly on investor DSCR and bank statement loans, which are refinance-opportunistic), introducing extension and contraction risk.

- **Home Price Index tab:** HPI is the critical collateral variable for Non-QM loss severity. The 26.5% average severity on involuntary liquidations reflects partial recovery from home equity — as HPA moderates or reverses, expected severity rises, widening the gap between nominal CDR (3.8%) and realized losses (0.03%). The Morningstar DBRS Q4 2022 analysis explicitly flagged regional home price softness as a risk monitor for deals with geographic concentration in markets that saw rapid appreciation.

- **Housing Supply tab:** Persistent supply constraints support home prices and therefore collateral values underlying Non-QM deals. Real estate investor borrowers (a major Non-QM segment) are particularly sensitive to local supply dynamics — rent yield assumptions supporting DSCR loans depend on vacancy rates and rental demand, which are influenced by new housing supply.

## Sources Cited

- [09-kbra-non-qm-default-study.md](../raw/09-kbra-non-qm-default-study.md) — KBRA's decade-long study of 475,000+ Non-QM loans: CDR data, realized loss figures, vintage performance table, FICO/LTV/documentation risk factor analysis, and the ~300 involuntary liquidation severity figure
- [10-riskspan-non-qm-securitization-market.md](../raw/10-riskspan-non-qm-securitization-market.md) — RiskSpan market history framing the regulatory origins of Non-QM (post-QM rule exclusions), borrower segment taxonomy (self-employed, credit-blemished, investors, foreign nationals), market structure (non-bank originators backed by asset managers), and key investor diligence dimensions
- [11-morningstar-dbrs-non-qm-q4-2022.md](../raw/11-morningstar-dbrs-non-qm-q4-2022.md) — Morningstar DBRS Q4 2022 performance update confirming senior tranche resilience through the rate shock, sub spread widening dynamics, origination volume decline, and the structural lesson that sound underwriting sustains credit performance through rate cycles
