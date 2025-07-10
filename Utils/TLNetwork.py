
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
        se = 0
        Zieq = []

        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        k_1 = self._layer_list[0].k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)

        #p calculation
        Zis = np.array([layer.Zo_from_theta_i_TM(freq, self._theta_1, k_1) for layer in self._layer_list])
        num_p = 2 * self._layer_list[0].Zo_from_theta_i_TM(freq, self._theta_1, k_1) * np.prod(Zis[1:-1] * 2)
        den_p *= np.prod(Zis[:-1] + Zis[1:])
        p = num_p/den_p

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for mi in self._layer_list[-2:0:-1]:
            Zi = mi.Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            gammaL = mi.gamma(freq) * mi.width(freq)
            Zeq = self.Zin(Zi, Zeq, gammaL)
            Zieq.append(Zeq)
        Zi = self._layer_list[0].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
        Gamma_in = self.Gamma(Zi, Zeq)

        q_i = self.get_q(freq, k_1)
        for i, layer in enumerate(self._layer_list[1:-1]):
            k_i = self.k_x(freq, self._layer_list[0], layer)
            d_i = mi.width(freq)
            exp_jkdi = np.exp(1j * k_i * d_i)
            exp_m2jkdi = np.exp(-2j * k_i * d_i)
            se *= exp_jkdi * (1 - q_i[i] * exp_m2jkdi)
            
        SE = 20 * np.log10(np.abs(se/p))

        return Gamma_in, SE
    
    def get_Zdi_TM(self, idx, freq, k_1, Zdi_list):

        # Si estamos en la ultima capa del shield
        if idx == len(self._layer_list) - 2:
            Zo = self._layer_list[idx].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            Zdi_list.append(Zo)
            return Zo, Zdi_list
        
        Zi1 = self._layer_list[idx+1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
        Zi2 = self._layer_list[idx+2].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
        coskdi = np.cos(self.k_x(freq, self._layer_list[0], self._layer_list[idx+1]))
        senkdi = np.sin(self.k_x(freq, self._layer_list[0], self._layer_list[idx+1]))
        Zdi, Zdi_list = self.get_Zdi_TM(idx+1, freq, k_1, Zdi_list)

        Zdi = Zi1 * ((Zdi * coskdi + 1j * Zi1 * senkdi)
                     /(Zi2 * coskdi + 1j * Zdi * senkdi))
        
        return Zdi, Zdi_list.append(Zdi)

    def get_q(self, freq, k_1, i):

        Zdi_list = []
        qi_list = []

        _, Zdi_list = self.get_Zdi_TM(1, freq, k_1, Zdi_list)

        for 
        
        for i, _ in enumerate(self._layer_list[1:-1]):
            Zi = self._layer_list[i+1].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            Zim1 = self._layer_list[i].Zo_from_theta_i_TM(freq, self._theta_1, k_1)
            Zdi = Zdi_list[i]

            print(Zi, Zim1, Zdi)

            qi = self.Gamma(Zim1, Zi) * self.Gamma(Zdi, Zi)
            print(qi)
            qi_list.append(qi)
            print(qi_list)

        return qi_list
        

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
        k_x = k_0 * np.sqrt((mi.ur * mi.e_comp(freq) - m1.ur * m1.e_comp(freq) * (np.sin(self.theta_i)**2))/const.epsilon_0, dtype=np.clongdouble)
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
