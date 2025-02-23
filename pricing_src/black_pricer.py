import numpy as np


class BlackPricer:
    """
    Analytical pricer using Black's formula
    Supports analytical risk calculations
    for deterministic params
    """

    def __init__(self, S, K, r, sigma, t, opt_type=1):
        """
        default constructor
        :param S:
        :param K:
        :param r:
        :param sigma:
        :param t:
        """
        self.S = S
        self.K = K
        self.r = r
        self.sigma = sigma
        self.t = t
        self.opt_type = opt_type

    # more constructor, like construct given price
    def calc_d1(self):
        pass

    def calc_d2(self):
        pass

    def price(self):
        pass

    def delta(self):
        pass

    ## more risk methods

