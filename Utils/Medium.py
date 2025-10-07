import scipy.constants as const
import numpy as np


class Medium:
    def __init__(self, er, ur, sigma, width=None, width_lambdas=None, loss_model=None, eps_i=None):
        """
        er: permitividad relativa (parte real)
        ur: permeabilidad relativa (real)
        sigma: conductividad (S/m) para el modelo 'sigma'
        width: espesor en metros (opcional)
        width_lambdas: espesor en longitudes de onda del propio medio (opcional)
        loss_model: 'sigma' o 'eps_i' (opcional, puede ser seteado después)
        eps_i: parte imaginaria de er (>=0) si loss_model=='eps_i' (opcional, puede ser seteado después)
        """
        self.ur = float(ur)
        self.er = float(er)
        self.u = self.ur * const.mu_0
        self.e = self.er * const.epsilon_0
        self.sigma = float(sigma)
        self._width = width
        self._width_lambdas = width_lambdas

        # Soporte para el nuevo modo de pérdidas. Si no lo pasan aquí, puede setearse más tarde desde la UI.
        self.loss_model = (loss_model if loss_model is not None else getattr(self, "loss_model", "sigma"))
        self.eps_i = float(eps_i) if eps_i is not None else float(getattr(self, "eps_i", 0.0))

        # índice del medio (no imprescindible, pero lo conservamos)
        self.n = np.sqrt(self.e * self.u)

    def width(self, freq):
        """
        Devuelve el espesor de la capa. Si no se fijó un espesor en metros,
        se calcula a partir del número de longitudes de onda deseado del propio medio:
            width = width_lambdas * c / (freq * sqrt(er*ur))
        Nota: si el medio es dispersivo con eps_i, usamos la parte REAL de er para la velocidad de fase.
        """
        if self._width is None:
            er_eff = float(np.real(self.er))  # mantener compatibilidad
            return self._width_lambdas * const.speed_of_light / (freq * np.sqrt(er_eff * self.ur))
        else:
            return self._width

    def e_comp(self, freq):
        """
        Permitividad COMPLEJA total:
          - Modo 'sigma' (original):   ε_c = ε - j σ / ω
          - Modo 'eps_i' (nuevo):      ε_c = ε0 * (εr' - j εr'')
        Donde ω = 2πf.
        """
        omega = 2 * np.pi * freq
        model = getattr(self, "loss_model", "sigma")
        if model == "eps_i":
            eps_i_val = float(getattr(self, "eps_i", 0.0))
            # ε_c = ε0(εr' - j εr'')
            return (self.er * const.epsilon_0) - 1j * const.epsilon_0 * eps_i_val
        else:
            # ε_c = ε - j σ/ω (comportamiento anterior)
            # (manejo robusto si freq→0)
            if omega == 0:
                return self.e
            return self.e - 1j * (self.sigma / omega)

    def eta(self, freq):
        """
        Impedancia intrínseca del medio: η = sqrt(μ / ε_c).
        """
        return np.sqrt(self.u / self.e_comp(freq))

    def k(self, freq):
        """
        Número de onda complejo: k = ω sqrt(μ ε_c).
        """
        omega = 2 * np.pi * freq
        return omega * np.sqrt(self.u * self.e_comp(freq))

    # Impedancia TM/TE en función del ÁNGULO dentro del medio (theta es el ángulo interno)
    def Zo_TM(self, freq, theta):
        """
        TM (p-polarizada): Z_TM = η cos θ.
        """
        return self.eta(freq) * np.cos(theta)

    def Zo_TE(self, freq, theta):
        """
        TE (s-polarizada): Z_TE = η / cos θ.
        """
        cos_theta = np.cos(theta)
        if np.abs(cos_theta) < 1e-12:
            return np.inf
        return self.eta(freq) / cos_theta

    # Impedancia TM/TE calculada a partir del ángulo de incidencia en el PRIMER medio
    def Zo_from_theta_i_TM(self, freq, theta_inc, k1):
        """
        Impedancia equivalente TM a partir de θ_inc en el primer medio (Snell).
        cos θ_i_en_este = sqrt(1 - (k1/ki * sinθ_inc)^2)
        Z_TM = η * cos θ_i_en_este
        """
        ki = self.k(freq)
        if ki == 0:
            return self.eta(freq)  # fallback
        sin_term = (k1 * np.sin(theta_inc)) / ki
        cos_internal = np.sqrt(1 - sin_term**2)
        return self.eta(freq) * cos_internal

    def Zo_from_theta_i_TE(self, freq, theta_inc, k1):
        """
        Impedancia equivalente TE a partir de θ_inc en el primer medio (Snell).
        cos θ_i_en_este = sqrt(1 - (k1/ki * sinθ_inc)^2)
        Z_TE = η / cos θ_i_en_este
        """
        ki = self.k(freq)
        if ki == 0:
            return np.inf
        sin_term = (k1 * np.sin(theta_inc)) / ki
        cos_internal = np.sqrt(1 - sin_term**2)
        if np.abs(cos_internal) < 1e-12:
            return np.inf
        return self.eta(freq) / cos_internal

    def gamma(self, freq):
        return -1j * self.k(freq)

    # Matriz ABCD para una capa en polarización TM
    def T_TM(self, freq, theta_inc, k1, k_x_i):
        """
        Matriz ABCD de la capa para TM.
        Z0_i usa Zo_from_theta_i_TM (Snell en el propio medio).
        """
        width = self.width(freq)
        A = np.cos(k_x_i * width)
        Z0_i = self.Zo_from_theta_i_TM(freq, theta_inc, k1)
        if np.abs(Z0_i) < 1e-14:
            B = 0
            C = 0
        else:
            s = np.sin(k_x_i * width)
            B = 1j * Z0_i * s
            C = 1j * (1 / Z0_i) * s
        D = A
        return np.array([[A, B], [C, D]])

    # Matriz ABCD para una capa en polarización TE
    def T_TE(self, freq, theta_inc, k1, k_x_i):
        """
        Matriz ABCD de la capa para TE.
        Z0_i usa Zo_from_theta_i_TE (Snell en el propio medio).
        """
        width = self.width(freq)
        A = np.cos(k_x_i * width)
        Z0_i = self.Zo_from_theta_i_TE(freq, theta_inc, k1)
        if np.isinf(Z0_i):
            B = 0
            C = 0
        else:
            s = np.sin(k_x_i * width)
            B = 1j * Z0_i * s
            C = 1j * (1 / Z0_i) * s
        D = A
        return np.array([[A, B], [C, D]])

    def is_air(self):
        return (self.er == 1.0) and (self.ur == 1.0) and (self.sigma == 0.0)

    def __repr__(self) -> str:
        lm = getattr(self, "loss_model", "sigma")
        ei = getattr(self, "eps_i", 0.0)
        return (f"Medium(er={self.er}, ur={self.ur}, sigma={self.sigma}, "
                f"loss_model='{lm}', eps_i={ei}, "
                f"width={self._width}, width_lambdas={self._width_lambdas})")
