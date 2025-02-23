from pricing_src.market_data_obj.market_data_interface import MarketData
from pricing_src.security.security_interface import Security


def Ev(sec: Security, method: str, market_data: MarketData):
    """
    interface function to evaluate for a security
    :param sec:
    :param method:
    :param market_data: list of market data
    :return:
    """
    return sec.evaluate(method, market_data)


def CreateEquityOption(**kwargs):
    """
    interface function to create option object
    :param kwargs:
    :return:
    """
    # parse the input and create the equity option
    return
