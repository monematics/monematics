"""
this file implements the baseline MVO portfolio optimization problem as a quadratic programming problem
"""
import numpy as np


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

    def solve(self):
        """
        this solves the baseline MVO problem
        :return: w, portfolio weights
        """
        return
