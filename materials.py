from enum import Enum, unique
import itertools
import functools


@unique
class Material(Enum):
    def __init__(self, b, c):
        self.b = b
        self.c = c
        self.coefficients = itertools.zip_longest(self.b, self.c)

    @functools.lru_cache(maxsize=256)
    def n(self, wavelength):
        wavelength_squared = wavelength**2
        return (1 + sum(b*wavelength_squared/(wavelength_squared-c) for b, c in self.coefficients))**.5
