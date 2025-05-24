
import numpy as np

from Utils.Medium import Medium

class TLineNetwork():

    def __init__(self, layer_list: list[Medium], theta_i: float):
        # Calculo de la lista de medios con sus angulos de propagacion
        self._theta_i = theta_i
        self._layer_list = layer_list

        pass

    def eta_in(self, eta_0, eta_1, gammaL):
        '''
        Funcion que calcula la impedancia equivalente vista desde 
        una distancia L de una interfaz entre 2 medios.

        Zo : float - Impedancia caracteristica del medio de incidencia
        Zl : float - Impedancia del medio luego de la interfaz
        gammaL : complex float - const de propagacion * espesor del medio.

        '''
        return eta_0*(eta_1+eta_0*np.tanh(gammaL, dtype=np.clongdouble))/(eta_0+eta_1*np.tanh(gammaL, dtype=np.clongdouble))

    def Gamma(self, eta_0, eta_1):
        '''
        Calculo de coeficiente de reflexion en una interfaz
        '''
        return (eta_1-eta_0)/(eta_1+eta_0)

    def get_ref_in_TM(self, freq):
         # Cargo la impedancia caracteristica de la capa final a donde se transmite la onda
        gamma_i = self._layer_list[0].gamma(freq)
        eta_eq = self._layer_list[-1].eta_from_theta_i_TM(freq, self._theta_i, gamma_i)

        # Para cada medio intermedio, calculo su impedancia de entrada equivalente
        # teniendo en cuenta todas las capas anteriores.
        for m1 in self._layer_list[-2:0:-1]:
            eta_0 = m1.eta_from_theta_i_TM(freq, self._theta_i, gamma_i)
            gammaL = m1.gamma_from_theta_i_TM(freq, self._theta_i, gamma_i) * m1.width(freq)
            eta_eq = self.eta_in(eta_0, eta_eq, gammaL)

        eta_0 = self._layer_list[0].eta_TM(freq, self._theta_i)

        return self.Gamma(eta_0, eta_eq)
    
    #a = np.exp(2*np.real(gammaL), dtype=np.longdouble)
    #loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.longdouble)**2) /
    #                    (a * (1-np.abs(ref_coef, dtype=np.longdouble)**2)), dtype=np.longdouble)

    def compute_shielding_effectiveness(self, freq):
        """
        Calculate shielding effectiveness (SE) using transmission line theory for multilayer mediums.
        
        Args:
            freq (float): Frequency in Hz.
            
        Returns:
            float: Shielding effectiveness in dB.
        """

        gamma_i_incident = self._layer_list[0].gamma(freq)
        theta_i = self._theta_i
        Z0 = self._layer_list[0].eta_TM(freq, theta_i)

        # Intermediate layers (excluding incident and transmitting)
        intermediate_layers = self._layer_list[1:-1]
        if not intermediate_layers:
            raise ValueError("At least one intermediate layer is required.")

        # 1. Compute characteristic impedances (Zi) for intermediate layers
        Z_list = [layer.eta_from_theta_i_TM(freq, theta_i, gamma_i_incident) for layer in intermediate_layers]

        # 2. Compute parameter 'p'
        # Numerator: 2Z0 * product(2Zi)
        numerator_p = 2 * Z0 * np.prod([2 * Zi for Zi in Z_list])
        # Denominator: (Z0 + Z2) * (ZN_1 + Z0) * product(Zi + Zi+1)
        term1 = Z0 + Z_list[0]
        term2 = Z_list[-1] + Z0
        product_denominator = term1 * term2 * np.prod([Z_list[i] + Z_list[i+1] 
                                                     for i in range(len(Z_list)-1)])
        p = numerator_p / product_denominator

        # 3. Compute input impedances Z(d_i) recursively
        Z_d = [Z0]  # Start with transmitting medium's impedance (Z0)
        for layer in reversed(intermediate_layers):
            gammaL = layer.gamma_from_theta_i_TM(freq, theta_i, gamma_i_incident) * layer.width(freq)
            eta_layer = layer.eta_from_theta_i_TM(freq, theta_i, gamma_i_incident)
            Z_in = self.eta_in(eta_layer, Z_d[0], gammaL)
            Z_d.insert(0, Z_in)  # Prepend to maintain order
        Z_d = Z_d[:-1]  # Remove the redundant Z0 at the end

        # 4. Compute 'q_i' for each layer
        q = []
        for i in range(len(Z_list)):
            Zi = Z_list[i]
            Z_prev = Z0 if i == 0 else Z_list[i-1]
            Zd_i = Z_d[i]
            numerator = (Zi - Z_prev) * (Zi - Zd_i)
            denominator = (Zi + Z_prev) * (Zi + Zd_i)
            q_i = numerator / denominator
            q.append(q_i)

        # 5. Compute product term: e^{j k_sn d_n} * (1 - q_i e^{-j 2 k_sn d_n})
        product_term = 1.0
        for i, layer in enumerate(intermediate_layers):
            gamma_layer = layer.gamma_from_theta_i_TM(freq, theta_i, gamma_i_incident)
            d_layer = layer.width(freq)
            gammaL = gamma_layer * d_layer
            exp_term = np.exp(gammaL)
            term = exp_term * (1 - q[i] * np.exp(-2 * gammaL))
            product_term *= term

        # 6. Calculate SE
        SE = 20 * np.log10(np.abs((1 / p) * product_term))
        return SE


    def get_ref_and_loss_TE(self, freq):
        '''
        Calculo de impedancia equivalente y perdidas acumuladas de toda la cadena de lineas
        para ondas TE. Para funcionamiento ver calc_total_equiv_impedance_and_loss_par

         freq : float - frecuencia de operacion en Hz
        Returns:
        tuple[complex, float] - (total impedancia equivalente, total perdidas acumuladas en dB)
        '''
        gamma_i = self._layer_list[0].gamma(freq)
        Zl = self._layer_list[-1].eta_from_theta_i_TE(
            freq, self._theta_i, gamma_i)
        loss = 0
        for m1 in self._layer_list[-2:0:-1]:
            Zo = m1.eta_from_theta_i_TE(freq, self._theta_i, gamma_i)
            gammaL = m1.gamma_from_theta_i_TM(
                freq, self._theta_i, gamma_i) * m1.width(freq)
            a = np.exp(2*np.real(gammaL), dtype=np.longdouble)
            ref_coef = (Zl-Zo)/(Zl+Zo)
            loss += 10*np.log10((a**2 - np.abs(ref_coef, dtype=np.longdouble)**2) /
                                (a * (1 - np.abs(ref_coef, dtype=np.longdouble)**2)), dtype=np.longdouble)
            Zl = self.eta_in(Zo, Zl, gammaL)
        
        Zo = self._layer_list[0].Zo_TE(freq, self._theta_i)
        return self.Gamma(Zo, Zl), loss
        

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
    print(net.get_ref_and_loss_TM(100e6))
    pass


'''
Corregir ley de snell por las formulas q me mando patricio

Separar coef de transmision y reflexion del poynting

Agregar coef de transmision del poynting en barrido de angulo para perp y par


'''
