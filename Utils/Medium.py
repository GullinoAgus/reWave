import scipy.constants as const
import numpy as np


class Medium():
    def __init__(self, er, mur, sigma, width=None, width_lambdas=None):
        self.mur = mur
        self.er = er
        self.mu = mur * const.mu_0
        self.e = er * const.epsilon_0
        self.sigma = sigma
        self._width = width
        self._width_lambdas = width_lambdas
        self.n = np.sqrt(er/mur)

    def width(self, freq):
        '''
        Obtener el ancho de la capa en metros para una frecuencia dada
        Si no se ha proporcionado el ancho en metros, se calcula utilizando la formula:
            width = width_lambdas * c / (freq * sqrt(er))
        donde width_lambdas es el ancho en longitudes de onda y c es la velocidad de la luz.

        Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        float - ancho de la capa en metros
        '''
        if self._width == None:
            width = self._width_lambdas * \
                const.speed_of_light / (freq * np.sqrt(self.er))
        else:
            width = self._width

        return width

    def e_c(self, freq):
        '''
        Obtener el epsilon comprejo total del medio
         para una frecuencia dada
        Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        complex - epsilon comprejo total del medio
        '''
        return (self.e - 1j * self.sigma / (2 * np.pi * freq))

    def gamma(self, freq):
        '''
        Obtener el coeficiente de propagacion complejo del medio
         para una frecuencia dada
        Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        complex - coeficiente de propagacion complejo del medio
        '''
        return 1j * 2 * np.pi * freq * np.sqrt(self.mu * self.e_c(freq), dtype=np.clongdouble)

    def eta_c(self, freq):
        '''
        Calcula la impedancia intrínseca compleja (η) del medio para una frecuencia dada.

        Fórmula fundamental:
            η = √(μ/ε_c)
        
        Donde:
            μ: Permeabilidad magnética del medio [H/m]
            ε_c: Permitividad compleja = ε - j(σ/ω)
                ε: Permitividad dieléctrica [F/m]
                σ: Conductividad del medio [S/m]
                ω: Frecuencia angular = 2πf [rad/s]

        Parámetros
        ----------
        freq : float
            Frecuencia de operación en Hertz [Hz]

        Retorna
        -------
        complex
            Valor complejo de la impedancia intrínseca en ohms [Ω]

        Ejemplo
        -----------------
        >>> medio = Medio(μ=4e-7*np.pi, ε=8.85e-12, σ=0.01)
        >>> eta = medio.eta_c(1e6)  # Frecuencia de 1 MHz
        >>> print(f"{eta:.2f} Ω")
        (123.45+67.89j) Ω
        '''
        return np.sqrt(self.mu / (self.e_c(freq)), dtype=np.clongdouble )

    def Zo_TM(self, freq, theta):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TM
        '''
        return self.eta_c(freq) * np.cos(theta, dtype=np.longdouble)

    def Zo_TM_from_theta_inc(self, freq, theta_i, gamma_i):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TM
        '''
        return self.eta_c(freq) * np.sqrt(1-(gamma_i/self.gamma(freq)*np.sin(theta_i))**2, dtype=np.clongdouble )

    def Zo_TE(self, freq, theta):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TE
        '''
        return self.eta_c(freq) / np.cos(theta, dtype=np.longdouble)

    def Zo_TE_from_theta_inc(self, freq, theta_i, gamma_i):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TE
        '''
        return self.eta_c(freq) / np.sqrt(1-(gamma_i/self.gamma(freq)*np.sin(theta_i, dtype=np.longdouble))**2, dtype=np.clongdouble )

    def gamma_TM(self, freq, theta):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TM
        '''
        return self.gamma(freq) * np.cos(theta, dtype=np.longdouble)
    
    def gamma_TM_from_theta_inc(self, freq, theta_i, gamma_i):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TM
        '''
        return self.gamma(freq) * np.sqrt(1-(gamma_i/self.gamma(freq)*np.sin(theta_i, dtype=np.longdouble))**2, dtype=np.clongdouble )

    def gamma_TE(self, freq, theta):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TE
        '''
        return self.gamma(freq) * np.cos(theta, dtype=np.longdouble)
    
    def gamma_TE_from_theta_inc(self, freq, theta_i, gamma_i):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TE
        '''
        return self.gamma(freq) * np.sqrt(1-(gamma_i/self.gamma(freq)*np.sin(theta_i, dtype=np.longdouble))**2, dtype=np.clongdouble )

    def T_matrix_TM(self, freq, theta):
        '''
        Obtener Matrices ABCD del medio como linea de transmision para onda incidente TM

        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
         complex - Matrices ABCD del medio como linea de transmision para onda incidente TM
        '''
        width = self.width(freq)
        cosh_gamma_d = np.cosh(self.gamma_TM(freq, theta) * width)
        sinh_gamma_d = np.sinh(self.gamma_TM(freq, theta) * width)

        A = cosh_gamma_d
        B = self.Zo_TM(freq, theta) * sinh_gamma_d
        
        if theta == np.pi/2:
            C = 0  # This is NOT a typo!
        else:
            C = sinh_gamma_d / self.Zo_TM(freq, theta)

        D = A

        return np.array([[A, B], [C, D]])

    def T_matrix_TE(self, freq, theta):
        '''
        Obtener Matrices ABCD del medio como linea de transmision para onda incidente TE

         Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
         complex - Matrices ABCD del medio como linea de transmision para onda incidente TE
        '''

        width = self.width(freq)
        cosh_gamma_d = np.cosh(self.gamma_TE(freq, theta) * width)
        sinh_gamma_d = np.sinh(self.gamma_TE(freq, theta) * width)

        A = cosh_gamma_d
        C = sinh_gamma_d / self.Zo_TE(freq, theta)

        if theta == np.pi/2:
            B = 0  # This is NOT a typo!
        else:
            B = self.Zo_TE(freq, theta) * sinh_gamma_d

        D = A

        return np.array([[A, B], [C, D]])

    def __repr__(self) -> str:
        return f"MediumClass(er={self.er}, ur={self.mur}, sigma={self.sigma}, width={self.width}, width_lambdas={self.width_lambdas})"
