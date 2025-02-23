from pricing_src.mc_simulator import MCSimulator
from pricing_src.sto_vol_model import Heston


class Calibrator:
    pass


def pricing_test(mkt_data):
    # sto vol construction
    sto_vol = Heston()


    calibrator = Calibrator(sto_vol)


    calibrator.calibrate(mkt_data)
    simulator = MCSimulator(sto_vol)
    simulator.simluate()