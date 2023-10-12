import pandas as pd
import numpy as np

data = pd.read_csv("CTC23_Blockchain_Data/BTC_Futures1.csv")

positions = []
profits = []
position = 0
profit = 0

def make_prediction(bid_price, ask_price):
    if bid_price < ask_price:
        return 1
    elif bid_price > ask_price:
        return -1
    else:
        return 0

for index, row in data.iterrows():
    bid_price = row['bid_px_00']
    ask_price = row['ask_px_00']
    
    prediction = make_prediction(bid_price, ask_price)
    
    if prediction == 1:
        if position == -1:
            profit += bid_price
        position = 1
    
    elif prediction == -1:
        if position == 1:
            profit -= ask_price
        position = -1
    
    elif prediction == 0:
        if position == 1:
            profit -= ask_price
        elif position == -1:
            profit += bid_price
        position = 0
    
    profits.append(profit)
    positions.append(position)

result_df = data[['ts_event']].copy()
result_df['position'] = positions

result_df.to_csv("bitcoin_trading_results.csv", index=False)

final_profit = profit
print("Final Profit:", final_profit)
