import numpy as np

class MCSimulator:
    def __init__(self, num_of_time, process = 'basic'):
        self.num_of_time = num_of_time
        self.process = process

    def simulate(self):
        return []

    def mean_path(self):
        paths  = self.simulate()
        return np.mean(paths)