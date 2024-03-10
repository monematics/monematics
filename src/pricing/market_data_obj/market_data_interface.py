from abc import ABC, abstractmethod


class MarketData(ABC):

    @abstractmethod
    def get_mkt_data_type(self):
        pass

# TODO: make market data type enum and change get_mkt_data_type
# class MarketDataType(ENUM)
