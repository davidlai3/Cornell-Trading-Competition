import pandas as pd

# Sample closing price data
closing_prices = [100.0, 102.5, 105.3, 108.6, 110.2, 112.8, 115.5, 118.4, 121.6, 124.0]

# Convert the list to a pandas Series for easier manipulation
price_series = pd.Series(closing_prices)

# Define the number of periods (n) for the SMA
n = 5

# Calculate the SMA using pandas' rolling() and mean() functions
sma = price_series.rolling(window=n, min_periods=1).mean()

# Print the SMA values
print("Simple Moving Average (SMA) for", n, "periods:")
print(sma)
