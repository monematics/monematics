"""
market stock quote class
TODO: might want to distinguish single name and indices, currently only single stock
"""
from src.pricing.market_data_obj.market_data_interface import MarketData


class StockQuote(MarketData):
    """
    stock quote class to store observed market price for a stock
    """

    def __init__(self, ticker, price, name=''):
        self.__ticker = ticker
        self.__price = price
        if name != '':
            self.__name = name
        else:
            self.__name = ticker

    def get_quote_price(self):
        return self.__price

    def set_stock_quote(self, quote_price):
        self.__price = quote_price

    def get_mkt_data_type(self):
        return "StockQuote"


class OptionQuote(MarketData):
    """
    option quote class to store market price and implied vol if observed any
    """

    def __init__(self, stock_quote: StockQuote, option_price: float = None, implied_vol: float = None):
        self.__stock_quote = stock_quote
        self.__option_price = option_price
        self.__implied_vol = implied_vol

    def get_underlying_quote(self):
        return self.__stock_quote

    def set_underlying_quote(self, stock_quote):
        self.__stock_quote = stock_quote

    def get_option_quote_price(self):
        return self.__option_price

    def set_option_quote_price(self, price):
        self.__option_price = price

    def get_option_quote_IV(self):
        return self.__implied_vol

    def set_option_quote_IV(self, implied_vol):
        self.__implied_vol = implied_vol

    def get_mkt_data_type(self):
        return "OptionQuote"
