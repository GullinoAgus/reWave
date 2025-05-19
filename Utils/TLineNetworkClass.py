
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

        pass

    def calc_equiv_impedance(self, Zo, Zl, gammaL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * espesor del medio.

        '''
        return Zo*(Zl+Zo*np.tanh(gammaL, dtype=np.complex256))/(Zo+Zl*np.tanh(gammaL, dtype=np.complex256))

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
        gamma_i = self._layer_list[0].prop_coef(freq)
        Zl = self._layer_list[-1].Zo_from_theta_i_par(
            freq, self._theta_i, gamma_i)
        loss = 0

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        # Tambien se van acumulando las perdidas de cada medio.
        for m1 in self._layer_list[-2:0:-1]:
            Zo = m1.Zo_from_theta_i_par(freq, self._theta_i, gamma_i)
            gammaL = m1.prop_coef_from_theta_i_par(
                freq, self._theta_i, gamma_i) * m1.width(freq)

            # Calculo de perdidas de la capa actual
            a = np.exp(2*np.real(gammaL), dtype=np.float128)
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.float128)**2) /
                                (a * (1-np.abs(ref_coef, dtype=np.float128)**2)), dtype=np.float128)

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
        Zo = self._layer_list[0].Zo_par(freq, self._theta_i)
        return self.calc_reflection_coeff(Zo, Zl), losses

    def calc_total_equiv_impedance_and_loss_per(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TE. Para funcionamiento ver calc_total_equiv_impedance_and_loss_par

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)
        '''
        gamma_i = self._layer_list[0].prop_coef(freq)
        Zl = self._layer_list[-1].Zo_from_theta_i_per(
            freq, self._theta_i, gamma_i)
        loss = 0
        for m1 in self._layer_list[-2:0:-1]:
            Zo = m1.Zo_from_theta_i_per(freq, self._theta_i, gamma_i)
            gammaL = m1.prop_coef_from_theta_i_par(
                freq, self._theta_i, gamma_i) * m1.width(freq)
            a = np.exp(2*np.real(gammaL), dtype=np.float128)
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.float128)**2) /
                                (a * (1 - np.abs(ref_coef, dtype=np.float128)**2)), dtype=np.float128)
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
        Zo = self._layer_list[0].Zo_per(freq, self._theta_i)
        return self.calc_reflection_coeff(Zo, Zl), losses

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
    print(net.calc_total_reflection_coef_par(100e6))
    pass


'''
Corregir ley de snell por las formulas q me mando patricio

Separar coef de transmision y reflexion del poynting

Agregar coef de transmision del poynting en barrido de angulo para perp y par


'''
