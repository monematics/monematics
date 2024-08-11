import datetime

from pricing_src.market_data_obj.market_data_interface import MarketData

TODAY = datetime.date.today()


class Curve(MarketData):

    def __init__(self, bmnames, bmrates, curve_date=TODAY):
        """
        constructor
        :param bmnames:
        :param bmrates:
        :param curve_date:
        """
        if len(bmnames) != len(bmrates):
            assert "different length for benchmark rates and benchmark names"
        self.__bmnames = bmnames
        self.__bmrates = bmrates
        self.__curve_date = curve_date
        self.__bm_in_yr_frac = self.BMInYrFrac()
        self.__bm_df = self.__calc_benchmark_df()
        pass

    def df(self, fut_date):
        """
        Calculate a discount factor from future date to today
        :param fut_date:
        :return:
        """
        assert (fut_date - TODAY) / 365 > 2, "This is a short end curve"
        pass

    def rate(self, start, end):
        """
        Calculates a forward projected rate between start and end
        :param start:
        :param end:
        :return:
        """
        pass

    def BMNames(self):
        """
        getter for benchmark names
        :return:
        """
        return self.__bmnames

    def BMRates(self):
        """
        getter for corresponding benchmark rates
        :return:
        """
        return self.__bmrates

    def BMInYrFrac(self):
        """
        convert benchmark mark names to year fractions, ex. '1Y' = 1.
        :return:
        """
        bm_in_yr_frac = []
        for benchmark in self.__bmnames:
            amt_part, yr_part = self.split_benchmark(benchmark)
            if yr_part == 'b':
                bm_in_yr_frac.append(amt_part / 365.25)
            elif yr_part == 'w':
                bm_in_yr_frac.append(amt_part * 7 / 365.25)
            elif bm_in_yr_frac == 'm':
                bm_in_yr_frac.append(amt_part / 12.)
            else:
                bm_in_yr_frac.append(amt_part)
        return bm_in_yr_frac

    def Today(self):
        """
        return the curve date
        :return:
        """
        return self.__curve_date

    def __calc_benchmark_df(self):
        """
        convert benchmark rates to a list of discount factor to interpolate
        :return:
        """


    def get_mkt_data_type(self):
        return "Curve"

    @staticmethod
    def split_benchmark(benchmark):
        """
        split the benchmark
        :param benchmark:
        :return:
        """
        return benchmark[-1:], int(benchmark[0:-1])

    @staticmethod
    def df_simple_rate():
        """

        :return:
        """


class DiscountFactor:
    """
    discount factor functor
    """

    def __init__(self, curve: Curve):
        self.__curve = curve

    def __call__(self, dates):
        return self.__curve.__df(dates)


class Rate:
    """
    projected rate functor
    """

    def __init__(self, curve: Curve):
        self.__curve = curve

    def __call__(self, start, end):
        return self.__curve.rate(start, end)


if __name__ == "__main__":
    # we assume a flat 5% rate across entire curve
    # we don't have market data to calibrate curve at this stage unfortunately
    # model now assumes log linear interpolation for 2yr and flat extrapolation beyond
    bm = ['1b', '1w', '1m', '3m', '6m', '1y', '2y']
    rates = [5.] * len(bm)
    usd_crv = Curve(bm, rates)
    # df and rate functor
    df = DiscountFactor(usd_crv)
    proj_rate = Rate(usd_crv)

    start_date = datetime.date(2024, 8, 7)
    end_date = datetime.date(2024, 11, 20)

    # a projected forward rate
    df(start_date)
    proj_rate(start_date, end_date)
    usd_crv.rate(start_date, end_date)
    # a discount factor for a future date
    usd_crv.df(datetime.date(2024, 3, 7))
