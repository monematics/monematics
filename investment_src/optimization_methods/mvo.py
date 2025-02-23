"""
this file implements various types of MVO portfolio optimization methods
central models
"""
import numpy as np
from enum import Enum


class MVOType(Enum):
    BASE = 0,
    MAXRET = 1,
    MIX = 2,
    MULTIPERIOD = 3,
    MAXSHARPE = 4,
    CVAR = 5,
    INTEGER = 6

    def __str__(self):
        return self.name


class MVO:
    def __init__(self, exp_returns, corr_matrix, target_return):
        """
        constructor
        :param exp_returns: numpy object (n,1), n : number of asset in the portfolio
        :param corr_matrix: numpy object (n,n)
        :param target_return: scalar value
        """
        self.mu = exp_returns
        self.Q = corr_matrix
        self.R = target_return
        self.w = np.array([0] * np.shape(self.mu)[0])
        pass

    def solve(self, allow_short_sale=False):
        """
        this solves the baseline MVO problem
        :return: w, portfolio weights
        """
        return
