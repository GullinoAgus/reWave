
import numpy as np

from Utils.Medium import Medium
import scipy.constants as const

class TLineNetwork:
    def __init__(self, layer_list, theta_i):
        """
        layer_list: lista de objetos Medium (incluye la capa de entrada y la de salida)
        theta_i: ángulo de incidencia en la primera capa (en radianes)
        """
        self._layer_list = layer_list
        self._theta_1 = theta_i

    # Ángulo de incidencia
    @property
    def theta_i(self):
        return self._theta_1

    @theta_i.setter
    def theta_i(self, value):
        if 0 <= value <= np.pi / 2:
            self._theta_1 = value

    # Cálculo de k_x para cada medio usando Snell y k de la primera capa
    def k_x_i(self, freq, mi: Medium, m1: Medium):
        """
        Devuelve el componente normal del número de onda en la capa 'mi', a partir
        del ángulo en la primera capa y del número de onda de la primera capa (k1).
        Se usa: k_x = k0 * sqrt(μ_r,i ε_r,i - μ_r,1 ε_r,1 sin² θ_i).
        """
        k0 = 2 * np.pi * freq / const.c
        sin2_theta = np.sin(self.theta_i) ** 2
        eps_cr_i = mi.e_comp(freq) / const.epsilon_0      # ε_r compleja de la capa i
        eps_cr_1 = m1.e_comp(freq) / const.epsilon_0      # ε_r compleja de la primera capa
        expr = mi.ur * eps_cr_i - m1.ur * eps_cr_1 * sin2_theta
        return k0 * np.sqrt(expr)

    # Impedancia de entrada equivalente a distancia L en una línea (función auxiliar)
    def Zin(self, Zi, Zl, kL):
        """
        Impedancia de entrada vista a una distancia L de la carga Zl en una línea de
        transmisión con impedancia característica Zi.
        Z_in = Zi * (Zl + j Zi tan(kL)) / (Zi + j Zl tan(kL))
        """
        return Zi * (Zl + 1j * Zi * np.tan(kL)) / (Zi + 1j * Zl * np.tan(kL))

    # Coeficiente de reflexión en una interfaz
    def Gamma(self, Zo, Zl):
        return (Zl - Zo) / (Zl + Zo)
    
    def get_se(self, freq, pol='TM'):
        if len(self._layer_list) == 3 and self._layer_list[0].is_air() and self._layer_list[-1].is_air():
            if pol.upper() == 'TM':
                return self.get_se_TM(freq)
            elif pol.upper() == 'TE':
                return self.get_se_TE(freq)
        else:
            if pol.upper() == 'TM':
                return self.get_matrix_se_TM(freq)
            elif pol.upper() == 'TE':
                return self.get_matrix_se_TE(freq)
            
    def get_se_TM(self, freq):
        """
        Calcula la Efectividad de Blindaje (SE) para polarización TM en el caso de 3 capas (single shield).
        Utiliza las fórmulas (4.20-4.23) del libro de Celozzi & Araneo y descompone la SE en:
        SE = R + A + M, donde:
        - R: reflection loss
        - A: absorption loss  
        - M: multiple reflection correction
        
        Returns:
            tuple: (se, R, A, M) donde se es la SE total y R, A, M son los componentes en dB
        """
        
        m1 = self._layer_list[0]  # Medio de entrada
        m2 = self._layer_list[1]  # Shield (medio intermedio)
        m3 = self._layer_list[2]  # Medio de salida

        k1 = m1.k(freq)
        kxs = self.k_x_i(freq, m2, m1)

        Z1 = m1.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        Z2 = m2.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        Z3 = m3.Zo_from_theta_i_TM(freq, self.theta_i, k1)

        d = m2.width(freq)
        
        # R: Reflection loss - ecuación (4.23a) generalizada
        # R = |(Z1+Z2)(Z2+Z3)/(4*Z2*Z3)|
        R = np.abs((Z1 + Z2) * (Z2 + Z3) / (4 * Z2 * Z3))
        
        # A: Absorption loss - ecuación (4.23b)
        # A = 20*log10(|exp(j*kx2*d)|) = -8.686 * Im(kx2) * d
        A = np.abs(np.exp(1j * kxs * d))
        
        # M: Multiple reflection correction - ecuación (4.23c) generalizada
        # M = 20*log10(|1 - (Z1-Z2)(Z1-Z3)/[(Z1+Z2)(Z1+Z3)] * exp(-2j*kx2*d)|)
        M = np.abs(
            1.0 - ((Z1 - Z2)*(Z3 - Z2) / ((Z2 + Z1)*(Z2 + Z3))) * np.exp(-1j * 2.0 * kxs * d)
        )
        
        return R*A*M, R, A, M

    def get_se_TE(self, freq):
        """
        Calcula la Efectividad de Blindaje (SE) para polarización TE en el caso de 3 capas (single shield).
        Utiliza las fórmulas (4.20-4.23) del libro de Celozzi & Araneo y descompone la SE en:
        SE = R + A + M, donde:
        - R: reflection loss
        - A: absorption loss  
        - M: multiple reflection correction
        
        Returns:
            tuple: (se, R, A, M) donde se es la SE total y R, A, M son los componentes en veces
        """
        
        m1 = self._layer_list[0]  # Medio de entrada
        m2 = self._layer_list[1]  # Shield (medio intermedio)
        m3 = self._layer_list[2]  # Medio de salida

        k1 = m1.k(freq)
        kxs = self.k_x_i(freq, m2, m1)

        Z1 = m1.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        Z2 = m2.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        Z3 = m3.Zo_from_theta_i_TE(freq, self.theta_i, k1)

        d = m2.width(freq)
        
        # R: Reflection loss - ecuación (4.23a) generalizada
        # R = |(Z1+Z2)(Z2+Z3)/(4*Z2*Z3)|
        R = np.abs((Z1 + Z2) * (Z2 + Z3) / (4 * Z2 * Z3))
        
        # A: Absorption loss - ecuación (4.23b)
        # A = 20*log10(|exp(j*kx2*d)|) = -8.686 * Im(kx2) * d
        A = np.abs(np.exp(1j * kxs * d))
        
        # M: Multiple reflection correction - ecuación (4.23c) generalizada
        # M = 20*log10(|1 - (Z1-Z2)(Z2-Z3)/[(Z1+Z2)(Z2+Z3)] * exp(-2j*kx2*d)|)
        M = np.abs(1.0 - ((Z1 - Z2)*(Z3 - Z2) / ((Z2 + Z1)*(Z2 + Z3))) * np.exp(-1j * 2.0 * kxs * d))
        
        return R*A*M, R, A, M

    # Cálculo de SE para polarización TM
    def get_matrix_se_TM(self, freq):
        """
        Devuelve la razón de amplitudes E_inc/E_trans para onda TM.
        Si se desea la SE en dB, usar 20*log10(abs(se)).
        """
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        k1 = m1.k(freq)
        # Impedancia de entrada y salida usando Snell
        eta_i = m1.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        eta_s = mN.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        # Construir la matriz ABCD total
        T_total = np.identity(2, dtype=complex)
        for mi in self._layer_list[1:-1]:
            k_x = self.k_x_i(freq, mi, m1)
            Ti = mi.T_TM(freq, self.theta_i, k1, k_x)
            T_total = T_total @ Ti
        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]
        # Coeficiente de transmisión según red ABCD y puertos con impedancias eta_i y eta_s
        denom = A * eta_s + B + C * eta_s * eta_i + D * eta_i
        t = (2 * eta_s) / denom
        se = 1 / t  # razón Ei/Et
        return se

    # Cálculo de SE para polarización TE
    def get_matrix_se_TE(self, freq):
        """
        Devuelve la razón de amplitudes E_inc/E_trans para onda TE.
        """
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        k1 = m1.k(freq)
        eta_i = m1.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        eta_s = mN.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        T_total = np.identity(2, dtype=complex)
        for mi in self._layer_list[1:-1]:
            k_x = self.k_x_i(freq, mi, m1)
            Ti = mi.T_TE(freq, self.theta_i, k1, k_x)
            T_total = T_total @ Ti
        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]
        denom = A * eta_s + B + C * eta_s * eta_i + D * eta_i
        t = (2 * eta_s) / denom
        se = 1 / t
        return se

    # Cálculo de reflexión total para TM
    def get_reflexion_TM(self, freq):
        """
        Calcula el coeficiente de reflexión total en el puerto de entrada para ondas TM.
        """
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        k1 = m1.k(freq)
        eta_i = m1.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        eta_s = mN.Zo_from_theta_i_TM(freq, self.theta_i, k1)
        # Construcción de la matriz ABCD total
        T_total = np.identity(2, dtype=complex)
        for mi in self._layer_list[1:-1]:
            k_x = self.k_x_i(freq, mi, m1)
            Ti = mi.T_TM(freq, self.theta_i, k1, k_x)
            T_total = T_total @ Ti
        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]
        # Coeficiente de reflexión en el puerto 1
        num = A * eta_s + B - C * eta_s * eta_i - D * eta_i
        den = A * eta_s + B + C * eta_s * eta_i + D * eta_i
        return num / den

    # Cálculo de reflexión total para TE
    def get_reflexion_TE(self, freq):
        """
        Calcula el coeficiente de reflexión total en el puerto de entrada para ondas TE.
        """
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        k1 = m1.k(freq)
        eta_i = m1.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        eta_s = mN.Zo_from_theta_i_TE(freq, self.theta_i, k1)
        T_total = np.identity(2, dtype=complex)
        
        for mi in self._layer_list[1:-1]:
            k_x = self.k_x_i(freq, mi, m1)
            Ti = mi.T_TE(freq, self.theta_i, k1, k_x)
            T_total = T_total @ Ti
            
        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]
        
        num = A * eta_s + B - C * eta_s * eta_i - D * eta_i
        den = A * eta_s + B + C * eta_s * eta_i + D * eta_i
        
        return num / den

    def is_evanescent(self, k_x: complex, tol: float = 1e-8) -> bool:
        """
        Comprueba si una onda es evanescente: parte real ~0 y parte imaginaria >0.
        """
        return np.abs(np.real(k_x)) < tol and np.imag(k_x) > tol

    def theta_t(self, freq):
        """
        Calcula el ángulo transmitido en la última capa a partir de Snell. Si el resultado
        es complejo o no está en [-1,1], devuelve pi/2 (onda evanescente).
        """
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        sin_theta_t = m1.k(freq) / mN.k(freq) * np.sin(self.theta_i)
        if np.iscomplex(sin_theta_t) or not -1 <= np.real(sin_theta_t) <= 1:
            return np.pi / 2
        return np.arcsin(np.abs(sin_theta_t))


if __name__ == "__main__":
    m1 = Medium(1, 1, 0, width=100)
    m2 = Medium(4, 1, 0, width=0.1)
    m4 = Medium(9, 1, 0, width=100)

    med_list = [m1, m2, m4]
    net = TLineNetwork(med_list, 0)
    freqs = np.logspace(np.log10(1), np.log10(10E9), 10000, base=10)

    print(net.get_reflexion_TM())
    pass


'''
Corregir ley de snell por las formulas q me mando patricio

Sobre las clases:

2_ondas, pag. 34-> d = 9,375mm

'''
