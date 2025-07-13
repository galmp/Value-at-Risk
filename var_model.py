import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Download stock data
tickers = ['AAPL', 'MSFT', 'JPM']
data = yf.download(tickers, start='2023-01-01', end='2025-01-01', auto_adjust=False)

# Debug: Print column names to verify structure
print("Columns in data:", data.columns)

# Step 2: Extract Adjusted Close prices from MultiIndex
adj_close = data.xs('Adj Close', level='Price', axis=1).copy()  # Extract 'Adj Close' for all tickers

# Calculate daily returns
returns = adj_close.pct_change().dropna()

# Step 3: Create portfolio
weights = np.array([0.4, 0.4, 0.2])  # Weights: 40% AAPL, 40% MSFT, 20% JPM
portfolio_returns = returns.dot(weights)

# Step 4: Calculate VaR (Historical Method)
confidence_level_95 = 0.05
confidence_level_99 = 0.01
var_95 = np.percentile(portfolio_returns, 100 * confidence_level_95)
var_99 = np.percentile(portfolio_returns, 100 * confidence_level_99)
print(f"95% VaR: {-var_95 * 100:.2f}%")
print(f"99% VaR: {-var_99 * 100:.2f}%")

# Step 5: Monte Carlo Simulation
n_simulations = 10000
n_days = 1  # 1-day VaR
mean_return = portfolio_returns.mean()
std_return = portfolio_returns.std()
simulated_returns = np.random.normal(mean_return, std_return, n_simulations)
simulated_var_95 = np.percentile(simulated_returns, 100 * confidence_level_95)
simulated_var_99 = np.percentile(simulated_returns, 100 * confidence_level_99)
print(f"Monte Carlo 95% VaR: {-simulated_var_95 * 100:.2f}%")
print(f"Monte Carlo 99% VaR: {-simulated_var_99 * 100:.2f}%")

# Step 6: Calculate Expected Shortfall (ES)
es_95 = np.mean(portfolio_returns[portfolio_returns <= np.percentile(portfolio_returns, 100 * confidence_level_95)])
es_99 = np.mean(portfolio_returns[portfolio_returns <= np.percentile(portfolio_returns, 100 * confidence_level_99)])
print(f"95% Expected Shortfall: {-es_95 * 100:.2f}%")
print(f"99% Expected Shortfall: {-es_99 * 100:.2f}%")

# Step 7: Visualization
plt.figure(figsize=(10, 6))
plt.hist(portfolio_returns, bins=50, alpha=0.7, color='blue', label='Portfolio Returns')
plt.axvline(-var_95, color='red', linestyle='--', label='95% VaR (Historical)')
plt.axvline(-var_99, color='darkred', linestyle='--', label='99% VaR (Historical)')
plt.axvline(-simulated_var_95, color='green', linestyle=':', label='95% VaR (Monte Carlo)')
plt.axvline(-simulated_var_99, color='darkgreen', linestyle=':', label='99% VaR (Monte Carlo)')
plt.axvline(-es_95, color='orange', linestyle='-.', label='95% ES (Historical)')
plt.axvline(-es_99, color='darkorange', linestyle='-.', label='99% ES (Historical)')
plt.title('Portfolio Returns Distribution and VaR/ES')
plt.xlabel('Daily Returns')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.savefig('var_plot.png')  # Save for GitHub
plt.show()