from abc import ABC, abstractmethod

import pandas as pd

from investment_src.portfolio_basic.expected_return import *
from investment_src.portfolio_basic.correlation_matrix import *


class PortfolioImpl(ABC):

    @abstractmethod
    def Mu(self, exp_returns: ExpReturns) -> float:
        pass

    @abstractmethod
    def Var(self, corr_mat: CorrMat) -> float:
        pass

    @abstractmethod
    def sharp(self, exp_returns: ExpReturns, corr_mat: CorrMat) -> float:
        pass


class Portfolio(PortfolioImpl):
    def Mu(self, exp_returns: ExpReturns) -> float:
        pass

    def __init__(self, *arg):
        self.num_assets = 0
        self.assets = []
        self.weights = pd.DataFrame([])
