import pandas as pd
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Directory where your CSV files are stored
data_directory = "CTC23_Blockchain_Data"

# Get a list of CSV files in the directory
csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]

# Initialize an empty list to store DataFrames from each CSV
data_frames = []

# Load and concatenate data from each CSV file
for csv_file in csv_files:
    file_path = os.path.join(data_directory, csv_file)
    df = pd.read_csv(file_path)
    data_frames.append(df)

# Concatenate all DataFrames into a single DataFrame
data = pd.concat(data_frames, ignore_index=True)

# Now you can proceed with feature engineering, preprocessing, and modeling using combined_data

# Feature Engineering: Extract relevant features
def make_prediction(data):
  # Feature Engineering: Extract relevant features
  data['price_diff'] = data['ask_px_00'] - data['bid_px_00']

  # Define the target variable
  data['action'] = np.where(data['price_diff'] > 0, 1, np.where(data['price_diff'] < 0, -1, 0))

  # Split the data into training and testing sets
  X = data[['price_diff', 'bid_sz_00', 'ask_sz_00']]
  y = data['action']

  # Train a machine learning model (in this case, a Decision Tree Classifier)
  model = DecisionTreeClassifier(random_state=42)
  model.fit(X, y)

  # Make predictions
  predictions = model.predict(X)

  return predictions

positions = []
profits = []
position = 0
profit = 0

# Get machine learning predictions
predictions = make_prediction(data)

# Modify the trading logic based on machine learning predictions
for prediction in predictions:
    if prediction == 1:  # Buy
        if position == -1:
            profit += data['bid_px_00']  # Cover short position
        position = 1  # Go long
    elif prediction == -1:  # Sell
        if position == 1:
            profit -= data['ask_px_00']  # Sell the position
        position = -1  # Go short
    else:  # Neutral
        if position == 1:
            profit -= data['ask_px_00']  # Sell to return to neutral
        elif position == -1:
            profit += data['bid_px_00']  # Cover short to return to neutral
        position = 0  # Stay neutral

    profits.append(profit)
    positions.append(position)

# Create a new DataFrame with date and position columns
result_df = data[['ts_event']].copy()
result_df['position'] = positions

# Save the results to a CSV file
result_df.to_csv("bitcoin_trading_results_ml.csv", index=False)

# Calculate the final profit
final_profit = profit
print("Final Profit:", final_profit)
