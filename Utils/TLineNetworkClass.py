
import numpy as np

from Utils.MediumClass import Medium

# http://mwl.diet.uniroma1.it/people/pisa/RFELSYS/MATERIALE%20INTEGRATIVO/BOOKS/Pozar_Microwave%20Engineering(2012).pdf

# Transmission-Line Analogies of Plane Electromagnetic-Wave Reflections ARTHUR BRONWELL, SENIOR MEMBER, I.R.E.

# https://www.researchgate.net/profile/Suthasinee-Lamultree/publication/229091611_Analysis_of_planar_multilayer_structures_at_oblique_incidence_using_an_equivalent_BCITL_model/links/0fcfd50052d1b542b9000000/Analysis-of-planar-multilayer-structures-at-oblique-incidence-using-an-equivalent-BCITL-model.pdf


class TLineNetwork():

    def __init__(self, layer_list: list[Medium], theta_i: float):
        # Calculo de la lista de medios con sus angulos de propagacion
        self._theta_i = theta_i
        self._layer_list = layer_list
        self._theta_mediums = [theta_i] + [self.get_theta_t(m1, m2) for m1, m2 in zip(
            self._layer_list[:-1], self._layer_list[1:])]

        pass

    def calc_equiv_impedance(self, Zo, Zl, gammaL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * ancho del medio.

        '''
        return Zo*(Zl+Zo*np.tanh(gammaL))/(Zo+Zl*np.tanh(gammaL))

    def calc_reflection_coeff(self, Zo, Zl):
        '''
        Calculo de coeficiente de reflexion en una interfaz
        '''
        return (Zl-Zo)/(Zl+Zo)

    def calc_total_equiv_impedance_and_loss_par(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)

        '''
        # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        Zl = self._layer_list[-1].Zo_par(freq, self._theta_mediums[-1])
        loss = 0
        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        # Tambien se van acumulando las perdidas de cada medio.
        for m1, theta1 in zip(self._layer_list[-2:0:-1], self._theta_mediums[-2:0:-1]):
            Zo = m1.Zo_par(freq, theta1)
            gammaL = m1.prop_coef_par(freq, theta1) * m1.width(freq)

            # Calculo de perdidas de la capa actual
            a = np.exp(2*np.real(gammaL), dtype=np.float128)
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef)**2) /
                                (a * (1-np.abs(ref_coef)**2)))

            # Calculo de la impedancia equivalente
            Zl = self.calc_equiv_impedance(Zo, Zl, gammaL)

        return Zl, loss

    def calc_total_reflection_coef_and_losses_par(self, freq):
        '''
        Calculo del coeficiente de reflexion entre el medio de incidencia y el sistema multicapa
        y las perdidas acumuladas de toda la cadena de lineas
        para ondas TM

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total coeficiente de reflexion, total perdidas acumuladas en dB)

        '''
        Zl, losses = self.calc_total_equiv_impedance_and_loss_par(freq)
        Zo = self._layer_list[0].Zo_par(freq, self._theta_mediums[0])
        return self.calc_reflection_coeff(Zo, Zl), losses

    def calc_total_equiv_impedance_and_loss_per(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TE. Para funcionamiento ver calc_total_equiv_impedance_and_loss_par

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)
        '''
        Zl = self._layer_list[-1].Zo_per(freq, self._theta_mediums[-1])
        loss = 0
        for m1, theta1 in zip(self._layer_list[-2:0:-1], self._theta_mediums[-2:0:-1]):
            Zo = m1.Zo_per(freq, theta1)
            gammaL = m1.prop_coef_per(freq, theta1) * m1.width(freq)
            a = np.exp(2*np.real(gammaL))
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef)**2) /
                                (a * (1-np.abs(ref_coef)**2)))
            Zl = self.calc_equiv_impedance(Zo, Zl, gammaL)
        return Zl, loss

    def calc_total_reflection_coef_and_losses_per(self, freq):
        '''
        Calculo del coeficiente de reflexion entre el medio de incidencia y el sistema multicapa
        y las perdidas acumuladas de toda la cadena de lineas
        para ondas TE

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total coeficiente de reflexion, total perdidas acumuladas en dB)

        '''
        Zl, losses = self.calc_total_equiv_impedance_and_loss_per(freq)
        Zo = self._layer_list[0].Zo_per(freq, self._theta_mediums[0])
        return self.calc_reflection_coeff(Zo, Zl), losses

    @property
    def theta_i(self):
        return self._theta_i

    @theta_i.setter
    def theta_i(self, value):
        if 0 <= value <= np.pi/2:
            self._theta_i = value

    def get_theta_t(self, m1: Medium, m2: Medium):
        n1 = m1.n
        n2 = m2.n
        theta_i = self.theta_i
        sin_teta_i = np.sin(theta_i)

        if n1 == n2:
            return theta_i
        else:
            snell = (n1 * sin_teta_i) / n2
            if snell > 1 or snell < -1:
                return np.pi/2  # Snell's Law not applicable, total internal reflection
            theta_t = np.arcsin(snell)
            return theta_t

    @property
    def theta_r(self):
        return self.theta_i


if __name__ == "__main__":
    m1 = Medium(1, 1, 0, width=100)
    m2 = Medium(4, 1, 0, width=0.1)
    m4 = Medium(9, 1, 0, width=100)

    med_list = [m1, m2, m4]
    net = TLineNetwork(med_list, 0)
    print(net.calc_total_reflection_coef_par(100e6))
    pass
