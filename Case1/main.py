import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import datetime, timedelta
from collections import defaultdict
import math
import matplotlib.pyplot as plt

emerging_market_countries = ['BRA','MEX','IND','CHN','ZAF']
developed_market_countries = ['USA','JPN','DEU','GBR','FRA']


portfolio = {
    'BRA': ['PBR', 'VALE']
    #'BRA': ['PBR', 'VALE', 'ITUB', 'NU', 'BSBR'],
    #'MEX': ['AMX','KCDMY','VLRS','ALFAA.MX','BBAJIOO.MX'],
    #'IND': ['RELIANCE.NS','TCS', 'HDB', 'INFY', 'ADANIENT.NS'],
    #'USA': ['AAPL', 'MSFT','GOOG','AMZN','NVDA']
}

def get_data(portfolio, start_date, end_date):
    data = pd.DataFrame()
    
    columns = []

    for country, tickers in portfolio.items():
        # Download data for each ticker
        df = yf.download(tickers, start=start_date, end=end_date)

        # Extract columns representing stock attributes (e.g. 'Open', 'Close', 'Volume')
        stock_attributes = df.columns.levels[0]

        # Extend columns with country and attribute prefixes
        country_columns = [(country, attr, ticker) for ticker in tickers for attr in stock_attributes]
        columns.extend(country_columns)

        # Concatenate dataframes
        data = pd.concat([data, df], axis=1)

    data.columns = pd.MultiIndex.from_tuples(columns, names=['country', 'attribute', 'ticker'])
    return data


def strategy(portfolio, start_date, end_date):
    data = get_data(portfolio, start_date, end_date)
    # Add tickers to dataframes
    return_list = pd.DataFrame(columns = data.columns.levels[2])

    for country in data.columns.levels[0]:
        for ticker in data[country]['Adj Close'].columns:
            returns = data[country]['Adj Close'][ticker]

            # Convert closing prices to pandas series for easier manipulation
            actual_prices = pd.Series(returns.values.tolist(), index=returns.index.tolist())
            model, model_data = fit_arima(portfolio, country, ticker, start_date)
            
            predicted_vals = []
            for date in returns.index.to_list():
                predicted = predict_next(model)
                predicted_vals.append(predicted)
                # If ARIMA model predicts increase, then long the stock
                if predicted > actual_prices[0]:
                    return_list.loc[pd.to_datetime(date).strftime('%Y-%m-%d'), ticker] = 1
                    
                # If ARIMA model predicts decrease, then short the stock
                elif predicted < actual_prices[0]:
                    return_list.loc[pd.to_datetime(date).strftime('%Y-%m-%d'), ticker] = -1

                model_data.loc[returns.index[-1] + pd.DateOffset(days=1)] = actual_prices[0] 
                actual_prices = actual_prices[1:]2015-01-02    2.711913

                model = arima(model_data)
    return normalize_returns(return_list, data)


# @Returns: ARIMA model and returns (pandas series)
def fit_arima(portfolio, country, ticker, start_date):
    stripped = datetime.strptime(start_date, '%Y-%m-%d')
    nstart = stripped - timedelta(days=20)
    data = get_data(portfolio, nstart, start_date)
    returns = data[country]['Adj Close'][ticker]
    returns = pd.Series(returns.values.tolist(), index=returns.index.tolist())
    return arima(returns), returns



# @Returns: Float value representing the predicted value of the next day
def predict_next(model):
    forecast = model.forecast()
    return forecast[forecast.keys()[-1]]


def arima(time_series):
    p = 5
    d = 1
    q = 0
    model = ARIMA(time_series, order=(p, d, q))
    results = model.fit()
    return results


def normalize_returns(return_list, data):

    normalized_data = pd.DataFrame(columns = data.columns.levels[2])
    # Convert return_list to list of integers
    numbers = return_list.values.tolist()

    # Normalize returns
    for ticker in return_list.columns:
        numbers = return_list[ticker].values.tolist()
        count_minus1 = numbers.count(-1)
        count_1 = numbers.count(1)

        scale_factor = 1 / (count_minus1 + count_1)

        mapped_numbers = [-1 * scale_factor if x == -1 else 1 * scale_factor for x in numbers]

        new_series = pd.Series(mapped_numbers, index=return_list.index)
        return_list[ticker] = new_series

    return return_list


return_list = strategy(portfolio, '2023-01-01', '2023-01-30')
