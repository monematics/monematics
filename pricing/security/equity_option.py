import datetime

from pricing.market_data_obj.equity_quote import OptionQuote
from pricing.security.security_interface import Option


class EquityOption(Option):
    supported_methods = ["list", "PV", "delta", "gamma", "vega", "rho", "exdate"]

    def calc_pv(self, market_data):
        pass

    def is_supported_method(self, method):
        pass

    def evaluate(self, method, market_data):
        # for non pv method first

        # then for pv method
        pass

    def __init__(self, strike: float, expiry: datetime.date, option_quote: OptionQuote, opt_type="Call"):
        self.strike = strike
        self.expiry = expiry
        if opt_type == "Call":
            self.type = 1
        elif opt_type == "Put":
            self.type = -1

        self.underlying = option_quote.get_underlying_quote()
        self.quote_price = option_quote.get_option_quote_price()
        self.quote_implied_vol = option_quote.get_option_quote_IV()

        # initialize some intermediate result
