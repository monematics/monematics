import yfinance as yf
import pandas as pd
import os
import datetime
from stock_data_utils import *

SAVE_PATH = os.path.join(os.path.dirname(__file__), 'static_data')


def get_daily_prices(tickers: list,
                     start_date: datetime.date = None,
                     end_date: datetime.date = None) -> pd.DataFrame:
    """
    ths will return dataframe of stocks daily adjClose prices
    currently impl save the data locally and load from local file, only mimicking a backend
    TODO : may need to change this when there is a backend
    :param tickers: list of tickers
    :param start_date: optional
    :param end_date: optional
    :return: adjClose price from yfinance
    """

    check_tickers_validity(tickers)

    # two routines
    # one already has that prices file locally
    # other is load from yfinance and save locally
    output = dict()
    for ticker in tickers:
        price_file_name = ticker + '.csv'
    try:
        ticker_info = yf.Ticker(tickers).info
    except Exception:
        raise Exception("Invalid Ticker")

    # if ticker_info.info is None:

    stock_obj = yf.Ticker(tickers)
    pass


if __name__ == '__main__':
    #msft = get_daily_prices('msft')
    data = yf.download('msft')

