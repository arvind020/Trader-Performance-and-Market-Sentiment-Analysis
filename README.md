# Trader-Performance-and-Market-Sentiment-Analysis
This repository contains a Python script to analyze the relationship between trader performance and market sentiment. The script processes Excel datasets, performs statistical analysis, and generates visualizations to uncover patterns and deliver insights for smarter trading strategies.

## Purpose
The goal is to explore how market sentiment (e.g., fear vs. greed) correlates with trader performance metrics such as profit/loss (PnL), win rate, and trading volume. This analysis aims to identify hidden patterns and suggest data-driven trading strategies.

## Requirements
- **Python 3.x**
- Required libraries:
  - `pandas` (for data manipulation)
  - `seaborn` (for statistical visualizations)
  - `matplotlib` (for plotting)
  - `scipy` (for statistical tests)
- Install dependencies using:
    pip install pandas seaborn matplotlib scipy


Datasets

Sentiment Data: fear_greed_index.xlsx (converted from .csv to .xlsx extension for ease of handling)

Columns: timestamp, value, classification, date
Source: Daily Bitcoin Fear & Greed Index (e.g., from alternative.me), with value (0-100) and classification (e.g., "Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed").


Trades Data: historical_data.xlsx (converted from .csv to .xlsx extension for ease of handling)

Columns: Account, Coin, Execution Price, Size Tokens, Size USD, Side, Timestamp IST, Start Position, Direction, Closed PnL, Transaction Hash, Order ID, Crossed Fee, Trade ID, Timestamp
Source: Historical trade data from Hyperliquid, with Closed PnL as profit/loss and Size USD as trade volume.


Both files should be placed at a suitable location to be used in the code.

Procedure
1. Data Loading and Preparation

Step: Load the Excel files into pandas DataFrames.
Process:

Read fear_greed_index.xlsx into sentiment and historical_data.xlsx into trades.
Convert date columns to datetime format:

sentiment['date'] uses '%m-%d-%Y' format.
trades['date'] extracts the date from Timestamp IST (e.g., MM-DD-YYYY HH:MM:SS to MM-DD-YYYY).

Purpose: Ensures consistent date handling for merging and analysis.

2. Data Transformation

Step: Transform and align the datasets.
Process:

Map classification to numeric values (e.g., "Extreme Fear" = 1, "Fear" = 2, ..., "Extreme Greed" = 5) into a new column class_numeric, filling missing values with -1.
Align datasets by finding the overlapping date range (min_date to max_date) and filter both DataFrames accordingly.
Check for sufficient data points (at least 2 rows in each dataset).

Purpose: Prepares data for numerical analysis and ensures compatibility between datasets.

3. Data Aggregation

Step: Aggregate trade data to daily metrics.
Process:

Group trades by date and calculate:

total_pnl: Sum of Closed PnL.
num_trades: Count of trades.
win_rate: Percentage of trades with positive Closed PnL (handled for empty groups with 0).
total_volume: Sum of Size USD.

Reset index for merging.


Purpose: Converts per-transaction data to daily summaries matching sentiment granularity.

4. Data Merging

Step: Combine aggregated trades with sentiment data.
Process:

Use pd.merge with inner join on date to create merged DataFrame.
Check that merged has at least 2 rows to ensure sufficient data for analysis.

Purpose: Links daily trader performance with corresponding sentiment values.

5. Statistical Analysis

Step: Perform correlation and grouped statistics.
Process:

Compute a correlation matrix for total_pnl, win_rate, total_volume, value, and class_numeric.
Calculate Pearson correlation and p-value specifically for total_pnl vs. value.
Group merged by classification to compute average total_pnl, win_rate, and total_volume.

Purpose: Quantifies relationships (e.g., negative correlation suggests better PnL in fear) and compares performance across sentiment states.

6. Visualization

Step: Generate plots to visualize insights.
Process:

Box Plot: sns.boxplot shows total_pnl distribution by classification, with rotated labels for readability.
Scatter Plot: plt.scatter plots value vs. total_pnl, colored by class_numeric, with a neutral threshold line at 50.
Bar Plot: sns.barplot displays average win_rate by classification, with standard deviation error bars.
Heatmap: sns.heatmap visualizes the correlation matrix with annotations.
Stacked Area Plot: pivot_volume.plot.area shows total_volume contribution by classification over time.

Purpose: Provides visual confirmation of statistical findings, highlighting trends, distributions, and sentiment-driven volume shifts.

Outputs

Console Output:

Correlation matrix table.
Specific total_pnl vs. value correlation with p-value.
Grouped statistics table by classification.

Plots:

Box plot: PnL spread by sentiment.
Scatter plot: Sentiment vs. PnL with classification colors.
Bar plot: Win rate by sentiment.
Heatmap: Correlation visualization.
Stacked area plot: Volume by sentiment over time.

Insights: Depends on data (e.g., higher PnL in fear, lower in greed), guiding contrarian strategies.

Potential Issues and Solutions

Date Mismatch: If merged has <2 rows, check overlapping dates in both files. Adjust ranges or add data.
Column Errors: Verify Closed PnL and Size USD match your Excel headers; update if needed (e.g., Closed P&L).
Insufficient Data: Ensure both Excel files have multiple rows; add more data if necessary.

Extensions

Additional Plots: Consider adding a rolling average line plot or a volume trend by side (Buy/Sell).
Modeling: Implement a simple regression or machine learning model (e.g., with scikit-learn) to predict PnL from sentiment.
Automation: Use a scheduler to update data daily and rerun analysis.

Usage

Install required libraries.
Place fear_greed_index.xlsx and historical_data.xlsx in the specified directory.
Run the script in a Python environment (e.g., Jupyter Notebook or IDE). I used Spyder IDE.
Review console outputs and generated plots for insights.

Contact
For questions or contributions, contact the author at arvind.bull@gmail.com/arvindmurali2002@hotmail.com (if applicable).
Last Updated
September 09, 2025, 01:29 PM IST

