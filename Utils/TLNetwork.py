
import numpy as np
from Utils.Medium import Medium

class TLineNetwork():

    def __init__(self, layer_list: list[Medium], theta_i: float):
        # Calculo de la lista de medios con sus angulos de propagacion
        self._theta_i = theta_i
        self._layer_list = layer_list

        pass

    def Zin(self, Zo, Zl, gammaL):
    def Zin(self, Zo, Zl, gammaL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * espesor del medio.

        '''
        return Zo*(Zl+Zo*np.tanh(gammaL, dtype=np.clongdouble))/(Zo+Zl*np.tanh(gammaL, dtype=np.clongdouble))

    def ref_coef(self, Zo, Zl):
    def ref_coef(self, Zo, Zl):
        '''
        Calculo de coeficiente de reflexion en una interfaz
        '''
        return (Zl-Zo)/(Zl+Zo)
    
    def get_ref_and_loss_TM(self, freq):

        gamma_inc = self._layer_list[0].gamma_TM(freq, self._theta_i)
        Zl = self._layer_list[-1].Zo_TM_from_theta_inc(freq, self._theta_i, gamma_inc)
        loss = 0

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        # Tambien se van acumulando las perdidas de cada medio.
        for m_i in self._layer_list[-2:0:-1]:

            Zo = m_i.Zo_TM_from_theta_inc(freq, self._theta_i, gamma_inc)
            gammaL = m_i.gamma_TM_from_theta_inc(freq, self._theta_i, gamma_inc) * m_i.width(freq)

            # Calculo de perdidas de la capa actual
            a = np.exp(2*np.real(gammaL), dtype=np.longdouble)
            ref_coef = self.ref_coef(Zo, Zl)
            ref_coef = self.ref_coef(Zo, Zl)
            loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.longdouble)**2) /
                                (a * (1-np.abs(ref_coef, dtype=np.longdouble)**2)), dtype=np.longdouble)

            # Calculo de la impedancia equivalente
            Zl = self.Zin(Zo, Zl, gammaL)

        Zo = self._layer_list[0].Zo_TM(freq, self._theta_i)
        
        return self.ref_coef(Zo, Zl), loss


    def get_ref_and_loss_TE(self, freq):
        
        gamma_inc = self._layer_list[0].gamma_TE(freq, self._theta_i)
        Zl = self._layer_list[-1].Zo_TE_from_theta_inc(freq, self._theta_i, gamma_inc)
        loss = 0

        for m1 in self._layer_list[-2:0:-1]:
            Zo = m1.Zo_TE_from_theta_inc(freq, self._theta_i, gamma_inc)
            gammaL = m1.gamma_TE_from_theta_inc(freq, self._theta_i, gamma_inc) * m1.width(freq)
            
            a = np.exp(2*np.real(gammaL), dtype=np.longdouble)
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.longdouble)**2) /
                                (a * (1 - np.abs(ref_coef, dtype=np.longdouble)**2)), dtype=np.longdouble)
            Zl = self.Zin(Zo, Zl, gammaL)

        Zo = self._layer_list[0].Zo_TE(freq, self._theta_i)

        return self.ref_coef(Zo, Zl), loss
    

    @property
    def theta_i(self):
        return self._theta_i

    @theta_i.setter
    def theta_i(self, value):
        if 0 <= value <= np.pi/2:
            self._theta_i = value

    @property
    def theta_r(self):
        return self.theta_i


if __name__ == "__main__":
    m1 = Medium(1, 1, 0, width=100)
    m2 = Medium(4, 1, 0, width=0.1)
    m4 = Medium(9, 1, 0, width=100)

    med_list = [m1, m2, m4]
    net = TLineNetwork(med_list, 0)
    print(net.get_ref_and_loss_TE(100E6))
    print(net.get_ref_and_loss_TE(100E6))
    pass


'''
Corregir ley de snell por las formulas q me mando patricio

Separar coef de transmision y reflexion del poynting

Agregar coef de transmision del poynting en barrido de angulo para perp y par


'''
