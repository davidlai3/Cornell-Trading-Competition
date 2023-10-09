import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from collections import defaultdict
import math
import matplotlib.pyplot as plt

emerging_market_countries = ['BRA','MEX','IND','CHN','ZAF']
developed_market_countries = ['USA','JPN','DEU','GBR','FRA']


portfolio = {
    'BRA': ['PBR', 'VALE', 'ITUB', 'NU', 'BSBR'],
    'MEX': ['AMX','KCDMY','VLRS','ALFAA.MX','BBAJIOO.MX'],
    'IND': ['RELIANCE.NS','TCS', 'HDB', 'INFY', 'ADANIENT.NS'],
    'USA': ['AAPL', 'MSFT','GOOG','AMZN','NVDA']
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


def momentum_trading_strat(portfolio, start_date, end_date):
    data = get_data(portfolio, start_date, end_date)
    trading_list = pd.DataFrame(columns = data.columns.levels[2])
    
    for country in data.columns.levels[0]:
        for ticker in data[country]['Adj Close'].columns:
            returns = data[country]['Adj Close'][ticker]

            # Convert closing prices to pandas series for easier manipulation
            price_series = pd.Series(returns.values.tolist(), index=returns.index.tolist())
            trading_list[ticker] = price_series
    return trading_list

def predict_data(dataframe):
    results = arima(dataframe)
    return results.forecast()

def arima(dataframe):
    p = 1
    d = 1
    q = 1
    model = ARIMA(dataframe, order=(p, d, q))
    results = model.fit()
    return results

trading_list = momentum_trading_strat(portfolio, '2015-01-01', '2023-01-01')
print(trading_list)

results = arima(trading_list['AAPL'])
forecast = results.forecast()
print(forecast)


