# NBA Free Agent Value Board: Predicting Contract Efficiency and Future Production

## Overview
This project develops a predictive model to assess the fair market value of NBA free agents and project their future on-court production (VORP) for the 2026 free agency class. The goal is to provide a data-driven tool for General Managers (GMs) to identify potentially overpaid or underpaid players and optimize roster construction.

## Motivation
NBA free agency involves significant financial decisions based on player performance, potential, and market dynamics. Traditional scouting and negotiation can be enhanced by quantitative analysis. This project aims to:
- Predict player contract values as a percentage of the salary cap.
- Forecast future player impact (VORP - Value Over Replacement Player).
- Identify players who offer high production relative to their contract value.

## Data Sources
- **Basketball Reference:** Advanced player statistics for the 2022-2026 NBA seasons (`.html` scraping).
- **Spotrac:** NBA free agent contract data, including actual contract values for 2024-2026 free agent classes (`.xlsx` file).

## Methodology

### 1. Data Ingestion & Preprocessing
- **Advanced Stats:** Web scraped 5 years of advanced player statistics from Basketball Reference. Cleansed and standardized column names.
- **Contract Data:** Loaded free agent contract details from an Excel file. Cleaned and normalized player names and contract values.
- **Feature Engineering (Advanced Stats):** Created three-year rolling windows of player performance (e.g., 2022-2024 for 2024 free agents). Calculated minute-weighted averages for rate statistics and three-year cumulative totals for volume statistics (e.g., total minutes, total VORP).
- **Name Standardization:** Developed a `fix_name` utility to handle player name inconsistencies across datasets, crucial for accurate merging.
- **Target Variable Creation:** `aav_pct_cap` (Average Annual Value as a percentage of the salary cap) for contract prediction. `future_vorp_next_season` for future production prediction.
- **Data Merging:** Combined advanced stats with contract data based on player name and free agency year.

### 2. Exploratory Data Analysis (EDA)
- Inspected data distributions (`aav_pct_cap` showed a right-skewed distribution, as expected in professional sports salaries).
- Identified and handled missing values through imputation (median strategy).
- Assessed duplicate player-year entries to ensure data integrity.
- **Outlier Analysis:** High-value contracts were identified as outliers but retained, as they represent legitimate market-driving players essential for a comprehensive model.

### 3. Feature Selection
- **Lasso Regression:** Applied Lasso to `x_train` to identify and select the most impactful features for predicting contract value, eliminating less relevant ones.
- **Variance Inflation Factor (VIF):** Performed iterative VIF removal to address multicollinearity among the Lasso-selected features, ensuring model stability and interpretability.

### 4. Model Training & Evaluation
Multiple regression models were trained and evaluated:
- **Model 1: Contract Value Prediction (`aav_pct_cap`)**
    - Linear Regression (Baseline)
    - Ridge Regression
    - Random Forest Regressor
    - General Additive Model (GAM)
    - **Evaluation Metrics:** R-squared ($R^2$), Mean Absolute Error (MAE), and Spearman's Rank Correlation (for assessing ranking ability).

- **Model 2: Future Production Prediction (`future_vorp_next_season`)**
    - Ridge Regression (chosen for its performance and interpretability).
    - Gradient Boosting Regressor (tuned with RandomizedSearchCV).
    - **Evaluation Metrics:** $R^2$, MAE, RMSE, and Spearman's Rank Correlation against mean and latest VORP baselines.

### 5. Key Findings & Model Choice

**For Contract Value Prediction (Model 1):**
Ridge Regression was selected as the primary model due to its strong balance of:
- **Out-of-sample performance:** Smallest train-test gap.
- **Ranking ability:** Second strongest Spearman correlation (0.798) behind Random Forest, indicating reliable player ranking.
- **Interpretability:** Ridge provides clear coefficients for feature importance.
- **Test MAE:** Exhibited a low MAE of 0.0231, representing a small average dollar error on unseen players.

**For Future Production Prediction (Model 2):**
Ridge Regression demonstrated superior performance compared to simple baselines, effectively predicting next-season VORP with a validation Spearman correlation of 0.428.

**Overall Takeaway:** GAM showed the strongest training fit but the weakest test performance (test R² 0.267 vs. Ridge's 0.432), indicating overfitting on a limited sample — a key reason Ridge was chosen over more flexible alternatives.

### 6. Final Output: 2026 NBA Free Agent Value Board
Two models are combined to create a comprehensive value board for the 2026 free agent class:
- **Model 1 (Ridge):** Provides `Predicted AAV % Cap` and `Contract Evaluation` (Overpaid, Underpaid, Fair Value).
- **Model 2 (Ridge):** Provides `Predicted Future VORP`, `Future VORP Percentile`, and `Future Production Rank`.

A `Future VORP per 1% Cap` metric is also calculated, offering a direct measure of projected production efficiency per unit of cap space.

The final board is exported as `2026_free_agent_value_board_full.csv`.

### 7. Deployment Preparation
All essential models (Ridge for AAV and VORP) and preprocessing objects (scalers, imputers) are saved using `joblib` for future deployment and inference on new data. Key data preprocessing functions (`fix_name`, `clean_player_name`, `create_weighted_stats`) are also defined for portability.

## How to Use/Reproduce
1. Clone this repository.
2. Ensure you have the required Python libraries installed (see imports in the notebook).
3. Run the notebook cells sequentially to reproduce the analysis and generate the value board.

## Further Enhancements
- Incorporate salary cap projections and team-specific needs.
- Explore more advanced feature engineering, including player archetypes or stylistic metrics.
- Implement more sophisticated ensemble models or deep learning approaches.
- Integrate sentiment analysis from news or social media for qualitative factors.

## Live Demo
[HoopsValuePro — 2026 NBA Free-Agent Value Board](https://your-app-url.streamlit.app)
