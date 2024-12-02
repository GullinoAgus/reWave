import numpy as np
from MediumClass import Medium

from Utils.TLineNetworkClass import Interface


if __name__ == "__main__":
    m1 = Medium(1, 1, 0, width=100)
    m2 = Medium(5, 1, 0, width=50)
    m4 = Medium(3, 1, 0, width=100)
    interfase12 = Interface(m1, m2)
    freq = 100e6
    med_list = [m2]
    theta_i = np.arctan2(np.sqrt(5), 1)
    interfase12.theta_i = theta_i
    theta_t = interfase12.theta_t
    resulting_matrix = np.identity(2)
    print(theta_i)
    for i in range(len(med_list)):
        resulting_matrix = resulting_matrix @ med_list[i].T_mat_par(
            freq, theta_t)
    print((m1.Zo_par(freq, theta_i) - m2.Zo_par(freq, theta_t)) /
          (m1.Zo_par(freq, theta_i) + m2.Zo_par(freq, theta_t)))
    print(m2.Zo_par(freq, theta_t))
    ntw = rf.a2s(np.array([resulting_matrix]), z0=m4.Zo_par(freq, theta_i))
    print("Resulting Matrix:")
    print(np.abs(ntw))
