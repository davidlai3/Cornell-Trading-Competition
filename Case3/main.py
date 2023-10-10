"""
given:
time, bid, ask, bid_size, ask_size
"""

"""
output:
csv file with dataframe and position column
"""

import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta


b1 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures1.csv')
# b2 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures2.csv')
# b3 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures3.csv')
# b4 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures4.csv')
# b5 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures5.csv')
# b6 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures6.csv')
# b7 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures7.csv')
# b8 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures8.csv')
# b9 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures9.csv')
# b10 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures10.csv')
# b11 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures11.csv')
# b12 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures12.csv')
# b13 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures13.csv')
# b14 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures14.csv')
# b15 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures15.csv')
# b16 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures16.csv')
# b17 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures17.csv')
# b18 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures18.csv')
# b19 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures19.csv')
# b20 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures20.csv')
# b21 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures21.csv')
# b22 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures22.csv')
# b23 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures23.csv')
# b24 = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures24.csv')


# timestamps = b24["ts_event"].values
# timestamps = [datetime.utcfromtimestamp(ts / 1e9) for ts in timestamps]

# bid_prices = b24["bid_px_00"].values
# normalized_bid_prices = bid_prices / 1e12  # Divide by 1e12 to scale down

# N = 10
# normalized_bid_prices = normalized_bid_prices[::N]

# window_size = 10  # Adjust the window size
# smoothed_bid_prices = normalized_bid_prices.rolling(window=window_size).mean()

# plt.plot(timestamps[::N], smoothed_bid_prices)

# plt.xlabel('Time')
# plt.ylabel('Bid Price')
# plt.title('Time vs. Bid Price for Bitcoin Futures')

# plt.tight_layout()

# plt.show()



import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file into a DataFrame
data = pd.read_csv('CTC23_Blockchain_Data/BTC_Futures1.csv')

# Extract timestamp and bid price columns
timestamps = data['ts_event']
bid_prices = data['bid_px_00']

# Normalize bid prices (optional)
normalized_bid_prices = bid_prices / 1e12  # Divide by 1e12 to scale down

# Convert timestamps to datetime format
timestamps = [datetime.utcfromtimestamp(ts / 1e9) for ts in timestamps]

# Downsample data (plot every Nth data point)
N = 15  # Adjust N based on your preference
timestamps = timestamps[::N]
normalized_bid_prices = normalized_bid_prices[::N]

# Apply a simple moving average for smoothing (optional)
window_size = 10  # Adjust the window size
smoothed_bid_prices = normalized_bid_prices.rolling(window=window_size).mean()

# Create the time vs. price plot
plt.figure(figsize=(12, 6))
plt.plot(timestamps, smoothed_bid_prices, label='Bid Price (smoothed)', color='blue')
plt.xlabel('Time')
plt.ylabel('Bid Price (normalized)')
plt.title('Time vs. Bid Price for Bitcoin Futures')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
