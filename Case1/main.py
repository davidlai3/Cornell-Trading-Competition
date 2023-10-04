import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib as plt
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
            price_series = pd.Series(returns.values.tolist(), index=returns.index)

            # Number of periods for SMA 
            span_period = 5

            # Calculate SMA
            sma = price_series.rolling(window=span_period, min_periods=1).mean()
            
            ticker_trades = pd.DataFrame(columns = [ticker])
            for date in returns.index:
                if (returns[date] > sma[date]):
                    ticker_trades.loc[date] = 1
                elif (returns[date] < sma[date]):
                    ticker_trades.loc[date] = -1
                else:
                    # TODO: Set to 0 but do not get divide by zero error
                    ticker_trades.loc[date] = -1
    trading_list = pd.concat([trading_list, ticker_trades], axis=1)
    trading_list_one = trading_list.sub(trading_list.mean(axis=1), axis=0)
    trading_list_norm = trading_list_one.div(trading_list_one.abs().sum(axis=1), axis=0)
    return trading_list_norma

trading_list = momentum_trading_strat(portfolio, '2015-01-01', '2023-01-01')
print(trading_list)



