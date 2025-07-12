
import numpy as np

from Utils.Medium import Medium
import scipy.constants as const

class TLineNetwork():

    def __init__(self, layer_list: list[Medium], theta_i: float):
        # Calculo de la lista de medios con sus angulos de propagacion
        self._theta_1 = theta_i
        self._layer_list = layer_list

        pass

    def Zin(self, Zi, Zl, kL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * espesor del medio.

        '''
        return Zi*(Zl+ 1j*Zi*np.tan(kL, dtype=np.clongdouble))/(Zi+1j*Zl*np.tan(kL, dtype=np.clongdouble))

    def Gamma(self, Zo, Zl):
        '''
        Calculo de coeficiente de reflexion en una interfaz
        '''
        return (Zl-Zo)/(Zl+Zo)
    
    def get_se_TM(self, freq):
        
        T_total = np.identity(2, dtype=np.clongdouble)
        m1 = self._layer_list[0]
        k_1 = self.k_x_i(freq, m1, m1) #TODO: No se si es k o k_x_1
        eta_i = m1.Zo_TM(freq, self.theta_i)
        eta_s = self._layer_list[-1].Zo_TM(freq, self.theta_i)

        if len(self._layer_list) == 2:
            tau = (1 + self.Gamma(eta_i, eta_s)) * (np.cos(self.theta_i)/np.cos(self.theta_t(freq)))
            se = 1 / tau     # Ei/Et
        else:
            for mi in reversed(self._layer_list[1:-1]):
                k_x_i = self.k_x_i(freq=freq, mi=mi, m1=m1)
                Ti = mi.T_TM(freq, self.theta_i, k_1, k_x_i)  # Get ABCD matrix
                T_total = Ti @ T_total    # Matrix multiply: T_i * T_total

            A, B = T_total[0, 0], T_total[0, 1]
            C, D = T_total[1, 0], T_total[1, 1]

            #se =  A + B/eta_s #(1+eta_i)/(A+C+(B+D)/eta_s)

            se = (A + B/eta_s + C*eta_i + D*(eta_i/eta_s))/2

        return np.abs(se)
    
    def get_se_TE(self, freq):
        
        T_total = np.identity(2, dtype=np.clongdouble)
        m1 = self._layer_list[0]
        k_1 = self.k_x_i(freq, m1, m1)
        eta_i = m1.Zo_TE(freq, self.theta_i)
        eta_s = self._layer_list[-1].Zo_TE(freq, self.theta_i)

        if len(self._layer_list) == 2:
            tau = 1 + self.Gamma(eta_i, eta_s)
            se = 1 / tau     # Ei/Et
        else:
            for mi in reversed(self._layer_list[1:-1]):
                k_x_i = self.k_x_i(freq=freq, mi=mi, m1=m1)
                Ti = mi.T_TE(freq, self.theta_i, k_1, k_x_i)  # Get ABCD matrix
                T_total = Ti @ T_total    # Matrix multiply: T_i * T_total

            A, B = T_total[0, 0], T_total[0, 1]
            C, D = T_total[1, 0], T_total[1, 1]

            se = (A + B/eta_s + C*eta_i + D*(eta_i/eta_s))/2
            #se = ((A+C)+(B+D)*(eta_i/eta_s))/(1+eta_i)

        return np.abs(se)
        
    def k_x_i(self, freq, mi: Medium, m1: Medium):
        k0 = 2 * np.pi * freq / const.c
        sin2_theta = np.sin(self.theta_i)**2
        k_x = k0 * np.sqrt((mi.ur * mi.e_comp(freq)- m1.ur * m1.e_comp(freq) * sin2_theta)/const.epsilon_0, dtype=np.clongdouble)
        return k_x

    def get_reflexion_TM(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        m1 = self._layer_list[0]
        k_1 = m1.k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TM(freq, self.theta_i, k_1)

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for mi in reversed(self._layer_list[1:-1]):
            Zi = mi.Zo_from_theta_i_TM(freq, self.theta_i, k_1)
            #print("### m1 ###") 
            #print(m1)
            #print("### mi ###")
            #print(mi)
            kL = self.k_x_i(freq=freq, mi=mi, m1=m1) * mi.width(freq)
            #print(kL)
            Zeq = self.Zin(Zi, Zeq, kL)
            #print(Zeq)
        Zi = self._layer_list[0].Zo_from_theta_i_TM(freq, self.theta_i, k_1)
        Gamma_in = self.Gamma(Zi, Zeq)

        return Gamma_in

    def get_reflexion_TE(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        m1 = self._layer_list[0]
        k_1 = m1.k(freq)
        Zeq = self._layer_list[-1].Zo_from_theta_i_TE(freq, self.theta_i, k_1)

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for mi in reversed(self._layer_list[1:-1]):
            Zi = mi.Zo_from_theta_i_TE(freq, self.theta_i, k_1)
            kL = self.k_x_i(freq=freq, mi=mi, m1=m1) * mi.width(freq)
            Zeq = self.Zin(Zi, Zeq, kL)
        Zi = self._layer_list[0].Zo_from_theta_i_TE(freq, self.theta_i, k_1)
        Gamma_in = self.Gamma(Zi, Zeq)

        return Gamma_in
    
    def is_evanescent(self, k_x: complex, tol: float = 1e-8) -> bool:
        return np.abs(np.real(k_x)) < tol and np.imag(k_x) > tol
    
    def theta_t(self, freq):
        m1 = self._layer_list[0]
        mN = self._layer_list[-1]
        sin_theta_t = m1.k(freq) / mN.k(freq) * np.sin(self.theta_i)
        #print(m1.k(freq), mN.k(freq), np.sin(self.theta_i), np.sin(self.theta_i), self.theta_i)
        # Si es complejo o el argumento excede [-1, 1], entonces onda evanescente
        if np.iscomplex(sin_theta_t) or not -1 <= np.real(sin_theta_t) <= 1:
            return np.pi/2

        return np.arcsin(sin_theta_t)
    
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
