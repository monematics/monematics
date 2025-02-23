from abc import abstractmethod, ABC, ABCMeta


class Interpolator(ABC):
    @abstractmethod
    def __call__(self, x):
        pass

    @abstractmethod
    def eval_all(self, new_x):
        pass


class LinearInterpolator(Interpolator):
    def __init__(self, x, fx):
        self.x = x
        self.fx = fx

    def __call__(self, x_to_eval):
        pass
