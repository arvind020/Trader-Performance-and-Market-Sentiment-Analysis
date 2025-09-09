import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

sentiment = pd.read_excel('C:/Users/arvin/OneDrive/Desktop/fear_greed_index.xlsx')  
trades = pd.read_excel('C:/Users/arvin/OneDrive/Desktop/historical_data.xlsx') 

sentiment['date'] = pd.to_datetime(sentiment['date'], format='%m-%d-%Y')
trades['date'] = pd.to_datetime(trades['Timestamp IST']).dt.date  
trades['date'] = pd.to_datetime(trades['date'])

class_map = {'Extreme Fear': 1, 'Fear': 2, 'Neutral': 3, 'Greed': 4, 'Extreme Greed': 5}
sentiment['class_numeric'] = sentiment['classification'].map(class_map).fillna(-1)  

min_date = max(sentiment['date'].min(), trades['date'].min())
max_date = min(sentiment['date'].max(), trades['date'].max())
sentiment = sentiment[(sentiment['date'] >= min_date) & (sentiment['date'] <= max_date)]
trades = trades[(trades['date'] >= min_date) & (trades['date'] <= max_date)]

if len(sentiment) < 2 or len(trades) < 2:
    raise ValueError("Insufficient data points in one or both datasets. Please check your Excel files for more rows.")

daily_trades = trades.groupby('date').agg(
    total_pnl=('Closed PnL', 'sum'),
    num_trades=('Closed PnL', 'count'),
    win_rate=('Closed PnL', lambda x: (x > 0).mean() * 100 if len(x) > 0 else 0),  
    total_volume=('Size USD', 'sum')
).reset_index()

merged = pd.merge(daily_trades, sentiment, on='date', how='inner')

if len(merged) < 2:
    raise ValueError("Merged dataset has fewer than 2 points. Check for date mismatches or insufficient overlapping data.")

corr = merged[['total_pnl', 'win_rate', 'total_volume', 'value', 'class_numeric']].corr()
print("Correlation Matrix:")
print(corr)
corr_coef, p_value = pearsonr(merged['total_pnl'], merged['value'])
print(f"Correlation between PnL and Sentiment: {corr_coef:.4f} (p-value: {p_value:.4f})")

grouped = merged.groupby('classification').agg(
    avg_pnl=('total_pnl', 'mean'),
    avg_win_rate=('win_rate', 'mean'),
    avg_volume=('total_volume', 'mean')
).reset_index()
print("\nGrouped Statistics by Classification:")
print(grouped)

plt.figure(figsize=(10, 6))
sns.boxplot(x='classification', y='total_pnl', data=merged)
plt.title('PnL Distribution by Sentiment Classification')
plt.xlabel('Sentiment Classification')
plt.ylabel('Total Daily PnL')
plt.xticks(rotation=45)  
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(merged['value'], merged['total_pnl'], alpha=0.5, c=merged['class_numeric'], cmap='viridis')
plt.colorbar(label='Classification (1-5)')
plt.xlabel('Sentiment Value')
plt.ylabel('Total Daily PnL')
plt.title('Sentiment Value vs. Total Daily PnL')
plt.axvline(x=50, color='red', linestyle='--', label='Neutral Threshold')
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='classification', y='win_rate', data=merged, estimator='mean', ci='sd')
plt.title('Average Win Rate by Sentiment Classification')
plt.xlabel('Sentiment Classification')
plt.ylabel('Average Win Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(merged[['total_pnl', 'win_rate', 'total_volume', 'value', 'class_numeric']].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Heatmap of Performance Metrics and Sentiment')
plt.tight_layout()
plt.show()

pivot_volume = merged.pivot_table(values='total_volume', index='date', columns='classification', fill_value=0)
plt.figure(figsize=(12, 6))
pivot_volume.plot.area(stacked=True, figsize=(12, 6))
plt.title('Trading Volume by Sentiment Classification Over Time')
plt.xlabel('Date')
plt.ylabel('Total Volume (USD)')
plt.legend(title='Classification')
plt.tight_layout()
plt.show()