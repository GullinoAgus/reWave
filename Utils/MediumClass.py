import scipy.constants as const
import numpy as np


class Medium():
    def __init__(self, er, ur, sigma, width):
        self.ur = ur
        self.er = er
        self.sigma = sigma
        self.width = width
        self.n = np.sqrt(er/ur)

    def e(self, freq):
        return (self.er * const.epsilon_0 + 1j * self.sigma / (2 * np.pi * freq))

    def eta(self, freq):
        return np.sqrt(const.mu_0 * self.ur / (self.e(freq)))
