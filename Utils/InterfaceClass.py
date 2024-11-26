
import numpy as np

from Utils.MediumClass import Medium

# 404


class Interface():

    def __init__(self, med1: Medium, med2: Medium):
        self.med1 = med1
        self.med2 = med2
        self._theta_i = 0
        pass

    @property
    def theta_i(self):
        return self.theta_i

    @theta_i.setter
    def theta_i(self, value):
        if 0 <= value <= 90:
            self._theta_i = value

    @property
    def theta_t(self):
        n1 = self.med1.n
        n2 = self.med2.n
        theta_i = self.theta_i
        sin_teta_i = np.sin(np.radians(theta_i))

        if n1 == n2:
            return theta_i
        else:
            snell = (n1 * sin_teta_i) / n2
            if snell > 1 or snell < -1:
                return 90  # Snell's Law not applicable, total internal reflection
            theta_t = np.degrees(np.arcsin(snell))
            return theta_t

    @property
    def theta_r(self):
        return self.theta_i

    def gamma_par12(self, freq):
        return (self.med2.eta(freq) * np.cos(self.theta_t) - self.med1.eta(freq) * np.cos(self.theta_i)) / \
               (self.med2.eta(freq) * np.cos(self.theta_t) +
                self.med1.eta(freq) * np.cos(self.theta_i))

    def gamma_par21(self, freq):
        return -self.gamma_par12(freq)

    def tau_par12(self, freq):
        return (1 + self.gamma_par12(freq)) * (np.cos(self.theta_i)/np.cos(self.theta_t))

    def tau_par21(self, freq):
        return (1 + self.gamma_par21(freq)) * (np.cos(self.theta_t)/np.cos(self.theta_i))

    def gamma_perp12(self, freq):
        return (self.med2.eta(freq) * np.cos(self.theta_i) - self.med1.eta(freq) * np.cos(self.theta_t)) / \
               (self.med2.eta(freq) * np.cos(self.theta_i) +
                self.med1.eta(freq) * np.cos(self.theta_t))

    def gamma_perp21(self, freq):
        return -self.gamma_perp12(freq)

    def tau_perp12(self, freq):
        return 1 + self.gamma_perp12(freq)

    def tau_perp21(self, freq):
        return 1 + self.gamma_perp21(freq)


if __name__ == "__main__":
    interface = Interface
