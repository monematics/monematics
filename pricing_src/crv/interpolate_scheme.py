"""
Interpolation scheme used in pricing
1. Log linear
2. APQ2N and 4N
3. Cubic Spline
"""
from abc import ABC


class InterpolationScheme(ABC):
    pass


class ExtrapolationScheme:
    def __init__(self, x):
        self.x = x

    def __call__(self, *args, **kwargs):
        return self.x
