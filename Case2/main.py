"""
given:
- close, open, high, low of VIX and SPX index
- option contracts with timedate, strike price, expiration, bid, ask
- option instruments
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


def get_index_data():

    df_SPX = pd.read_csv('Data/S_P 500 data.csv')
    df_VIX = pd.read_csv('Data/VIX data.csv')

    return df_SPX, df_VIX


def get_option_data():

    df_SPX_OPTIONS = pd.read_csv('Data/SPX options.csv')
    df_VIX_OPTIONS = pd.read_csv('Data/VIX options.csv')

    return df_SPX_OPTIONS, df_VIX_OPTIONS


def get_instrument_data():

    df_SPX_INSTRUMENT = pd.read_csv('Data/SPX options instrument ids.csv')
    df_VIX_INSTRUMENT = pd.read_csv('Data/VIX options instrument ids.csv')

    return df_SPX_INSTRUMENT, df_VIX_INSTRUMENT


"""
display graph of s&p and vix v date based on close
"""
def graph_indexes(df_SPX, df_VIX):

    x = df_SPX['date'].values
    y_SPX = df_SPX['close'].values
    y_VIX = df_VIX['close'].values

    plt.subplot(2, 1, 1)
    plt.plot(x, y_SPX)
    plt.title('S&P')

    plt.subplot(2, 1, 2) 
    plt.plot(x, y_VIX)
    plt.title('VIX')

    plt.tight_layout()

    plt.show()


def main():

    df_SPX, df_VIX = get_index_data()

    graph_indexes(df_SPX, df_VIX)


if __name__ == '__main__':
    main()

