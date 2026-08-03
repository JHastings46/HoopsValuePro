# NBA Free Agent Value Board: Predicting Contract Efficiency and Future Production

# HoopsValuePro: NBA Free Agent Contract & Production Modeling

## Overview
This project builds a dual-model decision support framework for evaluating NBA 
free agent signings. It predicts both what a player will get paid (as a 
percentage of the salary cap) and how much he will actually produce (VORP), 
then combines both outputs to flag players who represent surplus value or 
overpayment risk. Built specifically around the 2026 NBA free agency class.

## Live Demo
[HoopsValuePro — 2026 NBA Free-Agent Value Board](https://hoopsvaluepro-rn664qf9eyfcjykp8ufzzx.streamlit.app/)

## Motivation
NBA free agency involves significant financial decisions made under uncertainty. 
Traditional scouting and negotiation benefit from quantitative guardrails. This 
project answers three questions a GM actually asks:
- What will this player command on the open market?
- How much will he actually produce next season?
- Is this contract worth it relative to projected output?

## Data Sources
- **Basketball Reference:** Advanced player statistics for the 2022–2026 NBA 
  seasons scraped via HTML, including PER, VORP, Win Shares, BPM, usage rate, 
  and true shooting percentage.
- **Spotrac:** NBA free agent contract data for the 2024–2026 classes including 
  AAV as a percentage of the salary cap. Sourced manually as an Excel file.

> **Note:** The Spotrac contract file must be sourced manually from Spotrac.com 
> and placed in the project root directory before running the notebook.

## Methodology

### 1. Data Ingestion & Preprocessing
- Scraped five years of advanced player statistics from Basketball Reference
- Constructed three-year rolling performance windows per free agency year 
  (e.g., 2022–2024 stats feed 2024 free agency predictions)
- Calculated minute-weighted averages for rate statistics and cumulative totals 
  for volume statistics
- Developed a `fix_name` utility to standardize player names across datasets
- Merged advanced stats with contract data on player name and free agency year

### 2. Exploratory Data Analysis
- Assessed distributions, missing values, and duplicate entries
- `aav_pct_cap` showed expected right skew consistent with NBA salary structures
- High-value outlier contracts retained as legitimate market-driving observations

### 3. Feature Selection
- **Lasso Regression:** Applied to training data to identify impactful features 
  and eliminate weaker predictors
- **Variance Inflation Factor (VIF):** Iterative removal of multicollinear 
  features among Lasso survivors to ensure model stability

### 4. Model Training & Evaluation

**Model 1 — Contract Value Prediction (aav_pct_cap)**

Four models compared: Linear Regression, Ridge Regression, Random Forest, GAM

| Metric    | Linear | Ridge  | RF Tuned | GAM    |
|-----------|--------|--------|----------|--------|
| Train R²  | 0.651  | 0.598  | 0.570    | 0.716  |
| Test R²   | 0.435  | 0.430  | 0.322    | 0.268  |
| Train MAE | 0.0233 | 0.0227 | 0.0212   | 0.0206 |
| Test MAE  | 0.0243 | 0.0231 | 0.0237   | 0.0236 |
| Spearman  | 0.769  | 0.798  | 0.827    | 0.729  |
| P-value   | 0.000  | 0.000  | 0.000    | 0.000  |

**Ridge selected** for its best balance of test R², lowest MAE, and strong 
Spearman (0.798). Random Forest had the highest Spearman (0.827) but the 
largest train-test gap (0.570 → 0.322), indicating overfitting. GAM showed 
the strongest training fit but weakest test performance, also indicating 
overfitting on a limited sample.

**Model 2 — Future Production Prediction (future_vorp_next_season)**

Ridge Regression selected after comparison against Gradient Boosting.

| Model              | Test R²  | MAE   | Spearman |
|--------------------|----------|-------|----------|
| Ridge              | 0.109    | 0.433 | 0.428    |
| Naive Mean Baseline| -0.004   | 0.451 | 0.670    |
| Recency Baseline   | -0.153   | 0.491 | 0.625    |

While the production model explains limited variance in absolute terms, it 
outperforms both a naive mean baseline and a single-season recency baseline, 
demonstrating that recent single-season production alone is a worse predictor 
than a multi-year model incorporating age and usage trends.

### 5. Final Output: 2026 NBA Free Agent Value Board
The two models are combined into a single value board for the 2026 class:
- **Contract Evaluation:** Predicted AAV % Cap vs. actual — flagged as 
  Overpaid, Underpaid, or Fair Value
- **Production Forecast:** Predicted Future VORP, VORP Percentile, 
  Future Production Rank
- **Efficiency Metric:** Future VORP per 1% Cap — projected production 
  per unit of cap space committed

Final board exported as `2026_free_agent_value_board_full.csv`

## How to Reproduce
```bash
# Requirements
Python 3.9+

pip install pandas numpy scikit-learn scipy joblib streamlit requests \
beautifulsoup4 openpyxl pyGAM
```
1. Clone this repository
2. Place your Spotrac contract Excel file in the project root directory
3. Run the notebook cells sequentially to reproduce the analysis
4. Launch the Streamlit app locally with `streamlit run app.py`

## Further Enhancements
- Incorporate salary cap projections and team-specific roster needs
- Add player archetype or positional style features
- Explore ensemble models combining contract and production predictions
- Integrate injury history and minutes restrictions as risk features
