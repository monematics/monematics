def check_tickers_validity(tickers):
    """
    error handling of list of tickers param
    :param tickers:
    :return: throws
    """
    # check the tickers type, has to be list of str and non-empty
    if type(tickers) is not list:
        raise Exception("get_daily_prices:: Tickers need to be of type list")

    if len(tickers) == 0:
        raise Exception("get_daily_prices:: Empty tickers")

    for s in tickers:
        if type(s) is not str:
            raise Exception("get_daily_prices:: ticker need to be of type str")
