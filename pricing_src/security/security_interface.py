from abc import ABC, abstractmethod


class Security(ABC):

    @abstractmethod
    def evaluate(self, method, market_data):
        pass

    @abstractmethod
    def is_supported_method(self, method):
        pass

    @abstractmethod
    def calc_pv(self, market_data):
        pass


class Option(Security, ABC):
    pass
