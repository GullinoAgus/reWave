import scipy.constants as const
import numpy as np


class Medium:
    def __init__(self, er, ur, sigma, width=None, width_lambdas=None):
        self.ur = ur                    # permeabilidad relativa (real)
        self.er = er                    # permitividad relativa (real)
        self.u = ur * const.mu_0        # permeabilidad absoluta (real)
        self.e = er * const.epsilon_0   # permitividad absoluta (real)
        self.sigma = sigma              # conductividad (real)
        self._width = width             # espesor en metros (real)
        self._width_lambdas = width_lambdas  # espesor en longitudes de onda
        self.n = np.sqrt(self.e * self.u)

    def width(self, freq):
        """
        Devuelve el espesor de la capa.  Si no se ha fijado un espesor en metros,
        se calcula a partir del número de longitudes de onda deseado:
            width = width_lambdas * c / (freq * sqrt(er*ur))
        """
        if self._width is None:
            return self._width_lambdas * const.speed_of_light / (freq * np.sqrt(self.er * self.ur))
        else:
            return self._width

    def e_comp(self, freq):
        """
        Permitivad compleja total: ε_c = ε - j σ/ω.
        """
        return self.e - 1j * self.sigma / (2 * np.pi * freq)

    def eta(self, freq):
        """
        Impedancia intrínseca del medio: η = sqrt(μ / ε_c).
        """
        return np.sqrt(self.u / self.e_comp(freq))

    def k(self, freq):
        """
        Número de onda complejo: k = ω sqrt(μ ε_c).
        """
        return 2 * np.pi * freq * np.sqrt(self.u * self.e_comp(freq))

    # Impedancia TM/TE en función del ángulo de incidencia en ese medio
    def Zo_TM(self, freq, theta):
        """
        Impedancia de onda equivalente para polarización TM con ángulo interno 'theta'.
        Para TM (p-polarizada), Z_TM = η cos θ.
        """
        return self.eta(freq) * np.cos(theta)

    def Zo_TE(self, freq, theta):
        """
        Impedancia de onda equivalente para polarización TE con ángulo interno 'theta'.
        Para TE (s-polarizada), Z_TE = η / cos θ.
        """
        cos_theta = np.cos(theta)
        if np.abs(cos_theta) < 1e-12:
            # En incidencia de 90° cos θ ≈ 0 → Z_TE tiende a infinito
            return np.inf
        return self.eta(freq) / cos_theta

    # Impedancia TM/TE calculada a partir del ángulo de incidencia en el primer medio
    def Zo_from_theta_i_TM(self, freq, theta_inc, k1):
        """
        Impedancia equivalente TM calculada a partir del ángulo de incidencia en la primera
        capa. Usa Snell y el número de onda k1 en la primera capa.
        """
        # cos θ_i = sqrt(1 - (k1/k_i sinθ_inc)**2)
        sin_term = (k1 * np.sin(theta_inc)) / self.k(freq)
        return self.eta(freq) * np.sqrt(1 - sin_term**2)

    def Zo_from_theta_i_TE(self, freq, theta_inc, k1):
        """
        Impedancia equivalente TE calculada a partir del ángulo de incidencia en la primera
        capa. Usa Snell.
        """
        sin_term = (k1 * np.sin(theta_inc)) / self.k(freq)
        cos_term = np.sqrt(1 - sin_term**2)
        if np.abs(cos_term) < 1e-12:
            return np.inf
        return self.eta(freq) / cos_term

    def gamma(self, freq):
        return -1j * self.k(freq)

    # Matriz ABCD para una capa en polarización TM
    def T_TM(self, freq, theta_inc, k1, k_x_i):
        """
        Devuelve la matriz ABCD de la capa para onda TM, utilizando la impedancia
        calculada a partir de Snell (Zo_from_theta_i_TM).
        """
        width = self.width(freq)
        A = np.cos(k_x_i * width)
        Z0_i = self.Zo_from_theta_i_TM(freq, theta_inc, k1)
        # Si la impedancia se anula (cos θ_i = 0) → onda evanescente: B = C = 0
        if np.abs(Z0_i) < 1e-14:
            B = 0
            C = 0
        else:
            B = 1j * Z0_i * np.sin(k_x_i * width)
            C = 1j * (1 / Z0_i) * np.sin(k_x_i * width)
        D = A
        return np.array([[A, B], [C, D]])

    # Matriz ABCD para una capa en polarización TE
    def T_TE(self, freq, theta_inc, k1, k_x_i):
        """
        Devuelve la matriz ABCD de la capa para onda TE, utilizando la impedancia
        calculada a partir de Snell (Zo_from_theta_i_TE).
        """
        
        width = self.width(freq)
        A = np.cos(k_x_i * width)
        Z0_i = self.Zo_from_theta_i_TE(freq, theta_inc, k1)
        # Si la impedancia tiende a infinito → B y C se consideran cero
        if np.isinf(Z0_i):
            B = 0
            C = 0
        else:
            B = 1j * Z0_i * np.sin(k_x_i * width)
            C = 1j * (1 / Z0_i) * np.sin(k_x_i * width)
        D = A
        return np.array([[A, B], [C, D]])

    def __repr__(self) -> str:
        return f"Medium(er={self.er}, ur={self.ur}, sigma={self.sigma}, width={self._width}, width_lambdas={self._width_lambdas})"