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

    def e_comp(self, freq):
        '''
        Obtener el epsilon comprejo total del medio
         para una frecuencia dada
        Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        complex - epsilon comprejo total del medio
        '''
        return (self.e - 1j * self.sigma / (2 * np.pi * freq))

    def prop_coef(self, freq):
        '''
        Obtener el coeficiente de propagacion complejo del medio
         para una frecuencia dada
        Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        complex - coeficiente de propagacion complejo del medio
        '''
        return np.sqrt(1j * 2 * np.pi * freq * self.u * (self.sigma + 1j * 2 * np.pi * freq * self.e), dtype=np.complex256)

    def eta(self, freq):
        '''
        Obtener la impedancia caracteristica del medio
         para una frecuencia dada
         Args:
        freq : float - frecuencia de operacion en Hz

        Returns:
        complex - impedancia caracteristica del medio
        '''
        return np.sqrt(self.u / (self.e_comp(freq)), dtype=np.complex256)

    def Zo_par(self, freq, theta):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TM
        '''
        return self.eta(freq) * np.cos(theta, dtype=np.float128)

    def Zo_from_theta_i_par(self, freq, theta_i, gamma_i):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TM
        '''
        return self.eta(freq) * np.sqrt(1-(gamma_i/self.prop_coef(freq)*np.sin(theta_i))**2, dtype=np.complex256)

    def prop_coef_par(self, freq, theta):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TM
        '''
        return self.prop_coef(freq) * np.cos(theta, dtype=np.float128)

    def prop_coef_from_theta_i_par(self, freq, theta_i, gamma_i):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TM
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TM
        '''
        return self.prop_coef(freq) * np.sqrt(1-(gamma_i/self.prop_coef(freq)*np.sin(theta_i, dtype=np.float128))**2, dtype=np.complex256)

    def Zo_per(self, freq, theta):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TE
        '''
        return self.eta(freq) / np.cos(theta, dtype=np.float128)

    def Zo_from_theta_i_per(self, freq, theta_i, gamma_i):
        '''
        Obtener la impedancia caracteristica equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - impedancia caracteristica equivalente para incidencia de ondas TE
        '''
        return self.eta(freq) / np.sqrt(1-(gamma_i/self.prop_coef(freq)*np.sin(theta_i, dtype=np.float128))**2, dtype=np.complex256)

    def prop_coef_per(self, freq, theta):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TE
        '''
        return self.prop_coef(freq) * np.cos(theta, dtype=np.float128)

    def prop_coef_from_theta_i_per(self, freq, theta_i, gamma_i):
        '''
        Obtener la constante de propagacion equivalente para incidencia de ondas TE
        para una frecuencia dada y un angulo de incidencia theta
        Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
        complex - constante de propagacion equivalente para incidencia de ondas TE
        '''
        return self.prop_coef(freq) * np.sqrt(1-(gamma_i/self.prop_coef(freq)*np.sin(theta_i, dtype=np.float128))**2, dtype=np.complex256)

    def T_mat_par(self, freq, theta):
        '''
        Obtener Matrices ABCD del medio como linea de transmision para onda incidente TM

         Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
         complex - Matrices ABCD del medio como linea de transmision para onda incidente TM
        '''
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
        '''
        Obtener Matrices ABCD del medio como linea de transmision para onda incidente TE

         Args:
        freq : float - frecuencia de operacion en Hz
        theta : float - angulo de incidencia en radianes

        Returns:
         complex - Matrices ABCD del medio como linea de transmision para onda incidente TE
        '''
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
        return f"MediumClass(er={self.er}, ur={self.ur}, sigma={self.sigma}, width={self._width}, width_lambdas={self._width_lambdas})"
