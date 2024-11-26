import numpy as np
from MediumClass import Medium
import skrf as rf


if __name__ == "__main__":
    m1 = Medium(1, 1, 0, width=100)
    m2 = Medium(5, 1, 0, width=50)
    m4 = Medium(1, 1, 0, width=100)
    freq = 100e6
    med_list = [m2]

    resulting_matrix = np.identity(2)
    print(m2.prop_coef(freq))
    for i in range(len(med_list)):
        resulting_matrix = resulting_matrix @ med_list[i].T_mat_par(freq, 0)
    print(m2.Zo_par(freq, 0))
    ntw = rf.a2s(np.array([resulting_matrix]), z0=m4.Zo_par(freq, 0))
    print("Resulting Matrix:")
    print(ntw)
