
import numpy as np

from Utils.Medium import Medium
import scipy.constants as const

class TLineNetwork():

    def __init__(self, layer_list: list[Medium], theta_i: float):
        # Calculo de la lista de medios con sus angulos de propagacion
        self._theta_1 = theta_i
        self._layer_list = layer_list

        pass

    def Zin(self, Zo, Zl, gammaL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * espesor del medio.

        '''
        return Zo*(Zl+Zo*np.tanh(gammaL, dtype=np.clongdouble))/(Zo+Zl*np.tanh(gammaL, dtype=np.clongdouble))

    def Gamma(self, Zo, Zl):
        '''
        Calculo de coeficiente de reflexion en una interfaz
        '''
        return (Zl-Zo)/(Zl+Zo)

    def get_reflexion_TM(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        k_1 = self._layer_list[0].k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for mi in reversed(self._layer_list[1:-1]):
            Zi = mi.Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            gammaL = mi.gamma(freq) * mi.width(freq)
            Zeq = self.Zin(Zi, Zeq, gammaL)
        Zi = self._layer_list[0].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
        Gamma_in = self.Gamma(Zi, Zeq)

        return Gamma_in
    
    def get_se_TM(self, freq):
        
        T_total = np.identity(2, dtype=np.clongdouble)
        k_1 = self._layer_list[0].k(freq)
        eta_i = self._layer_list[0].eta(freq)
        eta_s = self._layer_list[-1].eta(freq)

        for mi in reversed(self._layer_list[1:-1]):
            Z_i = mi.Zo_from_theta_i_TM(freq, self.theta_i, k_1)
            k_i = self.k_x(freq, mi, Z_i)
            Ti = mi.T_TM(freq, self.theta_i, k_1, k_i)  # Get ABCD matrix
            T_total = Ti @ T_total    # Matrix multiply: T_i * T_total

        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]

        #se =  A + B/eta_s #(1+eta_i)/(A+C+(B+D)/eta_s)

        se = 2/(A + B/eta_s + C*eta_i + D*(eta_i/eta_s))
        
        return -20 * np.log10(np.abs(se))
    
    def get_se_TE(self, freq):
        
        T_total = np.identity(2, dtype=np.clongdouble)
        k_1 = self._layer_list[0].k(freq)
        eta_i = self._layer_list[0].eta(freq)
        eta_s = self._layer_list[-1].eta(freq)

        for mi in reversed(self._layer_list[1:-1]):
            Z_i = mi.Zo_from_theta_i_TE(freq, self.theta_i, k_1)
            k_i = self.k_x(freq, mi, Z_i)
            Ti = mi.T_TE(freq, self.theta_i, k_1, k_i)  # Get ABCD matrix
            T_total = Ti @ T_total    # Matrix multiply: T_i * T_total

        A, B = T_total[0, 0], T_total[0, 1]
        C, D = T_total[1, 0], T_total[1, 1]

        #se =  A + B/eta_s #(1+eta_i)/(A+C+(B+D)/eta_s)

        se = 2/(A + B/eta_s + C*eta_i + D*(eta_i/eta_s))
        
        return -20 * np.log10(np.abs(se))
    
    def k_x(self, freq, mi: Medium, Zi):
        k_x = 2 * np.pi * freq * mi.u/Zi
        return k_x

    def get_reflexion_TE(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TE

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        k_1 = self._layer_list[0].k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TE(freq, self._theta_1, k_1)

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for mi in self._layer_list[-2:0:-1]:
            Zo = mi.Zo_from_theta_i_TE(freq, self._theta_1, k_1)
            gammaL = mi.gamma(freq) * mi.width(freq)
            
            # Calculo de la impedancia equivalente
            Zeq = self.Zin(Zo, Zeq, gammaL)

        Zo = self._layer_list[0].Zo_from_theta_i_TE(freq, self._theta_1, k_1)

        return self.Gamma(Zo, Zeq)
    
    @property
    def theta_i(self):
        return self._theta_1

    @theta_i.setter
    def theta_i(self, value):
        if 0 <= value <= np.pi/2:
            self._theta_1 = value

    @property
    def theta_r(self):
        return self.theta_i


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

Separar coef de transmision y reflexion del poynting

Agregar coef de transmision del poynting en barrido de angulo para perp y par

Sobre las clases:

2_ondas, pag. 34-> d = 9,375mm

'''
