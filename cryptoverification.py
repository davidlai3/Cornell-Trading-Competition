#!/usr/bin/env python3

import numpy as np
import pandas as pd

# input is the list of dates inputted to competitor
# output is the user output of buy/sell/neurtral
def check_crypto_output(marketdata, positions):
    # checking if positions is a dataframe
    assert isinstance(positions, pd.DataFrame), "positions should be a dataframe"

    assert "DATETIME" in positions.columns, "positions dataframe does not have 'DATETIME' column, please read naming specifications"

    # checks whether every value in 'DATETIME' is a datetime object
    assert positions['DATETIME'].apply(lambda x: isinstance(x, pd.Timestamp)).all(), "every element in 'DATATIME' column of positions should be a datatime object"

    # checking if right number of dates, and that they are equal
    assert marketdata['ts_recv'].equals(positions['DATETIME']), "the 'DATETIME' column of positions should match 'ts_recv' of marketdata column"
    
    # checking if all outputs are valid
    assert all(positions['POSITION'].isin([-1, 0, 1])), "all values in 'DATETIME' column need to be either -1, 0 or 1"
