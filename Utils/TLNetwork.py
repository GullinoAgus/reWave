
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

    def get_reflexion_and_SE_TM(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        q_i = []
        k_i = []
        d_i = []

        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        k_1 = self._layer_list[0].k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)

        #p calculation
        Zis = np.array([layer.Zo_from_theta_i_TE(freq, self._theta_1, k_1) for layer in self._layer_list])
        num_p = 2 * self._layer_list[0].Zo_from_theta_i_TM(freq, self._theta_1, k_1) * np.prod(Zis[1:-1] * 2)
        den_p = (Zis[0] + Zis[2]) * (Zis[-1] + Zis[2]) * np.prod(Zis[2:-2] + Zis[3:-1])
        p = num_p/den_p

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for i, mi in enumerate(self._layer_list[-2:0:-1]):
            Zo = mi.Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            Zo_next = self._layer_list[i+1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            gammaL = mi.gamma(freq) * mi.width(freq)
            
            # Calculo de la impedancia equivalente
            Zeq = self.Zin(Zo, Zeq, gammaL)
            q_i.append(self.Gamma(Zo, Zo_next) * self.Gamma(Zo, Zeq))
            k_i.append(mi.k(freq))
            d_i.append(mi.width(freq))
            
        Zo = self._layer_list[0].Zo_from_theta_i_TM(freq, self._theta_1, k_1)

        q_i = np.array(q_i)
        k_i = np.array(k_i)
        d_i = np.array(d_i)
        exp_jkdi = np.exp(1j * k_i * d_i)
        exp_m2jkdi = np.exp(-2j * k_i * d_i)
        SE = 20 * np.log10(np.abs(np.prod(exp_jkdi * (1 - q_i * exp_m2jkdi))/p))

        return self.Gamma(Zo, Zeq), SE


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
    
    def k_x(self, freq, m1: Medium, mi: Medium):

        k_0 = 2 * np.pi * freq * np.sqrt(const.mu_0 * const.epsilon_0, dtype=np.clongdouble)
        k_x = k_0 * np.sqrt((mi.ur * mi.e_comp(freq) - m1.ur * m1.e_comp(freq) * (np.sin(self.theta_i)**2))//const.epsilon_0, dtype=np.clongdouble)
        return k_x
    
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

    print(net.get_reflexion_and_SE_TM())
    pass


'''
Corregir ley de snell por las formulas q me mando patricio

Separar coef de transmision y reflexion del poynting

Agregar coef de transmision del poynting en barrido de angulo para perp y par

Sobre las clases:

2_ondas, pag. 34-> d = 9,375mm

'''
