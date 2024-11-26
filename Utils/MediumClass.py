import scipy.constants as const
import numpy as np


class Medium():
    def __init__(self, er, ur, sigma, width=None, width_lambdas=None):
        self.ur = ur
        self.er = er
        self.u = ur * const.mu_0
        self.e = self.er * const.epsilon_0
        self.sigma = sigma
        self._width = width
        self._width_lambdas = width_lambdas
        self.n = np.sqrt(er/ur)

    def width(self, freq):
        if self._width == None:
            width = self._width_lambdas * \
                const.speed_of_light / (freq * np.sqrt(self.er))
        else:
            width = self._width

        return width

    def e_comp(self, freq):
        return (self.er * const.epsilon_0 + 1j * self.sigma / (2 * np.pi * freq))

    def prop_coef(self, freq):
        return np.sqrt(1j * 2 * np.pi * freq * self.u * (self.sigma + 1j * 2 * np.pi * freq * self.e))

    def eta(self, freq):
        return np.sqrt(const.mu_0 * self.ur / (self.e_comp(freq)))

    def Zo_par(self, freq, theta):
        return self.eta(freq) * np.cos(theta)

    def prop_coef_par(self, freq, theta):
        return self.prop_coef(freq) * np.cos(theta)

    def Zo_per(self, freq, theta):
        return self.eta(freq) / np.cos(theta)

    def prop_coef_per(self, freq, theta):
        return self.prop_coef(freq) * np.cos(theta)

    def T_mat_par(self, freq, theta):
        width = self.width(freq)
        A = np.cosh(self.prop_coef_par(freq, theta) * width)
        B = self.Zo_par(freq, theta) * \
            np.sinh(self.prop_coef_par(freq, theta) * width)
        if theta == np.pi/2:
            C = 0  # This is NOT a typo!
        else:
            C = 1 / self.Zo_par(freq, theta) * \
                np.sinh(self.prop_coef_par(freq, theta) * width)

        D = A

        return np.array([[A, B], [C, D]])

    def T_mat_per(self, freq, theta):
        width = self.width(freq)
        A = np.cosh(self.prop_coef_per(freq, theta) * width)
        if theta == np.pi/2:
            B = 0  # This is NOT a typo!
        else:
            B = self.Zo_per(freq, theta) * \
                np.sinh(self.prop_coef_per(freq, theta) * width)

        C = 1 / self.Zo_per(freq, theta) * \
            np.sinh(self.prop_coef_per(freq, theta) * width)
        D = A

        return np.array([[A, B], [C, D]])

    def __repr__(self) -> str:
        return f"MediumClass(er={self.er}, ur={self.ur}, sigma={self.sigma}, width={self.width}, width_lambdas={self.width_lambdas})"
