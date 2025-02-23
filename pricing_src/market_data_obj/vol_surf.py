from pricing_src.market_data_obj.market_data_interface import MarketData


class VolSurface(MarketData):
    """
    construct a vol surface given a calibrated sto vol model
    """

    def __init__(self, model):
        """
        constructor given a calibrated sto vol model
        :param model:
        """
        self.model = model

    def from_panel(self, panel_data):
        """
        constructor from a table of vol surface
        :param panel_data:
        :return:
        """
        pass

    def vol(self, strike, expiry):
        """
        get an implied vol to use in black pricer from the vol surface
        use interpolation scheme
        :param strike:
        :param expiry:
        :return:
        """
        pass

    def get_mkt_data_type(self):
        return "vol_surface"
